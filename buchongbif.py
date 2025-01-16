import os
import subprocess
import re
import shutil

def list_video_files(directory):
    video_extensions = ['.mp4', '.avi', '.mkv', '.mov', '.wmv', '.ts']

    for root, dirs, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            if any(file_path.lower().endswith(ext) for ext in video_extensions):
                print(file_path)
                file_name = os.path.splitext(file)[0]
                print(file_name)

                # 处理文件名中的特殊字符
                safe_file_name = re.sub(r'[^\w\s\-]', '_', file_name)
                tempdir = f"/home/temp/{safe_file_name}temp"
                bifname = safe_file_name + "-320-10.bif"
                biffilepath = os.path.join(root, bifname)

                if os.path.isfile(biffilepath):
                    print("已经存在bif，跳过")
                else:
                    print("不存在bif，开始创建")
                    os.makedirs(tempdir, exist_ok=True)

                    # 调用 ffmpeg
                    mkffmpeg = [
                        "ffmpeg",
                        "-i", file_path,
                        "-r", "0.1",
                        "-threads", "16",
                        "-an",
                        "-sn",
                        "-vf", "scale=w=640:h=-1,format=p010",
                        "-f", "image2",
                        f"{tempdir}/img_%05d.jpg"
                    ]
                    try:
                        subprocess.run(mkffmpeg, check=True)
                    except subprocess.CalledProcessError as e:
                        print(f"运行 ffmpeg 时出错：{e}")
                        continue

                    # 调用 makebif 脚本
                    makebif_cmd = [
                        "python3", "/root/makebif/makebif.py",
                        "-n", bifname,
                        "-d", tempdir
                    ]
                    try:
                        subprocess.run(makebif_cmd, check=True)
                    except subprocess.CalledProcessError as e:
                        print(f"运行 makebif 时出错：{e}")
                        continue

                    # 清理临时目录并移动 BIF 文件
                    shutil.rmtree(tempdir)
                    shutil.move(f"/root/makebif/{bifname}", root)

# 指定目录
directory_to_search = "/home/auto/"

# 遍历目录并处理视频文件
list_video_files(directory_to_search)
