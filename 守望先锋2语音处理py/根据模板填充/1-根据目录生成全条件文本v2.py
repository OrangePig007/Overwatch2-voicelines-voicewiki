import os
import re
import shutil
from datetime import datetime
#这个会把大招文件夹的音频和文件夹都统计

# --- 在这里定义你的过滤关键词 ---
filter_keyword = ''  # 如果想处理所有文件，请设置为 '' 或 None

# 定义一个专门记录错误日志的文件路径
filefolder = 'ow-dmon-ver'
error_log_path = f'G:\\守望语音\\{filefolder}\\missing_paths_log.txt'

# --- 音频复制开关 ---
ENABLE_AUDIO_COPY = True  # True: 复制并重命名到单独文件夹; False: 只生成文本
AUDIO_COPY_FOLDER = f'G:\\守望语音\\{filefolder}\\upload'

hero = 'D.Mon'
hero_zh = 'D.Mon'

date_str = datetime.now().strftime('%y%m%d')
file = f'G:\\守望语音\\{filefolder}\\{hero}-{date_str}-所有音频.txt'
action_zh = f'G:\\守望语音\\{filefolder}\\ZHS\\HeroVoice\\{hero_zh}'
action_en = f'G:\\守望语音\\{filefolder}\\EN\\HeroVoice\\{hero}'

actions = []


def restore_filename_text(text):
    """
    还原文件名里的占位符：
    - `_内容_` 优先视为引号，改回 `“内容”`
    - 剩余单个 `_` 视为问号，改回 `?`
    """
    text = text.replace(")_ ", ") ")
    text = re.sub(r'_(.+?)_', r'“\1”', text)
    return text.replace("_", "?")


def load_first_gen_ids(path):
    """读取第一代序号文件，返回一个 set。"""
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return {line.strip() for line in f if line.strip()}
    except FileNotFoundError:
        with open(error_log_path, 'a+', encoding='utf-8') as err_f:
            err_f.write(f"[缺失] 第一代序号文件不存在: {path}\n")
        return set()


def get_flat_audio_name(filename, lang):
    """把原始文件名转成平铺后的目标名。"""
    base_id = os.path.splitext(filename)[0].split('-', 1)[0]
    return f"{base_id}_{lang}.ogg"


def copy_audio_file(src_path, dst_folder, new_name):
    """复制音频到平铺目录，必要时覆盖同名文件。"""
    os.makedirs(dst_folder, exist_ok=True)
    dst_path = os.path.join(dst_folder, new_name)
    if os.path.exists(dst_path):
        with open(error_log_path, 'a+', encoding='utf-8') as err_f:
            err_f.write(f"[覆盖] {new_name} 已存在，已覆盖: {src_path}\n")
    shutil.copy2(src_path, dst_path)


def save(file_path, hero, action, zh_path, en_path, first=None):
    current_zh_path = os.path.join(zh_path, action)
    current_en_path = os.path.join(en_path, action)
    
    # 1. 检查中文路径是否存在
    if not os.path.exists(current_zh_path):
        with open(error_log_path, 'a+', encoding='utf-8') as err_f:
            err_f.write(f"[目录缺失] {hero} | {action} | 中文路径不存在\n")
        return

    try:
        # 只处理 .ogg 文件，其他后缀全部忽略
        en = sorted([f for f in os.listdir(current_en_path) if f.lower().endswith('.ogg')])
        zh = sorted([f for f in os.listdir(current_zh_path) if f.lower().endswith('.ogg')])
        
        # 如果过滤后该文件夹为空，记录一下并跳过
        if not en:
            with open(error_log_path, 'a+', encoding='utf-8') as err_f:
                err_f.write(f"[跳过] {action} | 文件夹内无有效 .ogg 文件\n")
            return

        if len(en) != len(zh):
            with open(error_log_path, 'a+', encoding='utf-8') as err_f:
                err_f.write(
                    f"[数量不一致] {hero} | {action} | EN={len(en)} | ZH={len(zh)}\n"
                )

        print(f"正在处理: {action}")

        with open(file_path, 'a+', encoding='utf-8') as f:
            action_title = f'{hero}\\{action}' if action else hero
            f.write(f'\n\n=={action_title}==\n')
            
            # 使用 zip 对齐处理，注意：如果中英文数量不一致，zip 会以短的为准
            for e, z in zip(en, zh):
                # 提取英文文本逻辑
                # 这里只去掉 .ogg 扩展名，.0B2 仍然保留在文件名主体里
                _e = os.path.splitext(e)[0].split('-', 1)[-1]
                if _e != '':
                    _en1 = _e[-1]
                    __en1 = _e[0:-1]
                    if _en1 == '_': _e = __en1 + '?'
                    elif _en1 == '!': _e = __en1 + '!'
                    elif _en1 == ')': _e = _e
                    else: _e = _e + '.'
                else:
                    _e = '...'
                _e = restore_filename_text(_e)
                
                # 提取文件 ID (前16位)
                fi = e[0:16]
                if first and fi in first:
                    fi += '|E'
                
                # 处理中文文本
                _z = os.path.splitext(z)[0].split('-', 1)
                _z0 = _z[1] if len(_z) > 1 else ""
                _z1 = restore_filename_text(_z0.replace("（", "(").replace("）：", ")").replace("）", ")"))
                
                # 写入 Wiki 模板
                if _e != '':
                    f.write(f'{{{{OW2Audio|File={fi}|en={_e}|zh={_z1}}}}}\n')
                else:
                    f.write(f'{{{{OW2Audio|File={fi}}}}}\n')

                if ENABLE_AUDIO_COPY:
                    copy_audio_file(
                        os.path.join(current_en_path, e),
                        AUDIO_COPY_FOLDER,
                        get_flat_audio_name(e, 'en')
                    )
                    copy_audio_file(
                        os.path.join(current_zh_path, z),
                        AUDIO_COPY_FOLDER,
                        get_flat_audio_name(z, 'zh')
                    )
                    
    except Exception as err:
        with open(error_log_path, 'a+', encoding='utf-8') as err_f:
            err_f.write(f"[运行报错] {action} | 错误信息: {str(err)}\n")


def collect_actions(directory, actions, base_path):
    # 只递归目录；如果目录里有 .ogg 文件，就把这个目录记为一个 action
    has_audio = False
    try:
        with os.scandir(directory) as entries:
            subdirs = []
            for entry in entries:
                if entry.is_file() and entry.name.lower().endswith('.ogg'):
                    has_audio = True
                elif entry.is_dir():
                    subdirs.append(entry.path)
    except FileNotFoundError:
        return

    if has_audio:
        relative_path = os.path.relpath(directory, base_path)
        if relative_path == '.':
            relative_path = ''
        actions.append(relative_path)

    for sub_path in subdirs:
        collect_actions(sub_path, actions, base_path)

collect_actions(action_en, actions, action_en)

actions.sort()
print(actions)
with open(file, 'w', encoding='utf-8'):
    pass

if ENABLE_AUDIO_COPY:
    os.makedirs(AUDIO_COPY_FOLDER, exist_ok=True)

first_gen = load_first_gen_ids(r'守望先锋2语音处理py\根据模板填充\守望先锋1代所有语音序号.txt')

for action in actions:
    # 增加过滤逻辑：如果关键词不为空且路径中不包含关键词，则跳过
    if filter_keyword and filter_keyword not in action:
        continue
        
    save(file, hero, action, action_zh, action_en, first_gen)
