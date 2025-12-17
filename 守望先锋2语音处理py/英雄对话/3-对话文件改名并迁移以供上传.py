import os
import shutil

def process_folder(folder_path, target_folder, lang):
    for root, dirs, files in os.walk(folder_path):
        for filename in files:
            if filename.endswith('.ogg'):
                file_parts = filename.split('.0B2-')
                if len(file_parts) >= 2:
                    new_filename = f"{file_parts[0]}.0B2_{lang}.ogg"
                    src_path = os.path.join(root, filename)
                    dest_path = os.path.join(target_folder, new_filename)
                    shutil.copy(src_path, dest_path)

# 源文件夹路径
action_zh = 'G:\守望语音\ow-lupa-ver\ZHS\BetterHeroVoice\斩仇'
action_en = 'G:\守望语音\ow-lupa-ver\EN\BetterHeroVoice\Vendetta'

# 目标文件夹路径
target_folder = 'G:\守望语音\ow-lupa-ver\待上传'

# 处理 action_en 文件夹
process_folder(action_en, target_folder, 'en')

# 处理 action_zh 文件夹
process_folder(action_zh, target_folder, 'zh')
