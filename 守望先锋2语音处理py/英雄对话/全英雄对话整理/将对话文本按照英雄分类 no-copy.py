import re
import os

# ==============================
# 全局配置区
# ==============================
# 1. 文本与模板路径
INPUT_VOICE_FILE = r'G:\守望语音\ow-domina-ver\all260307.txt'
TEMPLATE_FILE = r'英雄对话\全英雄对话整理\对话模板.txt'

# 2. 输出文本路径
OUTPUT_FOLDER = r'G:\守望语音\ow-domina-ver'
TARGET_HERO_CHINESE = "天使"
OUTPUT_FILENAME = f'{TARGET_HERO_CHINESE}_双人对话.txt'
OUTPUT_PATH = os.path.join(OUTPUT_FOLDER, OUTPUT_FILENAME)

# 3. 英雄顺序 (已更新)
HERO_ORDER = [
    'D.Va', '奥丽莎', '查莉娅', '温斯顿', '破坏球', '莱因哈特', '西格玛', 
    '路霸', '末日铁拳', '渣客女王', '拉玛刹', '毛加', '骇灾', '金驭', '半藏', 
    '回声', '堡垒', '士兵：76', '托比昂', '死神', '法老之鹰', '源氏', 
    '狂鼠', '猎空', '秩序之光', '美', '艾什', '卡西迪', '黑影', '黑百合', 
    '索杰恩', '探奇', '弗蕾娅', '斩仇','安燃','埃姆雷', '卢西奥', '天使', '安娜', '巴蒂斯特', 
    '布丽吉塔', '禅雅塔', '莫伊拉', '雾子', '生命之梭', '伊拉锐', '朱诺', '无漾', 
    '瑞稀', '飞天猫'
]

# 4. 名称映射 (已更新)
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
    '斩仇': 'Vendetta', '安燃': 'Anran', '埃姆雷': 'Emre',
    '金驭': 'Domina', '瑞稀': 'Mizuki', '飞天猫': 'Jetpack Cat',
}
reverse_name_mapping = {v: k for k, v in name_mapping.items()}


# ==============================
# 工具函数区
# ==============================
def replace_question_marks(text):
    """仅替换 ?内容? 格式（第一个?后无空格）为 "内容" """
    return re.sub(r'\?(?! )(.*?)\?', r'"\1"', text)


# ==============================
# 核心逻辑区
# ==============================
def main():
    # 1. 读取文本
    try:
        with open(INPUT_VOICE_FILE, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        print(f"读取文本失败: {str(e)}")
        return

    # 2. 提取对话
    voice_table_blocks = content.split("{{OWVoiceTable")
    target_hero_en = name_mapping.get(TARGET_HERO_CHINESE)
    
    if not target_hero_en:
        print(f"错误：映射表中未找到英雄 {TARGET_HERO_CHINESE}")
        return

    hero_dialogues = {} 

    for block in voice_table_blocks:
        if target_hero_en not in block:
            continue

        try:
            block_core = block.strip().split("}}")[0]
            voice_block = f"{{{{OWVoiceTable\n{block_core}}}}}"
            voice_block = replace_question_marks(voice_block)
        except IndexError:
            continue

        # 提取英雄
        heroes_in_block = []
        for hero_part in block.split('|hero'):
            if not hero_part.strip(): continue
            try:
                h_name = hero_part.strip().split('|')[0].split('=')[-1]
                if h_name and h_name not in heroes_in_block:
                    heroes_in_block.append(h_name)
            except IndexError: continue

        # 仅筛选双人对话
        if len(heroes_in_block) != 2:
            continue

        other_hero_en = [h for h in heroes_in_block if h != target_hero_en][0]
        if other_hero_en not in hero_dialogues:
            hero_dialogues[other_hero_en] = []

        if voice_block not in hero_dialogues[other_hero_en]:
            hero_dialogues[other_hero_en].append(voice_block)

    # 3. 排序并生成输出内容
    available_heroes_cn = []
    for hero_en in list(hero_dialogues.keys()):
        if hero_en in reverse_name_mapping:
            available_heroes_cn.append(reverse_name_mapping[hero_en])
        else:
            print(f"跳过未识别英雄: {hero_en}")

    sorted_heroes_cn = [h for h in HERO_ORDER if h in available_heroes_cn]

    output_content = f"{{{{Back|{TARGET_HERO_CHINESE}（守望先锋2）|{TARGET_HERO_CHINESE}}}}}\n\n"
    for hero_cn in sorted_heroes_cn:
        hero_en = name_mapping[hero_cn]
        dialogues = hero_dialogues[hero_en]
        output_content += f"== {hero_cn} ==\n"
        output_content += "\n".join(dialogues) + "\n\n"

    # 4. 写入文件
    try:
        os.makedirs(OUTPUT_FOLDER, exist_ok=True)
        with open(OUTPUT_PATH, 'w', encoding='utf-8') as f:
            f.write(output_content)
        print(f"\n任务完成！")
        print(f"文本已保存至: {OUTPUT_PATH}")
        print(f"整理了与 {len(sorted_heroes_cn)} 位英雄的对话")
    except Exception as e:
        print(f"文件写入失败: {str(e)}")


if __name__ == "__main__":
    main()