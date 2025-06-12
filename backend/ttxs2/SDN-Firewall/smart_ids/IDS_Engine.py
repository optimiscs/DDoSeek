import torch
import torch.nn.functional as F
import os
import sys
import pandas as pd

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from model_training.model import ConvNet
from model_training import config

map_ = {0: "BENIGN", 1: "Bruteforce DNS", 2: "DoS HTTP", 3: "Mirai DDoS DNS", 4: "DoS UDP", 5: "DoS SYN", 6: "DoS ACK",
        7: "DoS RST"}

model = ConvNet()
model_file = os.path.split(os.path.realpath(__file__))[0] + f'/model_training/{config.CHECKPOINT_FILE}'
model.load_state_dict(torch.load(model_file, map_location=config.DEVICE)['state_dict'])
model = model.to(config.DEVICE)


def IDS():
    os.system(f"cicflowmeter -f {config.pcap_name} -c {config.csv_name}")
    features = pd.read_csv(config.csv_name, usecols=config.features)
    features = features[config.features]
    features.insert(7, "fwd_header_len.1", features["fwd_header_len"])
    features = torch.tensor(features.values, dtype=torch.float32)
    features.to(config.DEVICE)
    predit_label = model(features)
    print("predit_lable:")
    print(predit_label)
    predit_label = int(torch.argmax(F.log_softmax(predit_label, dim=1), dim=1))
    print(f"predit result:{predit_label} {map_[predit_label]}")
    return map_[predit_label]
