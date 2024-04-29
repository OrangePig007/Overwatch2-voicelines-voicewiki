import os
import shutil

# 源文件夹和目标文件夹的路径
source_folder = "F:/QQ文件/试验2/missing_folder"
target_folder = "F:/QQ文件/试验2/miss-en"

# 读取文件名列表
file_list_file = "F:/QQ文件/试验2/1.txt"
output_file = "F:/QQ文件/试验2/not_found.txt"

# 打开txt文件并读取文件名列表
with open(file_list_file, "r") as f:
    file_name_prefixes = f.read().splitlines()

# 用于记录未找到的文件名
not_found_files = []

# 创建源文件夹中的文件字典
file_dict = {}
for root, dirs, files in os.walk(source_folder):
    for file in files:
        file_dict[file[:16]] = os.path.join(root, file)

# 遍历文件名前16位列表，并复制文件到目标文件夹
for prefix in file_name_prefixes:
    source_path = file_dict.get(prefix)
    if source_path:
        target_path = os.path.join(target_folder, os.path.basename(source_path))
        shutil.copy(source_path, target_path)
        print(f"复制文件: {os.path.basename(source_path)}")
    else:
        not_found_files.append(prefix)

# 将未找到的文件名写入not_found.txt文件
with open(output_file, "w") as f:
    for file_name in not_found_files:
        f.write(file_name + "\n")

print("复制完成")
