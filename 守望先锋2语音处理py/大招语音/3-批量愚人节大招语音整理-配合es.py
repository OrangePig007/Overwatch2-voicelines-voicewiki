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

def search_with_es(nums, path, temp_txt_path):
    # 使用 es.exe 在指定路径中搜索每个 num 并导出结果到临时文本文件
    es_exe_path = r'C:\Program Files\Everything\es.exe'
    combined_results = []
    
    for num in nums:
        command = f'"{es_exe_path}" "{num}" -path "{path}" -export-txt "{temp_txt_path}"'
        subprocess.run(command, shell=True)
        
        # 从临时文本文件读取搜索结果
        with open(temp_txt_path, 'r', encoding='utf-8') as file:
            result = [line.strip() for line in file.readlines()]
            combined_results.extend(result)
    
    return combined_results

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

def output_text(file_paths, output_path, nums):
    text_data = {}
    
    for num in nums:
        text_data[num] = {}
    
    for file_path in file_paths:
        for num in nums:
            if num in file_path:
                lang_abbr = get_lang_abbr(os.path.dirname(file_path))
                text_data[num][lang_abbr] = os.path.basename(file_path).split("-", 1)[-1][0:-4]

    with open(output_path, "w+", encoding='utf-8') as file_to_write:
        for num, lang_data in text_data.items():
            file_to_write.write(f'''{{{{OW13UFool|Num = {num}
|en = {lang_data.get("en", "")} 
|zh = {lang_data.get("zh", "")}
|zht = {lang_data.get("zht", "")}
|ja = {lang_data.get("ja", "")}
|ko = {lang_data.get("ko", "")}
|ru = {lang_data.get("ru", "")}
|fr = {lang_data.get("fr", "")}
|de = {lang_data.get("de", "")}
|eseu = {lang_data.get("eseu", "")}
|esla = {lang_data.get("esla", "")}
|it = {lang_data.get("it", "")}
|pt = {lang_data.get("pt", "")}
|pl = {lang_data.get("pl", "")}
}}}}\n''')

path = r"F:\守望先锋语音整理\ow-240826"
nums = input("请输入ID（逗号分隔）: ").split(",")
output_path = r"F:\守望先锋语音整理\ow-240826\ulti.txt"
output_folder = r"F:\守望先锋语音整理\ow-240826\转换后的音频"
temp_txt_path = r"F:\守望先锋语音整理\ow-240826\temp_search_results.txt"

file_paths = search_with_es(nums, path, temp_txt_path)
if file_paths:
    output_text(file_paths, output_path, nums)
    print("输出已保存到", output_path)
    rename_and_convert(file_paths, output_folder)
    print("音频已转换并保存到", output_folder)
else:
    print("未找到相关文件。")

# 删除临时文本文件
os.remove(temp_txt_path)
