import tifffile as tiff
import numpy as np
import pandas as pd
import os
import imageio

"""
该部分用qupath得到的TMA数据和ometiff图像数据得到切分的数据块，总共10个通道，单个芯片的尺寸定为8000*8000，项目FISH
"""
# 读取 TMA.txt 文件
tma_data = pd.read_csv('TMA.txt', delimiter='\t')
tmaspot_size_px = 8000  ## 7800 定义图像块的大小，单位：像素
pixel_size = 0.4418  ## 每个像素的长度，单位，微米
# 创建输出文件夹
output_folder = "output"
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# 读取 OME-TIFF 文件
with tiff.TiffFile('HX mIF&FISH_2023582032.ome.tiff') as ome_tiff:
    image_stack = ome_tiff.asarray()  # 读取整个图像堆栈
    for index, row in tma_data.iterrows():
        label = row['Name']
        x_um = float(row['Centroid X µm'])  # 中心坐标X（微米）
        y_um = float(row['Centroid Y µm'])  # 中心坐标Y（微米）
        if not row['Missing']:  # 如果图像块不是缺失的
            x_px = int(x_um / pixel_size)  # 将中心坐标X从微米转换为像素
            y_px = int(y_um / pixel_size)  # 将中心坐标Y从微米转换为像素
            x_start, y_start = max(0, x_px - tmaspot_size_px // 2), max(0, y_px - tmaspot_size_px // 2)  # 确定读取区域的坐标范围，因为如果执行切分我们的电脑内存无法满足将整个数组展开。
            x_end, y_end = min(image_stack.shape[2], x_px + tmaspot_size_px // 2), min(image_stack.shape[1],
                                                                                       y_px + tmaspot_size_px // 2)
            # 提取图像块
            tmaspot = image_stack[:, y_start:y_end, x_start:x_end]  # 包含10个通道的图像块
            # 创建以label命名(也就是TMA中的组名)的子文件夹
            folder_path = os.path.join(output_folder, label)
            if not os.path.exists(folder_path):
                os.makedirs(folder_path)
            # 逐个通道保存为PNG图片
            for i in range(10):
                channel_image = tmaspot[i, :, :]
                filename = os.path.join(folder_path, f"{label}_c{i + 1}.jpg")
                imageio.imwrite(filename, channel_image)



# import tifffile as tiff
# import numpy as np
# import pandas as pd
# import imageio
# import os
# from PIL import Image

# """
# 该部分用qupath得到的TMA数据和qptiff图像数据得到切分的数据块，每场图片的尺寸为4000*4000，用于项目C7
# """
# # 读取 TMA.txt 文件
# tma_data = pd.read_csv('tma.txt', delimiter='\t')
# tmaspot_size_px = 4000  # 定义图像块的大小，单位：像素
# pixel_size = 0.4974  # 每个像素的长度，单位，微米
# # 创建输出文件夹
# output_folder = "output"
# if not os.path.exists(output_folder):
#     os.makedirs(output_folder)

# # 读取 OME-TIFF 文件
# with tiff.TiffFile('C7-LHC_Scan1.qptiff') as tiff:
#     image_stack = tiff.asarray()  # 读取整个图像堆栈
#     for index, row in tma_data.iterrows():
#         label = row['Name']
#         x_um = float(row['Centroid X µm'])  # 中心坐标X（微米）
#         y_um = float(row['Centroid Y µm'])  # 中心坐标Y（微米）
#         if not row['Missing']:  # 如果图像块不是缺失的
#             x_px = int(x_um / pixel_size)  # 将中心坐标X从微米转换为像素
#             y_px = int(y_um / pixel_size)  # 将中心坐标Y从微米转换为像素
#             x_start, y_start = max(0, x_px - tmaspot_size_px // 2), max(0, y_px - tmaspot_size_px // 2)
#             x_end, y_end = min(image_stack.shape[2], x_px + tmaspot_size_px // 2), min(image_stack.shape[1],
#                                                                                        y_px + tmaspot_size_px // 2)
#             # 提取图像块
#             tmaspot = image_stack[:, y_start:y_end, x_start:x_end]  # 包含10个通道的图像块
#             # 创建以label命名的子文件夹
#             folder_path = os.path.join(output_folder, label)
#             if not os.path.exists(folder_path):
#                 os.makedirs(folder_path)
#             # 逐个通道保存为PNG图片
#             for i in range(8):
#                 channel_image = tmaspot[i, :, :]
#                 filename = os.path.join(folder_path, f"C{i + 1}.png")
#                 imageio.imwrite(filename, channel_image)


# # 把文件夹中尺寸不足tmaspot_size_px的图片都进行填充
# for subdir in os.listdir(output_folder):
#     subdir_path = os.path.join(output_folder, subdir)
#     if os.path.isdir(subdir_path):
#         # 遍历子文件夹中的所有png图片
#         for file in os.listdir(subdir_path):
#             if file.endswith(".png"):
#                 file_path = os.path.join(subdir_path, file)
#                 with Image.open(file_path) as img:
#                     # 检查图片尺寸
#                     if img.size[0] < tmaspot_size_px or img.size[1] < tmaspot_size_px:
#                         # 创建一个新的背景图，颜色为黑色
#                         new_img = Image.new("L", (tmaspot_size_px, tmaspot_size_px), (0))
#                         # 将原始图片粘贴到背景图中心
#                         new_img.paste(img, ((tmaspot_size_px - img.size[0]) // 2, (tmaspot_size_px - img.size[1]) // 2))
#                         # 保存修改后的图片
#                         new_img.save(file_path)
