import numpy
import json
with open("D://data//save_online_data//online_data1.json",'r') as file:
    load_dict = json.load(file)
    print(load_dict)
    load_dict["track"][0]["N"]=10

    # print(load_dict)
    out_file=open("D://data//out_online_data//online_data1.json", 'w')
    out_file.write(json.dumps(load_dict,indent=4))
    out_file.close()
