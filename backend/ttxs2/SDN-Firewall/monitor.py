
from __future__ import division
from ryu import cfg
from ryu.topology.switches import Switches
from ryu.topology.switches import LLDPPacket
from operator import attrgetter
from ryu.base import app_manager
from ryu.controller import ofp_event
from ryu.controller.handler import CONFIG_DISPATCHER, MAIN_DISPATCHER
from ryu.controller.handler import set_ev_cls
from ryu.ofproto import ofproto_v1_3
from ryu.lib.packet import packet
from ryu.lib.packet import ethernet
from ryu.lib.packet import ether_types
from ryu.topology import api as topo_api
from ryu.lib.packet import ipv4
from ryu.lib.packet import arp
from ryu.lib import hub

from ryu.topology import event, switches
from ryu.topology.api import get_all_switch, get_link, get_switch
from ryu.lib.ofp_pktinfilter import packet_in_filter, RequiredTypeFilter
from ryu.base.app_manager import lookup_service_brick

import networkx as nx
import sys
import time
import datetime


class monitor(app_manager.RyuApp):
    OFP_VERSIONS = [ofproto_v1_3.OFP_VERSION]

    def __init__(self, *args, **kwargs):
        super(monitor, self).__init__(*args, **kwargs)
        self.topology_api_app = self
        self.link_to_port = {}       # (src_dpid,dst_dpid)->(src_port,dst_port)
        self.access_table = {}       # {(sw,port) :[host1_ip]}
        self.switch_port_table = {}  # dpip->port_num
        self.access_ports = {}       # dpid->port_num
        self.interior_ports = {}     # dpid->port_num
        self.graph = nx.DiGraph()
        self.ip_to_mac = {}
        self.dps = {}
        self.tx_bytes = {}
        self.port_speed = {}
        self.switches = None        
        self.echo_latency = {}
        self.sw_module = lookup_service_brick('switches')
        self.discover_thread = hub.spawn(self._discover)        
        self.measure_thread = hub.spawn(self._detector)

        self.name = "monitor"
        self.delay_info = {
            "update_time": "",
            "delay_table": []
        }

    def _detector(self):
        """
            Delay detecting functon.
            Send echo request and calculate link delay periodically
        """
        while True:
            hub.sleep(5)
            self._send_echo_request()
            self.create_link_delay()
            self.delay_info['update_time'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            self.delay_info['delay_table'] = self.show_delay_statis()

    def _discover(self):
        while True:
            for datapath in self.dps.values():
                self.request_stats(datapath)
            self.get_topology(None)
            hub.sleep(5)

    def _send_echo_request(self):
        """
            Seng echo request msg to datapath.
        """
        for datapath in self.dps.values():
            parser = datapath.ofproto_parser
            echo_req = parser.OFPEchoRequest(datapath,
                                             data=str.encode("%.12f" % time.time()))
            datapath.send_msg(echo_req)
            hub.sleep(self.sending_echo_request_interval)

    @set_ev_cls(ofp_event.EventOFPEchoReply, MAIN_DISPATCHER)
    def echo_reply_handler(self, ev):
        """
            Handle the echo reply msg, and get the latency of link.
        """
        now_timestamp = time.time()
        try:
            latency = now_timestamp - eval(bytes.decode(ev.msg.data))
            self.echo_latency[ev.msg.datapath.id] = latency
        except:
            return

    def get_delay(self, src, dst):
        """
            Get link delay.
                        Controller
                        |        |
        src echo latency|        |dst echo latency
                        |        |
                   SwitchA-------SwitchB
                        
                    fwd_delay--->
                        <----reply_delay
            delay = (forward delay + reply delay - src datapath's echo latency
        """
        try:
            fwd_delay = self.graph[src][dst]['lldpdelay']
            re_delay = self.graph[dst][src]['lldpdelay']
            src_latency = self.echo_latency[src]
            dst_latency = self.echo_latency[dst]
            
            delay = (fwd_delay + re_delay - src_latency - dst_latency) / 2 * 1000 # ms
            return max(delay, 0.1)
        except:
            return float('inf')

    def _save_lldp_delay(self, src=0, dst=0, lldpdelay=0):
        try:
            self.graph[src][dst]['lldpdelay'] = lldpdelay
        except:
            return

    def create_link_delay(self):
        """
            Create link delay data, and save it into graph object.
        """
        try:
            for src in self.graph:
                for dst in self.graph[src]:
                    if src == dst:
                        self.graph[src][dst]['delay'] = 0
                        continue
                    delay = self.get_delay(src, dst)
                    self.graph[src][dst]['delay'] = delay
        except:
            return

    def show_delay_statis(self):
        delay_table = []
        self.logger.info("\nsrc   dst      delay     bw")
        self.logger.info("----------------------------------------------")
        for src in self.graph:
            for dst in self.graph[src]:
                delay = self.graph[src][dst]['delay']
                bw = 0.001
                if "bw" in self.graph[src][dst].keys():
                    bw = self.graph[src][dst]["bw"]
                self.logger.info("%s<-->%s : %.4f      %.4f" % (src, dst, delay, bw))
                delay_table.append({'src': src, 'dst': dst, 'delay': delay, 'bw': bw})
        return delay_table

    def request_stats(self, datapath):
        """
            Sending request msg to datapath
        """
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser
        req = parser.OFPPortStatsRequest(datapath, 0, ofproto.OFPP_ANY)
        datapath.send_msg(req)

    def get_topology(self, ev):
        """
            Get topology info
        """
        # print "get topo"
        switch_list = get_all_switch(self)        
        self.sending_echo_request_interval = 0.5
        # print switch_list
        self.create_port_map(switch_list)
        self.switches = self.switch_port_table.keys()
        links = get_link(self.topology_api_app, None)
        self.create_interior_links(links)
        self.create_access_ports()
        self.get_graph()

    def create_port_map(self, switch_list):
        for sw in switch_list:
            dpid = sw.dp.id
            self.graph.add_node(dpid)
            self.dps[dpid] = sw.dp
            self.switch_port_table.setdefault(dpid, set())
            self.interior_ports.setdefault(dpid, set())
            self.access_ports.setdefault(dpid, set())

            for p in sw.ports:
                self.switch_port_table[dpid].add(p.port_no)

    def create_interior_links(self, link_list):
        for link in link_list:
            src = link.src
            dst = link.dst
            self.link_to_port[
                (src.dpid, dst.dpid)] = (src.port_no, dst.port_no)

            # Find the access ports and interiorior ports
            if link.src.dpid in self.switches:
                self.interior_ports[link.src.dpid].add(link.src.port_no)
            if link.dst.dpid in self.switches:
                self.interior_ports[link.dst.dpid].add(link.dst.port_no)

    def create_access_ports(self):
        for sw in self.switch_port_table:
            all_port_table = self.switch_port_table[sw]
            interior_port = self.interior_ports[sw]
            self.access_ports[sw] = all_port_table - interior_port

    def get_graph(self):
        link_list = topo_api.get_all_link(self)
        for link in link_list:
            src_dpid = link.src.dpid
            dst_dpid = link.dst.dpid
            src_port = link.src.port_no
            dst_port = link.dst.port_no
            port_key = (src_dpid, src_port)
            self.graph.add_edge(src_dpid, dst_dpid,
                                src_port=src_port,
                                dst_port=dst_port,
                                bw=self.port_speed[port_key] if port_key in self.port_speed.keys() else 0.001)
        return self.graph


    @set_ev_cls(ofp_event.EventOFPPacketIn, MAIN_DISPATCHER)
    def _packet_in_handler(self, ev):
        msg = ev.msg
        datapath = msg.datapath

        parser = datapath.ofproto_parser
        in_port = msg.match['in_port']
        pkt = packet.Packet(msg.data)

        eth_type = pkt.get_protocols(ethernet.ethernet)[0].ethertype
        eth_pkt = pkt.get_protocol(ethernet.ethernet)
        arp_pkt = pkt.get_protocol(arp.arp)
        ip_pkt = pkt.get_protocol(ipv4.ipv4)
        if eth_type == ether_types.ETH_TYPE_LLDP:
            try:
                src_dpid, src_port_no = LLDPPacket.lldp_parse(msg.data)
                dpid = msg.datapath.id
                if self.sw_module is None:
                    self.sw_module = lookup_service_brick('switches')

                for port in self.sw_module.ports.keys():
                    if src_dpid == port.dpid and src_port_no == port.port_no:
                        port_data = self.sw_module.ports[port]
                        if port_data.timestamp:
                            delay = time.time() - port_data.timestamp
                            self._save_lldp_delay(src=src_dpid, dst=dpid,
                                                  lldpdelay=delay)
            except LLDPPacket.LLDPUnknownFormat as e:
                return
        else:
            if ip_pkt:
                src_ipv4 = ip_pkt.src
                src_mac = eth_pkt.src
                if src_ipv4 != '0.0.0.0' and src_ipv4 != '255.255.255.255':
                    self.ip_to_mac[src_ipv4] = src_mac

            if arp_pkt:
                arp_src_ip = arp_pkt.src_ip
                arp_dst_ip = arp_pkt.dst_ip
                mac = arp_pkt.src_mac

                # Record the access info
                self.ip_to_mac[arp_src_ip] = mac

    @set_ev_cls(ofp_event.EventOFPPortStatsReply, MAIN_DISPATCHER)
    def _port_stats_reply_handler(self, ev):
        """
            Save port's stats info
            Calculate port's speed and save it.
        """
        body = ev.msg.body
        dpid = ev.msg.datapath.id
        for stat in sorted(body, key=attrgetter('port_no')):
            port_no = stat.port_no
            if port_no != ofproto_v1_3.OFPP_LOCAL:
                key = (dpid, port_no)
                value = stat.tx_bytes
                if key in self.tx_bytes.keys():
                    speed = (value - self.tx_bytes[key]) / 1024 / 1024  # MB/s
                    if speed < 0.001:
                        speed = 0.001
                    self.port_speed[key] = speed
                else:
                    self.port_speed[key] = 0.001
                self.tx_bytes[key] = value

    def get_host_location(self, host_ip):
        """
            Get host location info:(datapath, port) according to host ip.
        """
        if host_ip in self.ip_to_mac.keys():
            host_mac = self.ip_to_mac[host_ip]
        else:
            return None
        for key in self.access_table.keys():
            if self.access_table[key] == host_mac:
                return key
        self.logger.debug("%s location is not found." % host_ip)
        return None

    def get_switches(self):
        return self.switches

    def get_links(self):
        return self.link_to_port

    def get_datapath(self, dpid):
        if dpid not in self.dps:
            switch = topo_api.get_switch(self, dpid)[0]
            self.dps[dpid] = switch.dp
            return switch.dp
        return self.dps[dpid]

    def add_flow(self, dp, p, match, actions, idle_timeout=0, hard_timeout=0):
        ofproto = dp.ofproto
        parser = dp.ofproto_parser

        inst = [parser.OFPInstructionActions(ofproto.OFPIT_APPLY_ACTIONS,
                                             actions)]

        mod = parser.OFPFlowMod(datapath=dp, priority=p,
                                idle_timeout=idle_timeout,
                                hard_timeout=hard_timeout,
                                match=match, instructions=inst)
        dp.send_msg(mod)


