import json
import os

def init_json_file(filename, init_data={}):
    if not os.path.isfile(filename):
        with open(filename, "w") as f:
            json.dump(init_data, f)
            print(f"File '{filename}' created and initialized with data {init_data}.")
    else:
        print(f"File '{filename}' already exists.")

# 读取 JSON 文件
def read_json_file(filename):
    with open(filename, "r") as f:
        data = json.load(f)
    return data

# 写入 JSON 文件
def write_json_file(data, filename):
    with open(filename, "w") as f:
        json.dump(data, f, indent=4)

# 根据键名获取对应的值
def get_value(data, key):
    if isinstance(data, dict):
        if key in data:
            return data[key]
        else:
            for k, v in data.items():
                result = get_value(v, key)
                if result is not None:
                    return result
    elif isinstance(data, list):
        for item in data:
            result = get_value(item, key)
            if result is not None:
                return result

# 根据键名修改对应的值
def update_value(data, key, new_value):
    if isinstance(data, dict):
        if key in data:
            data[key] = new_value
        else:
            for k, v in data.items():
                update_value(v, key, new_value)
    elif isinstance(data, list):
        for item in data:
            update_value(item, key, new_value)

# 根据键名删除对应的键值对或者列表元素
def delete_value(data, key):
    if isinstance(data, dict):
        if key in data:
            del data[key]
        else:
            for k, v in data.items():
                delete_value(v, key)
    elif isinstance(data, list):
        for item in data:
            if isinstance(item, dict) and key in item:
                data.remove(item)
            else:
                delete_value(item, key)

# 添加键值对
def add_key_value(data, key, value):
    if isinstance(data, dict):
        data[key] = value
    elif isinstance(data, list):
        data.append(value)


if __name__ == "__main__":
    # 读取 JSON 文件
    test_file = "./venv/.test.json"

    init_json_file(test_file, init_data={"name": "fguiju"})

    data = read_json_file(test_file)
    print("原始数据：", data)

    # 获取键值对
    value = get_value(data, "name")
    print("获取键值对：", value)

    # 修改键值对
    update_value(data, "name", "NewName")
    print("修改后数据：", data)

    # 删除键值对
    delete_value(data, "name")
    print("删除后数据：", data)

    # 添加键值对
    add_key_value(data, "new_key", "new_value")
    print("添加后数据：", data)

    # 写入 JSON 文件
    write_json_file(data, test_file)
