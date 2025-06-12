import pandas as pd
import os
import joblib

import IDS_Engine
from model_training import config

def IDS_preprocsss():
    os.system(f"cicflowmeter -f {config.pcap_name} -c {config.csv_name}")
    to_pred = pd.read_csv(config.csv_name, encoding='utf-8')

    to_pred = to_pred.drop([
        'Flow ID', 
        'Src IP', 
        'Src Port', 
        'Dst IP', 
        'Dst Port', 
        'Timestamp',
        'Label'
    ])

    pre = joblib.load('models/SSRC_Pre.pkl')
    pca = joblib.load('models/SSRC_PCA.pkl')
    mod = joblib.load('models/SSRC_RF.pkl')

    to_pred = pre.transform(to_pred)
    to_pred = pca.transform(to_pred)
    res = mod.predict(to_pred)
    return res

def IDS():
    return IDS_Engine.IDS()