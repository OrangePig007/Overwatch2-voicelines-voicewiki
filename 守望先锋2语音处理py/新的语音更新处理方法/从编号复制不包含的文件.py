import os
import shutil

# 输入文件夹目录
source_folder = r'F:\守望先锋语音整理\ow-240426\ZH'

# 输出文件夹目录
destination_folder = r'F:\守望先锋语音整理\ow-240426\new-vo\ZH'

# 从文本文件中读取要排除的编号
exclude_numbers_file = r'F:\守望先锋语音整理\ow-240426\all-vo-num-240426.txt'
with open(exclude_numbers_file, 'r') as file:
    exclude_numbers = [line.strip() for line in file]

# 遍历源文件夹
for root, dirs, files in os.walk(source_folder):
    for file in files:
        file_path = os.path.join(root, file)
        
        # 检查文件名是否包含排除的编号
        if not any(number in file for number in exclude_numbers):
            # 构建目标文件夹中的相对路径
            relative_path = os.path.relpath(file_path, source_folder)
            destination_path = os.path.join(destination_folder, relative_path)
            
            # 确保目标文件夹存在
            os.makedirs(os.path.dirname(destination_path), exist_ok=True)
            
            # 复制文件到目标文件夹
            shutil.copy(file_path, destination_path)

print("复制完成")