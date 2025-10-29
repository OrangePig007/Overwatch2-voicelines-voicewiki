import re
import os
import shutil

# ==============================
# 全局配置区 - 所有路径和参数都在这里设置
# ==============================
# 1. 文本与模板路径
INPUT_VOICE_FILE = 'G:\守望语音\ow-wuyang-ver/AllConv250919.txt'  # 所有英雄语音合集文件
TEMPLATE_FILE = '英雄对话\全英雄对话整理\对话模板.txt'  # 模板文件（可选）

# 2. 输出文本路径
OUTPUT_FOLDER = 'G:/守望语音/ow-wuyang-ver/'  # 文本输出文件夹
TARGET_HERO_CHINESE = "堡垒"  # 要提取的目标英雄中文名
OUTPUT_FILENAME = f'{TARGET_HERO_CHINESE}_双人对话.txt'  # 文本输出文件名
OUTPUT_PATH = os.path.join(OUTPUT_FOLDER, OUTPUT_FILENAME)  # 完整文本输出路径

# 3. 音频文件路径
AUDIO_EN_FOLDER = 'G:\守望语音\ow-wuyang-ver\对话(en)\HeroConvo'  # 英文音频源文件夹
AUDIO_ZH_FOLDER = 'G:\守望语音\ow-wuyang-ver\对话(zh)\HeroConvo'  # 中文音频源文件夹
UPLOAD_FOLDER = 'G:\守望语音\ow-wuyang-ver\待上传'  # 音频待上传文件夹

# 4. 英雄顺序和名称映射
HERO_ORDER = [
    'D.Va', '奥丽莎', '查莉娅', '温斯顿', '破坏球', '莱因哈特', '西格玛', 
    '路霸', '末日铁拳', '渣客女王', '拉玛刹', '毛加', '骇灾', '半藏', 
    '回声', '堡垒', '士兵：76', '托比昂', '死神', '法老之鹰', '源氏', 
    '狂鼠', '猎空', '秩序之光', '美', '艾什', '卡西迪', '黑影', '黑百合', 
    '索杰恩', '探奇', '弗蕾娅', '卢西奥', '天使', '安娜', '巴蒂斯特', 
    '布丽吉塔', '禅雅塔', '莫伊拉', '雾子', '生命之梭', '伊拉锐', '朱诺', '无漾'
]

name_mapping = {
    'D.Va': 'D.Va', '奥丽莎': 'Orisa', '查莉娅': 'Zarya', '温斯顿': 'Winston',
    '破坏球': 'Wrecking Ball', '莱因哈特': 'Reinhardt', '西格玛': 'Sigma',
    '路霸': 'Roadhog', '末日铁拳': 'Doomfist', '渣客女王': 'Junker Queen',
    '拉玛刹': 'Ramattra', '半藏': 'Hanzo', '回声': 'Echo', '堡垒': 'Bastion',
    '士兵：76': 'Soldier_ 76', '托比昂': 'Torbjörn', '死神': 'Reaper',
    '法老之鹰': 'Pharah', '源氏': 'Genji', '狂鼠': 'Junkrat', '猎空': 'Tracer',
    '秩序之光': 'Symmetra', '美': 'Mei', '艾什': 'Ashe', '卡西迪': 'Cassidy',
    '黑影': 'Sombra', '黑百合': 'Widowmaker', '索杰恩': 'Sojourn',
    '卢西奥': 'Lúcio', '天使': 'Mercy', '安娜': 'Ana', '巴蒂斯特': 'Baptiste',
    '布丽吉塔': 'Brigitte', '禅雅塔': 'Zenyatta', '莫伊拉': 'Moira',
    '雾子': 'Kiriko', '生命之梭': 'Lifeweaver', '伊拉锐': 'Illari',
    '毛加': 'Mauga', '探奇': 'Venture', '朱诺': 'Juno', '骇灾': 'Hazard',
    '弗蕾娅': 'Freja', '无漾': 'Wuyang',
}
reverse_name_mapping = {v: k for k, v in name_mapping.items()}


# ==============================
# 工具函数区
# ==============================
def replace_question_marks(text):
    """仅替换 ?内容? 格式（第一个?后无空格）为 "内容" """
    return re.sub(r'\?(?! )(.*?)\?', r'"\1"', text)


def collect_audio_files(audio_folder, lang):
    """收集指定文件夹下的音频文件，返回 {音频ID: 完整路径} 的字典"""
    audio_map = {}
    for root, _, files in os.walk(audio_folder):
        for filename in files:
            if filename.endswith('.ogg'):
                # 拆分文件名（格式：xxx-xxx-音频ID.ogg），提取音频ID
                file_parts = filename.split('-')
                if len(file_parts) >= 3:
                    audio_id = file_parts[2].replace('.ogg', '')  # 去掉后缀，保留纯ID
                    audio_map[audio_id] = os.path.join(root, filename)
    print(f"已收集 {lang} 音频 {len(audio_map)} 个")
    return audio_map


def copy_audio_to_upload(audio_id, audio_map_en, audio_map_zh, upload_folder):
    """根据音频ID，复制中英文音频到待上传文件夹"""
    # 处理英文音频
    if audio_id in audio_map_en:
        en_dest = os.path.join(upload_folder, f"{audio_id}_en.ogg")
        shutil.copy(audio_map_en[audio_id], en_dest)
        # print(f"已复制英文音频: {audio_id}_en.ogg")
    
    # 处理中文音频
    if audio_id in audio_map_zh:
        zh_dest = os.path.join(upload_folder, f"{audio_id}_zh.ogg")
        shutil.copy(audio_map_zh[audio_id], zh_dest)
        # print(f"已复制中文音频: {audio_id}_zh.ogg")


# ==============================
# 核心逻辑区
# ==============================
def main():
    # 1. 初始化：创建待上传文件夹（如果不存在）
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    print(f"已确保待上传文件夹存在: {UPLOAD_FOLDER}")

    # 2. 收集中英文音频文件（提前建立ID与路径的映射，提高效率）
    audio_map_en = collect_audio_files(AUDIO_EN_FOLDER, 'en')
    audio_map_zh = collect_audio_files(AUDIO_ZH_FOLDER, 'zh')

    # 3. 读取语音合集文本
    try:
        with open(INPUT_VOICE_FILE, 'r', encoding='utf-8') as f:
            content = f.read()
        print(f"\n成功读取语音文本: {INPUT_VOICE_FILE}")
    except Exception as e:
        print(f"读取文本失败: {str(e)}")
        return

    # 4. 读取模板文件（可选）
    try:
        with open(TEMPLATE_FILE, 'r', encoding='utf-8') as f:
            template = f.read()
        print(f"成功读取模板文件: {TEMPLATE_FILE}")
    except (FileNotFoundError, Exception) as e:
        print(f"模板文件处理异常: {str(e)}，将使用默认格式")

    # 5. 提取目标英雄的双人对话
    voice_table_blocks = content.split("{{OWVoiceTable")
    target_hero_en = name_mapping.get(TARGET_HERO_CHINESE)
    if not target_hero_en:
        print(f"错误：未找到 {TARGET_HERO_CHINESE} 的英文映射")
        return

    hero_dialogues = {}  # 存储 {对话对象英文名: [对话块列表]}
    used_audio_ids = set()  # 记录已处理的音频ID，避免重复复制

    for block in voice_table_blocks:
        if target_hero_en not in block:
            continue  # 跳过不含目标英雄的块

        # 重构对话块 + 替换成对问号
        try:
            block_core = block.strip().split("}}")[0]
            voice_block = f"{{{{OWVoiceTable\n{block_core}}}}}"
            voice_block = replace_question_marks(voice_block)  # 处理问号
        except IndexError:
            continue  # 跳过格式错误的块

        # 提取块中涉及的所有英雄（去重）
        heroes_in_block = []
        for hero_part in block.split('|hero'):
            if not hero_part.strip():
                continue
            try:
                hero_name = hero_part.strip().split('|')[0].split('=')[-1]
                if hero_name and hero_name not in heroes_in_block:
                    heroes_in_block.append(hero_name)
            except IndexError:
                continue

        # 只保留「恰好2个英雄」的对话
        if len(heroes_in_block) != 2:
            continue

        # 确定对话对象（排除目标英雄自身）
        other_hero_en = [h for h in heroes_in_block if h != target_hero_en][0]
        if other_hero_en not in hero_dialogues:
            hero_dialogues[other_hero_en] = []

        # 避免重复添加对话块
        if voice_block not in hero_dialogues[other_hero_en]:
            hero_dialogues[other_hero_en].append(voice_block)

            # 提取当前对话块中的音频ID（file1=xxx、file2=xxx等）
            audio_ids = re.findall(r'file\d+=(.*?)\|', block_core)
            for audio_id in audio_ids:
                if audio_id and audio_id not in used_audio_ids:
                    used_audio_ids.add(audio_id)
                    # 复制音频到待上传文件夹
                    #copy_audio_to_upload(audio_id, audio_map_en, audio_map_zh, UPLOAD_FOLDER)

    # 6. 处理未知英雄（如Unknown1FE）
    available_heroes_cn = []
    for hero_en in list(hero_dialogues.keys()):
        try:
            hero_cn = reverse_name_mapping[hero_en]
            available_heroes_cn.append(hero_cn)
        except KeyError:
            print(f"警告：未识别英雄 {hero_en}，已跳过其对话")
            del hero_dialogues[hero_en]

    # 7. 按指定顺序排列对话
    sorted_heroes_cn = [h for h in HERO_ORDER if h in available_heroes_cn]

    # 8. 生成输出文本内容
    output_content = f"{{{{Back|{TARGET_HERO_CHINESE}（守望先锋2）|{TARGET_HERO_CHINESE}}}}}\n\n"
    #output_content += f"=={TARGET_HERO_CHINESE}的双人对话==\n\n"

    for hero_cn in sorted_heroes_cn:
        hero_en = name_mapping[hero_cn]
        dialogues = hero_dialogues[hero_en]
        # 按要求的格式添加标题
        output_content += f"== {hero_cn} ==\n"
        #output_content += f"#{hero_en}\n\n"
        output_content += "\n".join(dialogues)
        output_content += "\n\n"

    # 9. 写入输出文本
    try:
        with open(OUTPUT_PATH, 'w', encoding='utf-8') as f:
            f.write(output_content)
        print(f"\n文本文件已保存: {OUTPUT_PATH}")
        print(f"共整理对话组数: {len(sorted_heroes_cn)}")
        print(f"共复制音频文件: {len(used_audio_ids)} 个")
    except Exception as e:
        print(f"写入文本失败: {str(e)}")


if __name__ == "__main__":
    main()