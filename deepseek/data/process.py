import os
import json

# 遍历当前目录下的所有 JSON 文件并修改其 instruction 字段
files = [f for f in os.listdir('.') if f.endswith('.json')]
for file in files:
    if file.endswith('.json'):
        with open(file, 'r', encoding='utf-8') as f:
            try:
                data = json.load(f)
                # 如果是列表类型的 JSON 文件，遍历每个元素
                if isinstance(data, list):
                    for item in data:
                        if isinstance(item, dict):
                            item['instruction'] = "Here is a JSON file of a network packet that may be used for DDOS attacks. Please analyze it and give its type with no more than one word from the following four choices: 1. MSSQL, 2. NetBIOS, 3. Syn, 4. UDP, 5. Benign(if it's not for DDoS attack)"
                # 如果是字典类型的 JSON 文件，直接修改 instruction 字段
                elif isinstance(data, dict):
                    data['instruction'] = "Here is a JSON file of a network packet that may be used for DDOS attacks. Please analyze it and give its type with no more than one word from the following four choices: 1. MSSQL, 2. NetBIOS, 3. Syn, 4. UDP, 5. Benign(if it's not for DDoS attack)"
                # 将修改后的数据写回文件
                with open(file, 'w', encoding='utf-8') as f_out:
                    json.dump(data, f_out, ensure_ascii=False, indent=4)
            except json.JSONDecodeError:
                print(f"{file}: 无法解析为JSON")