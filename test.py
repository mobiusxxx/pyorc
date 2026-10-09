'''
Author: xiafanli xiafanli@eccom.com.cn
Date: 2024-05-29 16:21:43
Description: 
'''
# '''
# Author: xiafanli xiafanli@eccom.com.cn
# Date: 2024-05-29 16:21:43
# Description: im
# '''
import pyorc
import numpy as np
from shapely.geometry import Polygon
import matplotlib.pyplot as plt
import time
# set a video filename below, change to your own local file location
video_file = r"H:\video\KLT-IV\Feshie\Feshie\UAS\Flight01_1430_1.518m\DJI_0002.MOV"
# video_file = r"H:/Standard calibration/velocity0-1/noTracerWithDark2/C1-2/velocity0-1_noTracerWithDark2_C1-2_merge.mp4"
def read_gcp(file_path):
    '''
    读取gcp文件
    '''
    gcps = dict()
    with open(file_path, 'r') as f:
        data = f.readlines()
    data = [i.strip('\n') for i in data]
    data = [i.split('\t') for i in data]
    data = data[3:]  # 去掉前三行
    # 前三列为世界坐标，后两列为像素坐标
    gcps['src'] = [[float(i[3]), float(i[4])] for i in data]
    gcps['dst'] = [[float(i[0]), float(i[1]), float(i[2])] for i in data]

    return gcps
# gcps_path = r"H:/hehai_ex/Standard calibration/GRP/C1-2_ADD_GRP.dat"
gcps_path = r"H:\video\KLT-IV\Feshie\Feshie\UAS\Flight01_1430_1.518m\GCP.txt"
gcps = read_gcp(gcps_path)
gcps["z_0"] = 0.0

# point to a file containing the camera configuration
cam_config = pyorc.CameraConfig(height=2160, width=4096, gcps=gcps,resolution=0.003)
# corners = [[45, 386], [1219, 416], [1233, 512], [24, 475]]
corners =  [[0, 0], [4096, 0], [4096, 2160], [0, 2160]]
# corners = [[522, 466], [1105, 419], [1019, 1349], [240, 1286]]
cam_config.set_bbox_from_corners(corners)
video = pyorc.Video(
    video_file,
    camera_config=cam_config,
    start_frame=0,
    end_frame=10,
    stabilize=None,
    h_a=0.0,
)
time1 = time.time()
# let's retrieve rgb frames
da_rgb = video.get_frames(method="rgb")
# now reproject

da_proj = da_rgb.frames.project()
time2 = time.time()
print("project time:", time2-time1)

# and plot!
quad_mesh = da_proj[0].frames.plot()
# show the plot
plt.show()
# # save the plot
# plt.savefig("output_Feshie_r0.05_z500.png")




# import json

# #读取json文件
# def read_json_file(file_path):
#     data = {}
#     with open(file_path, 'r') as f:
#         for line in f:
#             data.update(json.loads(line))
#     return data

# data = read_json_file(r"H:\Standard calibration\velocity0-1\noTracerWithDark2\C1-1\middle_result\velocity0-1_noTracerWithDark2_C1-1_standard.json")
# print(data)