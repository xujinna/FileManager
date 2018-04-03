import os, yaml


def analyze_yml(file_name, key_name):
    # 当前目录
    file_path = os.getcwd() + os.sep + "data" + os.sep + file_name + ".yml"
    with open(file_path, "r", encoding="utf-8") as r:
        return yaml.load(r)[key_name]