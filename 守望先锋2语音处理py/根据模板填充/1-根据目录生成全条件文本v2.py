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

hero = 'All'
hero_zh = 'All'

date_str = datetime.now().strftime('%y%m%d')
file = f'G:\\守望语音\\{filefolder}\\{hero}-{date_str}-所有音频.txt'
zh_root = f'G:\\守望语音\\{filefolder}\\ZHS'
en_hero_root = f'G:\\守望语音\\{filefolder}\\EN\\HeroVoice'
zh_hero_root = f'G:\\守望语音\\{filefolder}\\ZHS\\HeroVoice'
action_en = os.path.join(en_hero_root, hero)
if hero in ('', 'All') or not os.path.exists(action_en):
    action_en = en_hero_root

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
    base_id = get_audio_id(filename)
    return f"{base_id}_{lang}.ogg"


def get_audio_id(filename):
    """提取音频序号：000000020019.0B2-台词.ogg -> 000000020019.0B2。"""
    return os.path.splitext(filename)[0].split('-', 1)[0]


def get_caption(filename):
    """提取文件名横线后的字幕部分。"""
    parts = os.path.splitext(filename)[0].split('-', 1)
    return parts[1] if len(parts) > 1 else ""


def copy_audio_file(src_path, dst_folder, new_name):
    """复制音频到平铺目录，必要时覆盖同名文件。"""
    os.makedirs(dst_folder, exist_ok=True)
    dst_path = os.path.join(dst_folder, new_name)
    if os.path.exists(dst_path):
        with open(error_log_path, 'a+', encoding='utf-8') as err_f:
            err_f.write(f"[覆盖] {new_name} 已存在，已覆盖: {src_path}\n")
    shutil.copy2(src_path, dst_path)


def build_audio_index(root_path):
    """递归建立 序号 -> 文件路径 索引；中文按序号匹配，不依赖条件目录。"""
    index = {}
    if not os.path.exists(root_path):
        with open(error_log_path, 'a+', encoding='utf-8') as err_f:
            err_f.write(f"[目录缺失] ZH 索引根目录不存在: {root_path}\n")
        return index

    for root, _, files in os.walk(root_path):
        for filename in files:
            if not filename.lower().endswith('.ogg'):
                continue
            file_id = get_audio_id(filename)
            src_path = os.path.join(root, filename)
            if file_id in index:
                with open(error_log_path, 'a+', encoding='utf-8') as err_f:
                    err_f.write(
                        f"[重复序号] {file_id} | 保留: {index[file_id]} | 忽略: {src_path}\n"
                    )
                continue
            index[file_id] = src_path
    return index


def save(file_path, hero, action, zh_index, en_path, first=None):
    current_en_path = os.path.join(en_path, action)

    try:
        # 只处理 .ogg 文件，其他后缀全部忽略
        en = sorted([f for f in os.listdir(current_en_path) if f.lower().endswith('.ogg')])
        
        # 如果过滤后该文件夹为空，记录一下并跳过
        if not en:
            with open(error_log_path, 'a+', encoding='utf-8') as err_f:
                err_f.write(f"[跳过] {action} | 文件夹内无有效 .ogg 文件\n")
            return

        print(f"正在处理: {action}")

        with open(file_path, 'a+', encoding='utf-8') as f:
            action_title = f'{hero}\\{action}' if action else hero
            f.write(f'\n\n=={action_title}==\n')
            
            # 条件分类和排序完全以 EN 目录为准；ZH 递归按同序号匹配。
            for e in en:
                # 提取英文文本逻辑
                # 这里只去掉 .ogg 扩展名，.0B2 仍然保留在文件名主体里
                _e = get_caption(e)
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
                fi = get_audio_id(e)
                if first and fi in first:
                    fi += '|E'
                
                # 处理中文文本
                zh_src_path = zh_index.get(get_audio_id(e))
                if zh_src_path:
                    z = os.path.basename(zh_src_path)
                    _z0 = get_caption(z)
                    _z1 = restore_filename_text(_z0.replace("（", "(").replace("）：", ")").replace("）", ")"))
                else:
                    _z1 = ""
                    with open(error_log_path, 'a+', encoding='utf-8') as err_f:
                        err_f.write(f"[缺少中文] {hero} | {action} | {get_audio_id(e)} | {e}\n")
                
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
                    if zh_src_path:
                        copy_audio_file(
                            zh_src_path,
                            AUDIO_COPY_FOLDER,
                            get_flat_audio_name(os.path.basename(zh_src_path), 'zh')
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
zh_index = build_audio_index(zh_hero_root if os.path.exists(zh_hero_root) else zh_root)

for action in actions:
    # 增加过滤逻辑：如果关键词不为空且路径中不包含关键词，则跳过
    if filter_keyword and filter_keyword not in action:
        continue
        
    save(file, hero, action, zh_index, action_en, first_gen)
