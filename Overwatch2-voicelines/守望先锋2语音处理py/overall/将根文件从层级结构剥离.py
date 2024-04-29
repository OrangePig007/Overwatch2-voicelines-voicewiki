import os
import shutil


def flat_copy(source_path, target_path):
    """
    This function copies all the files into a target directory.
    """
    for file in os.listdir(source_path):
        path = os.path.join(source_path, file)
        if os.path.isfile(path):
            shutil.copy(path, target_path)
        else:
            flat_copy(path, target_path)


s_path = input("请输入原始文件夹路径: ")
t_path = input("请输入目标文件夹路径: ")
if not os.path.exists(t_path):
    os.mkdir(t_path)
flat_copy(s_path, t_path)
print("复制完成")


