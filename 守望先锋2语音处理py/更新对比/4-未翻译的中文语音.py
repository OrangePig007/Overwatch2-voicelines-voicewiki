import os
import re

# 指定文件夹路径
folder_path = 'F:/QQ文件/试验2/miss-zh'

# 获取文件夹中的所有文件名
file_names = os.listdir(folder_path)

# 筛选不含中文字符的文件名
non_chinese_file_names = []

for file_name in file_names:
    # 使用正则表达式检查文件名是否包含中文字符
    if not re.search('[\u4e00-\u9fa5]', file_name):
        non_chinese_file_names.append(file_name)

# 删除不含中文字符的文件
for file_name in non_chinese_file_names:
    file_path = os.path.join(folder_path, file_name)
    os.remove(file_path)
    print(f"已删除文件: {file_path}")

print("文件删除完成")
