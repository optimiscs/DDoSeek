from smart_ids import IDS_Engine, ML_engine
from scapy.all import *
from utils import SOCKFILE_IDS_ALERT, DELIMITER
from utils import PacketLogger, getActionForLabel
import socket
from smart_ids.model_training import config

iface = 's3-eth2'
# MODEL = 'DL'
MODEL = 'ML'

# count = 0
# packets = []


def send_alert(alert):
    print("send alert:", alert)
    sock = socket.socket(socket.AF_UNIX, socket.SOCK_DGRAM)
    sock.connect(SOCKFILE_IDS_ALERT)
    sock.send(alert.encode())


# def predit():
#     label = IDS_Engine.IDS()  # call IDS
#     return label


def analyze_packet(pkt):
    s_ip = pkt[IP].src
    s_port = pkt[TCP].sport
    d_ip = pkt[IP].dst
    d_port = pkt[TCP].dport
    # rdpcap('existing.pcap')
    data = "NOPAYLOAD"
    ten_bytes = ""
    if 'Raw' in pkt:
        data = pkt['Raw'].load
    try:
        ten_bytes = " ".join(["%02x" % ord(ch) for ch in data][:10])
    except:
        pass
    # global count
    # global packets
    # if count == 5:
    #     label = predit()
    #     packets = []
    #     count = 0
    # else:
        # existing_packets = rdpcap(config.pcap_name)
        # new_packets = [pkt]
        # new_packets.append(pkt)
        # packets.append(pkt)
        # all_packets = existing_packets + new_packets
        # wrpcap(config.pcap_name, packets)
        # count += 1
        # return
    wrpcap(config.pcap_name, pkt)
    
    label = ''
    if MODEL == 'DL':
        label = IDS_Engine.IDS()  # call IDS
    if MODEL == 'ML':
        label = ML_engine.IDS()

    action = getActionForLabel(label)
    PacketLogger.record(action, label, s_ip, s_port, d_ip, d_port, str(data))

    if label != "BENIGN":
        # alert message <label, s_ip, s_port, d_ip, d_port, data>
        alert = DELIMITER.join([label, s_ip, str(s_port), d_ip, str(d_port), str(data)])
        send_alert(alert)
    # print("Packet [%s:%d --> %s:%d][%s] has been analyzed." % (s_ip, s_port, d_ip, d_port, ten_bytes))
    print("Packet [%s:%d --> %s:%d] has been analyzed." % (s_ip, s_port, d_ip, d_port))
    print("Payload:", ten_bytes)


if __name__ == '__main__':
    print("Sniffing...")
    sniff(iface=iface,
          prn=analyze_packet,
          filter="tcp")
