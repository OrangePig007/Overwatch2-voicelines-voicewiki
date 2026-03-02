import os
import re

# ================= 配置区域 =================
DATA_DIR = r"G:\守望语音\ow-domina-ver\本地化文本" 

# 按照你要求的顺序重新排列了 Key
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
    search_pool = [] 
    pattern = re.compile(r"^([0-9A-F]{12}\.07C):\s*(.*)$")

    print("正在预处理 13 国语言数据...")
    
    for lang_key, filename in FILES.items():
        path = os.path.join(DATA_DIR, filename)
        if not os.path.exists(path):
            print(f"找不到文件: {filename}")
            continue
            
        with open(path, 'r', encoding='utf-8', errors='ignore') as f:
            current_id = None
            current_content = []

            for line in f:
                line_str = line.rstrip('\n')
                match = pattern.match(line_str)
                
                if match:
                    if current_id:
                        text = "\n".join(current_content)
                        id_map[current_id][lang_key] = text
                        # 搜索池存入时去除换行符，方便匹配连贯的关键词
                        search_pool.append((text.replace("\n", "").lower(), current_id))
                    
                    current_id, first_part = match.groups()
                    if current_id not in id_map:
                        id_map[current_id] = {}
                    current_content = [first_part]
                else:
                    if current_id:
                        current_content.append(line_str)
            
            if current_id:
                text = "\n".join(current_content)
                id_map[current_id][lang_key] = text
                search_pool.append((text.replace("\n", "").lower(), current_id))
                    
    return id_map, search_pool

def main():
    id_map, search_pool = load_data()
    print(f"解析完成！已按照指定语言顺序就绪。")
    
    while True:
        query = input("\n请输入关键词 (q退出): ").strip().lower()
        if query == 'q': break
        if not query: continue

        # 匹配逻辑：在去掉了换行符的文本中查找
        match_ids = set()
        for clean_text, sid in search_pool:
            if query in clean_text:
                match_ids.add(sid)

        if not match_ids:
            print(f"未找到相关内容。")
            continue

        results = sorted(list(match_ids))
        print(f"\n找到 {len(results)} 个匹配项：")
        
        # 结果截断保护
        display_list = results
        if len(results) > 8:
            print(f"--- 匹配项较多，仅显示前 8 条 ---")
            display_list = results[:8]

        for sid in display_list:
            print(f"\n[ID: {sid}]")
            print("=" * 60)
            # 严格按照要求的 LANG_ORDER 顺序打印
            for lang in LANG_ORDER:
                text = id_map[sid].get(lang, "---")
                # 打印到控制台时保留原始换行，方便观察格式
                print(f"{lang:<5}: {text}")
            print("-" * 60)

if __name__ == "__main__":
    main()