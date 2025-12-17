import os
from pydub import AudioSegment
import subprocess

# 语言映射关系，用于给音频后缀命名
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
    # 使用 es.exe 在指定路径中搜索并导出到临时文本文件
    es_exe_path = r'C:\Program Files\Everything\es.exe'
    command = f'"{es_exe_path}" "{num}" -path "{path}" -export-txt "{temp_txt_path}"'
    subprocess.run(command, shell=True)
    
    # 从临时文本文件读取搜索结果
    with open(temp_txt_path, 'r', encoding='utf-8') as file:
        result = [line.strip() for line in file.readlines()]
    
    return result

def get_lang_abbr(directory):
    for lang_abbr, lang_dir in LANG_DIRECTORY_MAPPING.items():
        if lang_dir in directory:
            return lang_abbr
    return os.path.basename(directory).upper()

def rename_and_convert(file_paths, output_folder):
    for file_path in file_paths:
        filename = os.path.basename(file_path)
        lang_abbr = get_lang_abbr(os.path.dirname(file_path))

        lang_folder = os.path.join(output_folder)
        os.makedirs(lang_folder, exist_ok=True)

        new_filename = f"{filename.split('-', 1)[0]}_{lang_abbr}.mp3"
        new_path = os.path.join(output_folder, new_filename)

        sound = AudioSegment.from_file(file_path, format="ogg")
        sound.export(new_path, format="mp3")

def output_text(file_paths, output_path, num):
    en = zhs = zht = ja = ko = ru = fr = de = it = esla = eseu = pt = pl = ""

    for file_path in file_paths:
        if 'EN\\' in file_path:
            en = os.path.basename(file_path).split("-", 1)[-1][0:-4]
        elif 'ZHT\\' in file_path:
            zht = os.path.basename(file_path).split("-", 1)[-1][0:-4]
        elif 'ZHS\\' in file_path:
            zhs = os.path.basename(file_path).split("-", 1)[-1][0:-4]
        elif 'JA\\' in file_path:
            ja = os.path.basename(file_path).split("-", 1)[-1][0:-4]
        elif 'KO\\' in file_path:
            ko = os.path.basename(file_path).split("-", 1)[-1][0:-4]
        elif 'RU\\' in file_path:
            ru = os.path.basename(file_path).split("-", 1)[-1][0:-4]
        elif 'FR\\' in file_path:
            fr = os.path.basename(file_path).split("-", 1)[-1][0:-4]
        elif 'DE\\' in file_path:
            de = os.path.basename(file_path).split("-", 1)[-1][0:-4]
        elif 'IT\\' in file_path:
            it = os.path.basename(file_path).split("-", 1)[-1][0:-4]
        elif 'ESEU\\' in file_path:
            eseu = os.path.basename(file_path).split("-", 1)[-1][0:-4]
        elif 'ESLA\\' in file_path:
            esla = os.path.basename(file_path).split("-", 1)[-1][0:-4]
        elif 'PT\\' in file_path:
            pt = os.path.basename(file_path).split("-", 1)[-1][0:-4]
        elif 'PL\\' in file_path:
            pl = os.path.basename(file_path).split("-", 1)[-1][0:-4]

    with open(output_path, "a+", encoding='utf-8') as file_to_write:
        file_to_write.write(f'''{{{{OW13U|Num = {num}
|en = {en}
|en_tr = 
|zh = {zhs}
|zh_en = 
|zht = {zht}
|zht_en = 
|ja = {ja}
|ja_tr = 
|ko = {ko}
|ko_tr = 
|ru = {ru}
|ru_tr = 
|fr = {fr}
|fr_tr = 
|de = {de}
|de_tr = 
|eseu = {eseu}
|eseu_tr = 
|esla = {esla}
|esla_tr = 
|it = {it}
|it_tr = 
|pt = {pt}
|pt_tr = 
|pl = {pl}
|pl_tr = 
}}}}
''')

path = "G:\\守望语音\\ow-lupa-ver"
num = input("请输入ID: ")
output_path = "G:\\守望语音\\ow-lupa-ver\\ulti.txt"
output_folder = "G:\\守望语音\\ow-lupa-ver\\转换后的音频"
temp_txt_path = "G:\\守望语音\\ow-lupa-ver\\temp_search_results.txt"

file_paths = search_with_es(num, path, temp_txt_path)
if file_paths:
    output_text(file_paths, output_path, num)
    print("输出已保存到", output_path)
    rename_and_convert(file_paths, output_folder)
    print("音频已转换并保存到", output_folder)
else:
    print("未找到相关文件。")

# 删除临时文本文件
os.remove(temp_txt_path)