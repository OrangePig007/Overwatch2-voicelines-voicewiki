import os
import re
import pandas as pd  # 需要安装: pip install pandas openpyxl

# ================= 配置区域 =================
DATA_DIR = r"G:\守望语音\ow-domina-ver\本地化文本" 
INPUT_FILE = r"G:\守望语音\ow-domina-ver\names.txt"  # 你的名字列表文件
OUTPUT_FILE = r"G:\守望语音\ow-domina-ver\localization_results.xlsx"

LANG_ORDER = [
    "EN", "ZHS", "ZHT", "JA", "KO", "RU", "FR", "DE", 
    "ESEU", "ESLA", "PT", "IT", "PL"
]

FILES = {
    "EN": "strings-en.txt", "ZHS": "strings-zhs.txt", "ZHT": "strings-zht.txt",
    "JA": "strings-ja.txt", "KO": "strings-ko.txt", "RU": "strings-ru.txt",
    "FR": "strings-fr.txt", "DE": "strings-de.txt", "ESEU": "strings-eseu.txt",
    "ESLA": "strings-esla.txt", "PT": "strings-pt.txt", "IT": "strings-it.txt",
    "PL": "strings-pl.txt"
}
# ============================================

def load_data():
    id_map = {}
    # 结构: { 'ID': { 'EN': '...', 'ZHS': '...' } }
    pattern = re.compile(r"^([0-9A-F]{12}\.07C):\s*(.*)$")

    print("正在预处理 13 国语言数据...")
    for lang_key, filename in FILES.items():
        path = os.path.join(DATA_DIR, filename)
        if not os.path.exists(path):
            continue
            
        with open(path, 'r', encoding='utf-8', errors='ignore') as f:
            current_id = None
            current_content = []
            for line in f:
                line_str = line.rstrip('\n')
                match = pattern.match(line_str)
                if match:
                    if current_id:
                        id_map[current_id][lang_key] = "\n".join(current_content)
                    current_id, first_part = match.groups()
                    if current_id not in id_map: id_map[current_id] = {}
                    current_content = [first_part]
                else:
                    if current_id: current_content.append(line_str)
            if current_id:
                id_map[current_id][lang_key] = "\n".join(current_content)
    return id_map

def export_to_excel():
    id_map = load_data()
    
    # 1. 读取你需要查询的名字列表
    if not os.path.exists(INPUT_FILE):
        print(f"错误：找不到输入文件 {INPUT_FILE}")
        return
    
    with open(INPUT_FILE, 'r', encoding='utf-8') as f:
        queries = [line.strip() for line in f if line.strip()]

    final_rows = []
    found_ids = set()

    print(f"正在匹配关键词并整理表格...")
    
    # 2. 遍历查询词
    for q in queries:
        q_lower = q.lower()
        # 在 id_map 中搜索（这里默认在所有语言中搜索，或者你可以指定只在 EN 或 ZHS 中搜）
        for sid, langs in id_map.items():
            # 只要任意一种语言包含了关键词，就记录该 ID
            match_found = False
            for text in langs.values():
                if q_lower in text.lower():
                    match_found = True
                    break
            
            if match_found and sid not in found_ids:
                # 构造一行数据
                row = {"ID": sid}
                for lang in LANG_ORDER:
                    row[lang] = langs.get(lang, "")
                final_rows.append(row)
                found_ids.add(sid)

    # 3. 导出 Excel
    if final_rows:
        df = pd.DataFrame(final_rows)
        # 调整列顺序：ID 在首列，后面跟着定义的语言顺序
        df = df[["ID"] + LANG_ORDER]
        df.to_excel(OUTPUT_FILE, index=False)
        print(f"导出成功！文件保存为: {OUTPUT_FILE}")
    else:
        print("未匹配到任何内容，未生成表格。")

if __name__ == "__main__":
    export_to_excel()