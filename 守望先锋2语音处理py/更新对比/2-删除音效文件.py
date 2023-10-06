import os

def delete_files_with_length(folder_path, length):
    try:
        for filename in os.listdir(folder_path):
            file_path = os.path.join(folder_path, filename)
            if os.path.isfile(file_path):
                # 获取不带扩展名的文件名
                file_name, _ = os.path.splitext(filename)
                if len(file_name) == length:
                    os.remove(file_path)
                    print(f"Deleted file: {filename}")
    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    folder_path = "F:\QQ文件\试验2\missing_folder"  # 替换为你的文件夹路径
    length_to_delete = 16  # 指定要删除的文件名长度

    delete_files_with_length(folder_path, length_to_delete)
