import os
from pydub import AudioSegment

# 语言映射关系，用于给音频后缀命名
LANG_DIRECTORY_MAPPING = {
    "ja": "JA",
    "en": "EN",
    "zh": "ZHS",
    "zht": "ZHT",
    "ko": "KR",
    "ru": "RU",
    "fr": "FR",
    "de": "DE",
    "it": "IT",
    "esla": "ESAL",
    "eseu": "ESEU",
    "pt": "PT",
    "pl": "PL"
}

def search(path, nums):
    result = []
    for num in nums:
        for root, dirs, files in os.walk(path):
            for file in files:
                if num in file:
                    result.append(os.path.join(root, file))
                    print('找到文件：' + os.path.join(root, file))
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

path = "F:/守望先锋语音"
nums = input("请输入ID（逗号分隔）: ").split(",")
output_path = "F:/守望先锋语音/ulti.txt"
output_folder = "F:/守望先锋语音/转换后的音频"

file_paths = search(path, nums)
if file_paths:
    output_text(file_paths, output_path, nums)
    print("输出已保存到", output_path)
    rename_and_convert(file_paths, output_folder)
    print("音频已转换并保存到", output_folder)
else:
    print("未找到相关文件。")
