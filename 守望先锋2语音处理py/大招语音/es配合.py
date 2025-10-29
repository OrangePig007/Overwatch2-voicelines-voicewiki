import os
from pydub import AudioSegment

# Language mapping for audio file suffix naming
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
    "esla": "ESAL",
    "eseu": "ESEU",
    "pt": "PT",
    "pl": "PL"
}

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
    # Initialize language variables
    en = zhs = zht = ja = ko = ru = fr = de = it = esla = eseu = pt = pl = ""

    # Fill language variables based on the file path
    for file_path in file_paths:
        if '\\EN\\' in file_path:
            en = os.path.basename(file_path).split("-", 1)[-1][0:-4]
        elif '\\ZHT\\' in file_path:
            zht = os.path.basename(file_path).split("-", 1)[-1][0:-4]
        elif '\\ZHS\\' in file_path:
            zhs = os.path.basename(file_path).split("-", 1)[-1][0:-4]
        elif '\\JA\\' in file_path:
            ja = os.path.basename(file_path).split("-", 1)[-1][0:-4]
        elif '\\KO\\' in file_path:
            ko = os.path.basename(file_path).split("-", 1)[-1][0:-4]
        elif '\\RU\\' in file_path:
            ru = os.path.basename(file_path).split("-", 1)[-1][0:-4]
        elif '\\FR\\' in file_path:
            fr = os.path.basename(file_path).split("-", 1)[-1][0:-4]
        elif '\\DE\\' in file_path:
            de = os.path.basename(file_path).split("-", 1)[-1][0:-4]
        elif '\\IT\\' in file_path:
            it = os.path.basename(file_path).split("-", 1)[-1][0:-4]
        elif '\\ESEU\\' in file_path:
            eseu = os.path.basename(file_path).split("-", 1)[-1][0:-4]
        elif '\\ESLA\\' in file_path:
            esla = os.path.basename(file_path).split("-", 1)[-1][0:-4]
        elif '\\PT\\' in file_path:
            pt = os.path.basename(file_path).split("-", 1)[-1][0:-4]
        elif '\\PL\\' in file_path:
            pl = os.path.basename(file_path).split("-", 1)[-1][0:-4]

    # Write the result to the output file
    with open(output_path, "w+", encoding='utf-8') as file_to_write:
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
}}}}''')

# Predefined list of file paths
file_paths = [
    "G:\\守望语音\\ow-freja-ver\\ESLA\\BetterHeroVoice\\Venture\\Ultimate\\0000000668BB.0B2-¡Trazando el sitio de excavación!.ogg",
    "G:\\守望语音\\ow-freja-ver\\ESEU\\BetterHeroVoice\\Venture\\Ultimate\\0000000668BB.0B2-¡Trazando el yacimiento!.ogg",
    "G:\\守望语音\\ow-freja-ver\\EN\\HeroVoice\\Venture\\Ultimate\\0000000668BB.0B2-Plotting out the dig site!.ogg",
    "G:\\守望语音\\ow-freja-ver\\EN\\BetterHeroVoice\\Venture\\Ultimate\\0000000668BB.0B2-Plotting out the dig site!.ogg",
    "G:\\守望语音\\ow-freja-ver\\DE\\BetterHeroVoice\\Venture\\Ultimate\\0000000668BB.0B2-Stecke die Grabungsstelle ab!.ogg",
    "G:\\守望语音\\ow-freja-ver\\IT\\BetterHeroVoice\\Venture\\Ultimate\\0000000668BB.0B2-Studiamo l'area di scavo!.ogg",
    "G:\\守望语音\\ow-freja-ver\\PT\\BetterHeroVoice\\Venture\\Ultimate\\0000000668BB.0B2-Traçando o local da escavação!.ogg",
    "G:\\守望语音\\ow-freja-ver\\FR\\BetterHeroVoice\\Venture\\Ultimate\\0000000668BB.0B2-Un excellent site de fouilles !.ogg",
    "G:\\守望语音\\ow-freja-ver\\PL\\BetterHeroVoice\\Venture\\Ultimate\\0000000668BB.0B2-Wyznaczam miejsce wykopalisk!.ogg",
    "G:\\守望语音\\ow-freja-ver\\RU\\BetterHeroVoice\\Авентюра\\Ultimate\\0000000668BB.0B2-Место раскопок выбрано!.ogg",
    "G:\\守望语音\\ow-freja-ver\\ZHS\\BetterHeroVoice\\探奇\\Ultimate\\0000000668BB.0B2-开始划分发掘现场！.ogg",
    "G:\\守望语音\\ow-freja-ver\\ZHT\\BetterHeroVoice\\無畏\\Ultimate\\0000000668BB.0B2-正在繪製挖掘地點！.ogg",
    "G:\\守望语音\\ow-freja-ver\\JA\\BetterHeroVoice\\ベンチャー\\Ultimate\\0000000668BB.0B2-発掘現場はここだ！.ogg",
    "G:\\守望语音\\ow-freja-ver\\KO\\BetterHeroVoice\\벤처\\Ultimate\\0000000668BB.0B2-발굴 현장 구상 시작!.ogg"
]

# Specify output paths
num = "00000005779F.0B2"
output_path = "G:\\守望语音\\ow-freja-ver\\ulti.txt"
output_folder = "G:\\守望语音\\ow-freja-ver\\转换后的音频"

# Process the files
output_text(file_paths, output_path, num)
print("输出已保存到", output_path)
rename_and_convert(file_paths, output_folder)
print("音频已转换并保存到", output_folder)
