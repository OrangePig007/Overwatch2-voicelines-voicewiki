import argparse
import os
import re
import shutil
from datetime import datetime


# 用旧版本全条件文本作为基准；新版本里同序号会被剔除。
filefolder = 'ow-dmon-ver'
OLD_ALL_TXT = rf'G:\守望语音\{filefolder}\All-260903-所有音频.txt'
NEW_ALL_TXT = rf'G:\守望语音\{filefolder}\All-260903-所有音频.txt'

# 新增条件文本和新增音频输出位置。
date_str = datetime.now().strftime('%y%m%d')
OUTPUT_TXT = rf'G:\守望语音\{filefolder}\All-{date_str}-新增音频.txt'
AUDIO_OUTPUT_FOLDER = rf'G:\守望语音\{filefolder}\new-upload'

# 新版本源音频目录。条件分类以 NEW_ALL_TXT 为准，音频按序号在这里递归查找。
EN_AUDIO_ROOT = rf'G:\守望语音\{filefolder}\EN\HeroVoice'
ZH_AUDIO_ROOT = rf'G:\守望语音\{filefolder}\ZHS\HeroVoice'

error_log_path = rf'G:\守望语音\{filefolder}\new_audio_filter_log.txt'

FILE_RE = re.compile(r'\{\{OW2Audio\|File=([^|}]+)')
SECTION_RE = re.compile(r'^\s*==(.+?)==\s*$')


def normalize_audio_id(file_value):
    """00000002BBE7.0B2|E -> 00000002BBE7.0B2"""
    return file_value.split('|', 1)[0].strip()


def extract_audio_ids(txt_path):
    ids = set()
    with open(txt_path, 'r', encoding='utf-8') as file:
        for line in file:
            match = FILE_RE.search(line)
            if match:
                ids.add(normalize_audio_id(match.group(1)))
    return ids


def get_audio_id(filename):
    return os.path.splitext(filename)[0].split('-', 1)[0]


def build_audio_index(root_path):
    index = {}
    if not os.path.exists(root_path):
        log(f'[目录缺失] 音频根目录不存在: {root_path}')
        return index

    for root, _, files in os.walk(root_path):
        for filename in files:
            if not filename.lower().endswith('.ogg'):
                continue
            audio_id = get_audio_id(filename)
            path = os.path.join(root, filename)
            if audio_id in index:
                log(f'[重复序号] {audio_id} | 保留: {index[audio_id]} | 忽略: {path}')
                continue
            index[audio_id] = path
    return index


def log(message):
    os.makedirs(os.path.dirname(error_log_path), exist_ok=True)
    with open(error_log_path, 'a+', encoding='utf-8') as file:
        file.write(message + '\n')


def copy_audio(audio_id, audio_index, lang):
    src_path = audio_index.get(audio_id)
    if not src_path:
        log(f'[缺少{lang.upper()}音频] {audio_id}')
        return False

    os.makedirs(AUDIO_OUTPUT_FOLDER, exist_ok=True)
    dst_path = os.path.join(AUDIO_OUTPUT_FOLDER, f'{audio_id}_{lang}.ogg')
    if os.path.exists(dst_path):
        log(f'[覆盖] {os.path.basename(dst_path)} 已存在，已覆盖: {src_path}')
    shutil.copy2(src_path, dst_path)
    return True


def filter_new_sections(old_ids, new_all_txt):
    output_lines = []
    new_ids = []
    current_title = None
    current_lines = []

    def flush_section():
        if current_title is None or not current_lines:
            return
        output_lines.append(f'\n\n=={current_title}==\n')
        output_lines.extend(current_lines)

    with open(new_all_txt, 'r', encoding='utf-8') as file:
        for line in file:
            section_match = SECTION_RE.match(line)
            if section_match:
                flush_section()
                current_title = section_match.group(1)
                current_lines = []
                continue

            file_match = FILE_RE.search(line)
            if not file_match:
                continue

            audio_id = normalize_audio_id(file_match.group(1))
            if audio_id in old_ids:
                continue

            current_lines.append(line)
            new_ids.append(audio_id)

    flush_section()
    return output_lines, new_ids


def parse_args():
    parser = argparse.ArgumentParser(
        description='用旧全条件文本的序号过滤新全条件文本，只保留新增条目并复制对应 EN/ZH 音频。'
    )
    parser.add_argument('--old', default=OLD_ALL_TXT, help='旧版本 All-*-所有音频.txt')
    parser.add_argument('--new', default=NEW_ALL_TXT, help='新版本 All-*-所有音频.txt')
    parser.add_argument('--output', default=OUTPUT_TXT, help='新增条件文本输出路径')
    parser.add_argument('--audio-output', default=AUDIO_OUTPUT_FOLDER, help='新增音频输出文件夹')
    parser.add_argument('--en-root', default=EN_AUDIO_ROOT, help='新版本 EN 音频根目录')
    parser.add_argument('--zh-root', default=ZH_AUDIO_ROOT, help='新版本 ZHS 音频根目录')
    return parser.parse_args()


def main():
    global OUTPUT_TXT, AUDIO_OUTPUT_FOLDER, EN_AUDIO_ROOT, ZH_AUDIO_ROOT
    args = parse_args()
    OUTPUT_TXT = args.output
    AUDIO_OUTPUT_FOLDER = args.audio_output
    EN_AUDIO_ROOT = args.en_root
    ZH_AUDIO_ROOT = args.zh_root

    if os.path.exists(error_log_path):
        os.remove(error_log_path)

    old_ids = extract_audio_ids(args.old)
    output_lines, new_ids = filter_new_sections(old_ids, args.new)

    with open(OUTPUT_TXT, 'w', encoding='utf-8') as file:
        file.writelines(output_lines)

    en_index = build_audio_index(EN_AUDIO_ROOT)
    zh_index = build_audio_index(ZH_AUDIO_ROOT)

    copied_en = 0
    copied_zh = 0
    for audio_id in dict.fromkeys(new_ids):
        if copy_audio(audio_id, en_index, 'en'):
            copied_en += 1
        if copy_audio(audio_id, zh_index, 'zh'):
            copied_zh += 1

    print(f'旧序号数量: {len(old_ids)}')
    print(f'新增模板行: {len(new_ids)}')
    print(f'新增唯一序号: {len(set(new_ids))}')
    print(f'输出文本: {OUTPUT_TXT}')
    print(f'音频输出目录: {AUDIO_OUTPUT_FOLDER}')
    print(f'复制 EN: {copied_en}')
    print(f'复制 ZH: {copied_zh}')
    print(f'日志: {error_log_path}')


if __name__ == '__main__':
    main()
