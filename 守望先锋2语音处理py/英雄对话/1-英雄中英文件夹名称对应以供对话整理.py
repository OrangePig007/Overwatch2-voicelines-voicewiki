import os

# 映射字典，格式为{旧名称: 新名称}
name_mapping = {
    'D.Va': 'D.Va',
    '奥丽莎': 'Orisa',
    '查莉娅': 'Zarya',
    '温斯顿': 'Winston',
    '破坏球': 'Wrecking Ball',
    '莱因哈特': 'Reinhardt',
    '西格玛': 'Sigma',
    '路霸': 'Roadhog',
    '末日铁拳': 'Doomfist',
    '渣客女王': 'Junker Queen',
    '拉玛刹': 'Ramattra',
    '半藏': 'Hanzo',
    '回声': 'Echo',
    '堡垒': 'Bastion',
    '士兵：76': 'Soldier_ 76',
    '托比昂': 'Torbjörn',
    '死神': 'Reaper',
    '法老之鹰': 'Pharah',
    '源氏': 'Genji',
    '狂鼠': 'Junkrat',
    '猎空': 'Tracer',
    '秩序之光': 'Symmetra',
    '美': 'Mei',
    '艾什': 'Ashe',
    '卡西迪': 'Cassidy',
    '黑影': 'Sombra',
    '黑百合': 'Widowmaker',
    '索杰恩': 'Sojourn',
    '卢西奥': 'Lúcio',
    '天使': 'Mercy',
    '安娜': 'Ana',
    '巴蒂斯特': 'Baptiste',
    '布丽吉塔': 'Brigitte',
    '禅雅塔': 'Zenyatta',
    '莫伊拉': 'Moira',
    '雾子': 'Kiriko',
    '生命之梭': 'Lifeweaver',
    '伊拉锐': 'Illari',
    '毛加': 'Mauga',
    '探奇': 'Venture',
    '朱诺': 'Juno',
    '骇灾': 'Hazard',
    '弗蕾娅': 'Freja',
    '无漾': 'Wuyang',
    '斩仇': 'Vendetta',
    '安燃': 'Anran',
    '埃姆雷': 'Emre',
    '金驭': 'Domina',
    '瑞稀': 'Mizuki',
    '飞天猫': 'Jetpack Cat',

    '克莱尔': 'Claire',
    '雷吉': 'Reggie',
    '露娜': 'Luna',
    '侍者机器人': 'Waitron',
    '收音机': 'Radio',
    '叙述者': 'The Narrator',
    '雅典娜': 'Athena',
    '伊基': 'Iggy',
    '伊纳瑞斯': 'Inarius',
    '毁灭者':'The Ravager',
}

# 指定包含二级文件夹的父文件夹路径
parent_folder = r'G:\守望语音\ow-domina-ver\upload\ZH\BetterHeroVoice'

# 遍历父文件夹中的二级文件夹
for old_name, new_name in name_mapping.items():
    old_folder_path = os.path.join(parent_folder, old_name)
    new_folder_path = os.path.join(parent_folder, new_name)
    
    # 使用os.rename函数来重命名文件夹
    try:
        os.rename(old_folder_path, new_folder_path)
        print(f'Renamed {old_name} to {new_name}')
    except FileNotFoundError:
        print(f'Folder {old_name} not found')

print('All renaming completed')
