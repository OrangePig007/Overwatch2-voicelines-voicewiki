import os
from pydub import AudioSegment
import subprocess
# 可以同时处理多个20260309
# 语言映射关系
LANG_DIRECTORY_MAPPING = {
    "ja": "JA",
    "en": "EN",
    "zh": "ZHS",
    "zht": "ZHT",
    "ko": "KO",
    "ru": "RU",
    "fr": "FR",
    "de": "DE",
    "it": "IT",
    "esla": "ESLA",
    "eseu": "ESEU",
    "pt": "PT",
    "pl": "PL"
}

def search_with_es(num, path, temp_txt_path):
    es_exe_path = r'C:\Program Files\Everything\es.exe'
    # 使用 double quotes 处理路径中可能存在的空格
    command = f'"{es_exe_path}" "{num}" -path "{path}" -export-txt "{temp_txt_path}"'
    subprocess.run(command, shell=True)
    
    if not os.path.exists(temp_txt_path):
        return []
        
    with open(temp_txt_path, 'r', encoding='utf-8') as file:
        result = [line.strip() for line in file.readlines() if line.strip()]
    
    return result

def get_lang_abbr(directory):
    for lang_abbr, lang_dir in LANG_DIRECTORY_MAPPING.items():
        if f'\\{lang_dir}\\' in f'\\{directory}\\': # 增强匹配准确度
            return lang_abbr
    return os.path.basename(directory).upper()

def rename_and_convert(file_paths, output_folder):
    for file_path in file_paths:
        try:
            filename = os.path.basename(file_path)
            lang_abbr = get_lang_abbr(os.path.dirname(file_path))

            os.makedirs(output_folder, exist_ok=True)

            # 格式：ID_语言.mp3
            new_filename = f"{filename.split('-', 1)[0]}_{lang_abbr}.mp3"
            new_path = os.path.join(output_folder, new_filename)

            if not os.path.exists(new_path): # 避免重复转换
                sound = AudioSegment.from_file(file_path, format="ogg")
                sound.export(new_path, format="mp3")
        except Exception as e:
            print(f"转换文件 {file_path} 时出错: {e}")

def output_text(file_paths, output_path, num):
    # 初始化语言字典，方便扩展
    langs = {k: "" for k in ["en", "zhs", "zht", "ja", "ko", "ru", "fr", "de", "it", "esla", "eseu", "pt", "pl"]}

    for file_path in file_paths:
        content = os.path.basename(file_path).split("-", 1)[-1][:-4]
        dirname = os.path.dirname(file_path).upper()
        
        if 'EN\\' in dirname: langs['en'] = content
        elif 'ZHT\\' in dirname: langs['zht'] = content
        elif 'ZHS\\' in dirname: langs['zhs'] = content
        elif 'JA\\' in dirname: langs['ja'] = content
        elif 'KO\\' in dirname: langs['ko'] = content
        elif 'RU\\' in dirname: langs['ru'] = content
        elif 'FR\\' in dirname: langs['fr'] = content
        elif 'DE\\' in dirname: langs['de'] = content
        elif 'IT\\' in dirname: langs['it'] = content
        elif 'ESEU\\' in dirname: langs['eseu'] = content
        elif 'ESLA\\' in dirname: langs['esla'] = content
        elif 'PT\\' in dirname: langs['pt'] = content
        elif 'PL\\' in dirname: langs['pl'] = content

    with open(output_path, "a+", encoding='utf-8') as file_to_write:
        file_to_write.write(f'''{{{{OW13UFool|Num = {num}
|en = {langs['en']}
|zh = {langs['zhs']}
|zht = {langs['zht']}
|ja = {langs['ja']}
|ko = {langs['ko']}
|ru = {langs['ru']}
|fr = {langs['fr']}
|de = {langs['de']}
|eseu = {langs['eseu']}
|esla = {langs['esla']}
|it = {langs['it']}
|pt = {langs['pt']}
|pl = {langs['pl']}
}}}}
''')

# --- 主程序逻辑 ---

home_folder = 'ow-domina-ver'
base_path = f"G:\\守望语音\\{home_folder}"
output_path = os.path.join(base_path, "ulti.txt")
output_folder = os.path.join(base_path, "转换后的音频")
temp_txt_path = os.path.join(base_path, "temp_search_results.txt")

# 获取输入并处理成列表
raw_input = input("请输入ID (支持多个，用空格或逗号分隔): ")
# 将逗号和分号统一替换为空格，然后分割字符串
id_list = raw_input.replace(',', ' ').replace(';', ' ').split()

for current_id in id_list:
    current_id = current_id.strip()
    print(f"\n正在处理 ID: {current_id}...")
    
    file_paths = search_with_es(current_id, base_path, temp_txt_path)
    
    if file_paths:
        output_text(file_paths, output_path, current_id)
        rename_and_convert(file_paths, output_folder)
        print(f"ID {current_id} 处理完成。")
    else:
        print(f"未找到与 ID {current_id} 相关的文件。")

# 清理临时文件
if os.path.exists(temp_txt_path):
    os.remove(temp_txt_path)

print("\n所有任务已执行完毕！")