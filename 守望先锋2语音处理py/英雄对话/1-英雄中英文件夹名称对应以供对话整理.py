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
    '托比昂': 'Torbjorn',
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
    '卢西奥': 'Lucio',
    '天使': 'Mercy',
    '安娜': 'Ana',
    '巴蒂斯特': 'Baptiste',
    '布丽吉塔': 'Brigitte',
    '禅雅塔': 'Zenyatta',
    '莫伊拉': 'Moira',
    '雾子': 'Kiriko',
    '生命之梭': 'Lifeweaver',
    '伊拉锐': 'Illari',
}

# 指定包含二级文件夹的父文件夹路径
parent_folder = 'F:\守望先锋语音\对话(zh)'

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
