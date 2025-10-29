import os
import shutil

#用于整理对话

def delete_folders_from_txt(txt_file, folder_path):
    # 读取txt文件中的字符串序列
    with open(txt_file, 'r') as f:
        characters_to_delete = f.readlines()
    
    # 清理字符串序列中的空白符和换行符
    characters_to_delete = [char.strip() for char in characters_to_delete]
    
    # 遍历文件夹中的文件夹
    for root, dirs, files in os.walk(folder_path, topdown=False):
        for folder in dirs:
            # 检查文件夹名是否包含要删除的字符
            if any(char in folder for char in characters_to_delete):
                folder_path_to_delete = os.path.join(root, folder)
                print("Deleting folder:", folder_path_to_delete)
                # 删除文件夹及其内容
                try:
                    shutil.rmtree(folder_path_to_delete)
                except OSError as e:
                    print(f"Error: {folder_path_to_delete} : {e.strerror}")

# 指定txt文件路径和要清理的文件夹路径
txt_file_path = r'守望先锋2语音处理py\新的语音更新处理方法\all-conv-num-240426.txt'
folder_to_delete_path = r'D:\ow-240826\对话(zh)'

# 调用函数删除文件夹
delete_folders_from_txt(txt_file_path, folder_to_delete_path)
