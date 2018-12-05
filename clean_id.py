import codecs
import re

'''
将pgsql数据库导出的attributes列中的数据解析读取出来

'''
path = ".\Data\\roma.txt"
desp = ".\Data\\r_node_id.txt"
pattern = "[0-9]+"
pattern2 = "([0-9]{1,}[.][0-9]*)"

file_handle = codecs.open(path, 'r', encoding='utf-8')
desp_handle = codecs.open(desp, 'w', encoding='utf-8')
lines = file_handle.readlines()

for line in lines:
    match_objects = re.split(' ', line)

    node_id = re.search(pattern, match_objects[0])[0]
    lat = re.search(pattern2, match_objects[1])[0]
    lng = re.search(pattern2, match_objects[2])[0]
    strt = node_id + '\t' + lat + '\t' + lng + '\r\n'
    desp_handle.writelines(strt)
