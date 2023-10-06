import os
import shutil

def compare_folders(folder1_path, folder2_path, extra_folder, missing_folder):
    folder1_files = set()
    folder2_files = set()

    for root, _, files in os.walk(folder1_path):
        for file in files:
            folder1_files.add(file[:16])  # 只保留根文件名的前16个字符

    for root, _, files in os.walk(folder2_path):
        for file in files:
            folder2_files.add(file[:16])  # 只保留根文件名的前16个字符

    extra_files = folder1_files - folder2_files
    missing_files = folder2_files - folder1_files

    with open('F:/QQ文件/试验2/extra_files.txt', 'w+', encoding='utf-8') as extra_file_list:
        extra_file_list.write('\n'.join(extra_files))

    with open('F:/QQ文件/试验2/missing_files.txt', 'w+', encoding='utf-8') as missing_file_list:
        missing_file_list.write('\n'.join(missing_files))

    for root, _, files in os.walk(folder1_path):
        for file in files:
            if file[:16] in extra_files:
                src_file = os.path.join(root, file)
                dst_file = os.path.join(extra_folder, file)
                os.makedirs(os.path.dirname(dst_file), exist_ok=True)
                shutil.copy(src_file, dst_file)

    for root, _, files in os.walk(folder2_path):
        for file in files:
            if file[:16] in missing_files:
                src_file = os.path.join(root, file)
                dst_file = os.path.join(missing_folder, file)
                os.makedirs(os.path.dirname(dst_file), exist_ok=True)
                shutil.copy(src_file, dst_file)

# 定义两个文件夹的路径和保存多出和缺少的文件的文件夹路径
folder1_path = 'E:/视频/素材-守望先锋/守望先锋语音提取/20221104/EN'
folder2_path = 'F:/守望先锋语音/EN'
extra_folder = 'F:/QQ文件/试验2/extra_folder'
missing_folder = 'F:/QQ文件/试验2/missing_folder'

compare_folders(folder1_path, folder2_path, extra_folder, missing_folder)
