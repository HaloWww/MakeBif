#!/usr/bin/python
import os
import struct
import array
import argparse


parser = argparse.ArgumentParser(description = 'this is a description')
parser.add_argument("--name", "-n")
parser.add_argument("--dir", "-d")
args = parser.parse_args()

def makeBIF(filename, directory):
    interval = 10
    # BIF 文件头部魔数和版本号
    magic = [0x89, 0x42, 0x49, 0x46, 0x0d, 0x0a, 0x1a, 0x0a]
    version = 0

    # 获取目录中的所有图片文件
    files = os.listdir(directory)
    # print(files)
    images = [image for image in files if image.lower().endswith(('.jpg', '.jpeg', '.png', '.bmp'))]
    images.sort()

    # 创建 BIF 文件
    with open(filename, "wb") as f:
        array.array('B', magic).tofile(f)  # 写入魔数
        f.write(struct.pack("<I", version))  # 写入版本号
        f.write(struct.pack("<I", len(images)))  # 写入图片数量
        f.write(struct.pack("<I", 1000 * int(interval)))  # 写入时间间隔（以毫秒为单位）
        array.array('B', [0x00 for _ in range(20, 64)]).tofile(f)  # 保留区域填充

        bifTableSize = 8 + (8 * len(images))
        imageIndex = 64 + bifTableSize
        timestamp = 0

        # 写入图片索引和时间戳
        for image in images:
            statinfo = os.stat(os.path.join(directory, image))
            f.write(struct.pack("<I", timestamp))
            f.write(struct.pack("<I", imageIndex))

            timestamp += 1
            imageIndex += statinfo.st_size

        f.write(struct.pack("<I", 0xffffffff))
        f.write(struct.pack("<I", imageIndex))

        # 写入图片数据
        for image in images:
            with open(os.path.join(directory, image), "rb") as image_file:
                data = image_file.read()
                f.write(data)

# 示例用法
makeBIF(args.name, args.dir)
