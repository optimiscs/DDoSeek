import torch

DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
EPOCHS = 250
NUM_WORKERS = 2
BATCH_SIZE = 100
NUM_CLASSES = 8
LEARNING_RATE = 1e-5
WEIGHT_DECAY = 1e-4
PIN_MEMORY = True
LOAD_MODEL = False
SAVE_MODEL = True
CHECKPOINT_FILE = "my_checkpoint.pth.tar"
TRAIN_DIR = "./total_23features_2_train.csv"
TEST_DIR = "./total_23features_2_test.csv"

types = ["BENIGN", "DrDoS_LDAP", "DrDoS_MSSQL", "DrDoS_NetBIOS",
         "DrDoS_UDP", "Syn", "Portmap", "UDP-lag"]
# types = ["BENIGN",
#          "Bruteforce DNS",
#          "DoS ACK",
#          "DoS FIN",
#          "DoS HTTP",
#          "DoS SYN",
#          "DoS UDP",
#          "Mirai DDoS DNS"]

# 23features
features = ['dst_port', 'protocol', 'flow_duration',
            'totlen_fwd_pkts', 'fwd_pkt_len_max', 'fwd_pkt_len_min',
            'fwd_pkt_len_std', 'flow_iat_mean',
            'flow_iat_max', 'flow_iat_min', 'fwd_iat_tot', 'fwd_iat_mean', 'fwd_iat_max',
            'fwd_header_len', 'fwd_pkts_s', 'pkt_len_min', 'pkt_len_max', 'pkt_len_mean',
            'pkt_len_std', 'ack_flag_cnt', 'subflow_fwd_byts', 'init_fwd_win_byts', 'fwd_seg_size_min']
# Index(['Dst Port', 'Protocol', 'Flow Duration', 'Total Length of Fwd Packet',
#        'Fwd Packet Length Max', 'Fwd Packet Length Min',
#        'Fwd Packet Length Std', 'Flow IAT Mean', 'Flow IAT Max',
#        'Flow IAT Min', 'Fwd IAT Total', 'Fwd IAT Mean', 'Fwd IAT Max',
#        'Fwd Header Length', 'Fwd Packets/s', 'Packet Length Min',
#        'Packet Length Max', 'Packet Length Mean', 'Packet Length Std',
#        'ACK Flag Count', 'Subflow Fwd Bytes', 'FWD Init Win Bytes',
#        'Fwd Seg Size Min']
# Index(['dst_port', 'protocol', 'flow_duration', 'fwd_pkts_s',
#        'totlen_fwd_pkts', 'fwd_pkt_len_max', 'fwd_pkt_len_min',
#        'fwd_pkt_len_std', 'pkt_len_max', 'pkt_len_min', 'pkt_len_mean',
#        'pkt_len_std', 'fwd_header_len', 'fwd_seg_size_min', 'flow_iat_mean',
#        'flow_iat_max', 'flow_iat_min', 'fwd_iat_tot', 'fwd_iat_max',
#        'fwd_iat_mean', 'ack_flag_cnt', 'init_fwd_win_byts',
#        'subflow_fwd_byts'],
#       dtype='object')

# 57features
# features = ["flow_duration", "tot_fwd_pkts", "tot_bwd_pkts", "totlen_fwd_pkts", "totlen_bwd_pkts",
#             "fwd_pkt_len_max", "fwd_pkt_len_mean", "fwd_pkt_len_std", "bwd_pkt_len_max", "bwd_pkt_len_mean",
#             "bwd_pkt_len_std", "flow_byts_s", "flow_pkts_s", "flow_iat_mean", "flow_iat_std",
#             "flow_iat_max", "flow_iat_min", "fwd_iat_tot", "fwd_iat_mean", "fwd_iat_std",
#             "fwd_iat_max", "fwd_iat_min", "bwd_iat_tot", "bwd_iat_mean", "bwd_iat_std",
#             "bwd_iat_max", "bwd_iat_min", "fwd_psh_flags", "fwd_header_len", "bwd_header_len",
#             "fwd_pkts_s", "bwd_pkts_s", "pkt_len_max", "pkt_len_mean", "pkt_len_std",
#             "pkt_len_var", "syn_flag_cnt", "urg_flag_cnt", "pkt_size_avg", "fwd_seg_size_avg",
#             "bwd_seg_size_avg", "subflow_fwd_pkts", "subflow_fwd_byts", "subflow_bwd_pkts", "subflow_bwd_byts",
#             "init_fwd_win_byts", "init_bwd_win_byts", "fwd_act_data_pkts", "fwd_seg_size_min", "active_mean",
#             "active_std", "active_max", "active_min", "idle_mean", "idle_std",
#             "idle_max", "idle_min"
#             ]
pcap_name = "tmp.pcap"
csv_name = "tmp.csv"
