import os

# --- 配置区域 ---
# 请确保这两个路径指向对应的 EN 和 ZH 根目录
EN_ROOT = r'G:\守望语音\ow-domina-ver\upload\EN\BetterHeroVoice\Jetpack Cat' 
ZH_ROOT = r'G:\守望语音\ow-domina-ver\upload\ZH\BetterHeroVoice\Jetpack Cat' 
OUTPUT_FILE = r'G:\守望语音\ow-domina-ver\cat_list4.txt'
# ---------------


def process_en_text(_e):
    """ 处理英文文本的特殊逻辑 """
    if _e and _e.strip():
        _en1 = _e[-1]
        __en1 = _e[0:-1]
        if _en1 == '_': 
            _e = __en1 + '?'
        elif _en1 == '!': 
            _e = __en1 + '!'
        else: 
            _e = _e + '.'
    else:
        _e = '...'
    
    _e = _e.replace(")_ ", ") ")
    _e = _e.replace("_", "?")
    return _e

def process_zh_text(_z):
    """ 处理中文文本，转换全角括号 """
    if not _z:
        return ""
    # 替换 （ 为 (，）：和 ） 为 )
    _z1 = _z.replace("（", "(").replace("）：", ")").replace("）", ")")
    return _z1

def build_zh_index(zh_path):
    index = {}
    print("正在扫描中文目录索引...")
    for root, dirs, files in os.walk(zh_path):
        for f in files:
            if f.endswith('.ogg'):
                file_id = f.replace('.ogg', '')
                index[file_id] = os.path.basename(root)
    return index

def organize_audio():
    zh_index = build_zh_index(ZH_ROOT)
    results = {}

    print("正在处理英文目录并清理路径...")
    for root, dirs, files in os.walk(EN_ROOT):
        audio_files = [f for f in files if f.endswith('.03F.ogg') or f.endswith('.0B2.ogg')]
        
        if audio_files:
            # --- 处理标题：去掉最末尾的字幕文件夹 ---
            # 原路径: Jetpack Cat\Armor\(cat sounds)
            # 目标路径: Jetpack Cat\Armor
            parent_dir = os.path.dirname(root)
            rel_path = os.path.relpath(parent_dir, os.path.dirname(EN_ROOT))
            condition_key = rel_path.replace('/', '\\')
            
            # 原始文件夹名作为处理前的文本
            raw_en = os.path.basename(root)
            
            if condition_key not in results:
                results[condition_key] = []
            
            for filename in audio_files:
                file_id = filename.replace('.ogg', '')
                
                # 获取原始中文描述
                raw_zh = zh_index.get(file_id, "")
                
                # --- 应用你提供的处理逻辑 ---
                final_en = process_en_text(raw_en)
                final_zh = process_zh_text(raw_zh)
                
                entry = f"{{{{OW2Audio|File={file_id}|en={final_en}|zh={final_zh}}}}}"
                results[condition_key].append(entry)

    # 写入文件
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        for condition in sorted(results.keys()):
            f.write(f"=={condition}==\n")
            # 内部按照 ID 排序，保证同组内有序
            for item in sorted(results[condition]):
                f.write(item + "\n")
            f.write("\n")

if __name__ == "__main__":
    if not os.path.exists(EN_ROOT):
        print("错误：请检查 EN_ROOT 路径")
    else:
        organize_audio()
        print(f"处理完成！生成文件: {OUTPUT_FILE}")