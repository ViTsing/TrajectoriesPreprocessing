import codecs
import os
import re
import datetime
from Format.T_Drive import mkdir

from math import radians, cos, sin, asin, sqrt

'''
用于计算驻留点
'''

class Point:
    '''
    To store a trajectory point
    '''

    def __init__(self, line_p):
        self.line = line_p.strip('\r\n')
        # line = re.sub("\.[0-9]+\+01", '', self.line)
        pattern1 = '\S+\s[0-9]{2}\:[0-9]{2}\:[0-9]{2}'
        line = re.search(pattern1, self.line)[0]
        match_objects = re.split(',', line)
        self.id = match_objects[0]
        # 纬度
        self.latitude = float(match_objects[2])
        # 经度
        self.longitude = float(match_objects[1])
        # 时间日期
        self.date_time = datetime.datetime.strptime(match_objects[3], "%Y-%m-%d %H:%M:%S")

    def __repr__(self):
        return repr((self.id, self.latitude, self.longitude, self.date_time))

    def output(self):
        return self.line


class Stay_Points:
    def __init__(self, point):
        self.point_list = list()
        self.point_list.append(point)

    def o_mean_point(self, file_handle):

        start_point = self.point_list[0]
        end_index = len(self.point_list) - 1
        end_point = self.point_list[end_index]
        inter = interval(end_point, start_point)
        # 返回不合格点的位置
        if inter <= 20:
            return 'ff'
        latitude = 0
        longitude = 0
        length = len(self.point_list)
        for point in self.point_list:
            latitude += point.latitude
            longitude += point.longitude
        arv = self.point_list[0].date_time
        lev = self.point_list[length - 1].date_time
        file_handle.writelines(
            str(latitude / length) + ',' + str(longitude / length) + ',' + str(arv) + ',' + str(lev) + '\r\n')
        return latitude / length, longitude / length, arv, lev

    def add(self, new_point, file_handle):
        index = 0
        for exsit_point in self.point_list:
            index += 1
            dist = distance(exsit_point, new_point)
            if dist > 200:
                # 如果下一个点不满足条件，判断已有序列长度
                if self.o_mean_point(file_handle) == 'ff':
                    return 'f', index
                else:

                    return 'f', len(self.point_list)
        # 如果所有点都满足
        self.point_list.append(new_point)
        return 't', 0


def haversine(lon1, lat1, lon2, lat2):  # 经度1，纬度1，经度2，纬度2 （十进制度数）
    """
    Calculate the great circle distance between two points (meters)
    on the earth (specified in decimal degrees)
    """
    # 将十进制度数转化为弧度
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

    # haversine公式
    # 经度差值
    dlon = lon2 - lon1
    # 纬度差值
    dlat = lat2 - lat1
    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * asin(sqrt(a))
    r = 6371.137  # 地球平均半径，单位为公里
    return c * r * 1000


def distance(p_1, p_2):
    '''
    :param p_1: point 1
    :param p_2: point 2
    :return: the distance between point 1 and point 2, measured by meters
    '''
    # 纬度1
    latitude_1 = p_1.latitude
    # 经度1
    longitude_1 = p_1.longitude
    # 纬度2
    latitude_2 = p_2.latitude
    # 经度2
    longitude_2 = p_2.longitude

    result = haversine(longitude_1, latitude_1, longitude_2, latitude_2)
    return abs(result)


def interval(p_1, p_2):
    '''
    :param p_1: Point 1
    :param p_2: Point 2
    :return: the time interval between Point 1 and Point 2, measured by minutes
    '''
    time_1 = p_1.date_time
    time_2 = p_2.date_time
    difference = (time_1 - time_2).total_seconds()
    return difference / 60


if __name__ == '__main__':
    # 定义输入输出路径
    root_path = "E:\DataSets\Preprocessed\Days\Feb\\"
    destination_folder = "E:\DataSets\Preprocessed\StayPoint\Feb\\"
    # 检验输入路径
    print(os.path.exists(root_path))
    # 遍历输入路径
    walk_results = os.walk(root_path)
    # 遍历路径下所有文件夹
    for root, dirs, files in walk_results:
        if len(dirs) > 0:
            for dir in dirs:
                new_folder = (destination_folder + dir).replace('Days', 'StayPoint', 1)
                mkdir(new_folder)
        # 当遍历到叶节点层时，返回所有文件
        if len(files) > 0:
            # 遍历当前文件夹所有文件
            for file in files:
                # 初始化用于存储point的列表
                list_temp = list()
                # 打开并读入某车某日的Trajectory轨迹
                path = root + '\\' + file
                file_handle = codecs.open(path, 'r', encoding='utf-8')
                lines = file_handle.readlines()
                file_handle.close()

                new_path = root.replace('Days', 'StayPoint', 1) + '\\' + file
                print(new_path)
                destination_handle = codecs.open(new_path, 'w', encoding='utf-8')
                # 存入数组
                for line in lines:
                    temp_p = Point(line)
                    list_temp.append(temp_p)
                # 按照时间对数组排序
                list_temp = sorted(list_temp, key=lambda point: point.date_time)

                i = 0
                # 终止条件
                while i < (len(list_temp) - 1):

                    # 初始化起始点，从i开始
                    stay_point1 = Stay_Points(list_temp[i])
                    j_flag = 0
                    # 控制变量j完全依赖于i
                    for j in range(i + 1, len(list_temp)):
                        # 依次添加节点
                        r, po = stay_point1.add(list_temp[j], destination_handle)
                        # 如果添加失败
                        if r == 'f':
                            i += po
                            # print(stay_point1.o_mean_point())
                            # 每次循环后销毁stay_point1对象
                            j_flag = 1
                            break
                        # 添加成功则继续添加新节点
                    if j_flag == 0:
                        # 如果当前文件全部节点添加成功,即j已到达文件最后一行
                        stay_point1.o_mean_point(destination_handle)
                        break

                del list_temp
