用于处理大型医学图像数据：
使用 QUPATH 和 PYTHON 对组织微阵列 （TMA） 进行脱组，得到一张张单个图像

步骤：首先使用qupath打开图像，使用TMA解阵列工具提取每个微点
      其次通过measure导出含有每个微店坐标位置、是否缺少等信息的txt文件
      最后使用python读取txt文件和ometiff图像，将图像转换为多维数组进行读取和切割，保存每个微店的图片

存在问题：图片过大无法读取，此时需要win11设置-查找-高级设置-性能选项-虚拟内存-选自定义大小-按C盘剩余空间选择尽可能大虚拟内存
          使用qupath进行组织微阵列脱组时可能会因为背景原因无法识别，则需要手动设置框选微点
