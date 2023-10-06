import os
import shutil

def process_folder(folder_path, target_folder, lang):
    for root, dirs, files in os.walk(folder_path):
        for filename in files:
            if filename.endswith('.ogg'):
                file_parts = filename.split('-')
                if len(file_parts) >= 3:
                    new_filename = f"{file_parts[2]}_{lang}.ogg"
                    src_path = os.path.join(root, filename)
                    dest_path = os.path.join(target_folder, new_filename)
                    shutil.copy(src_path, dest_path)

# 源文件夹路径
action_en = 'F:/守望先锋语音/对话(en)'
action_zh = 'F:/守望先锋语音/对话(zh)'

# 目标文件夹路径
target_folder = 'F:/待上传/'

# 处理 action_en 文件夹
process_folder(action_en, target_folder, 'en')

# 处理 action_zh 文件夹
process_folder(action_zh, target_folder, 'zh')
