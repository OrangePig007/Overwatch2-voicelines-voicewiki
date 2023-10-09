import re

# 读取文本文件
with open('F:/守望先锋语音/new试验/20231005全对话NoPvE', 'r', encoding='utf-8') as file:
    content = file.read()
with open('F:/守望先锋语音/new试验/对话模板.txt', 'r', encoding='utf-8') as template_file:
    template = template_file.read()
# 分割文本为块
voice_table_blocks = content.split("{{OWVoiceTable")

# 创建一个新的文本文件来存储只涉及两个人的对话
two_heroes_output_file = open('F:/守望先锋语音/new试验/two_heroes_output.txt', 'w', encoding='utf-8')

# 创建一个新的文本文件来存储多于两个人的对话
more_than_two_heroes_output_file = open('F:/守望先锋语音/new试验/more_than_two_heroes_output.txt', 'w', encoding='utf-8')

# 定义要查找的英雄
chinese_name = "索杰恩"  # 将目标英雄替换成你想要的英雄名字
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
}

target_hero = name_mapping[chinese_name]

# 创建一个字典来存储相同 unique_heroes 的 voice_table_block
unique_heroes_blocks = {}
more_than_two_heroes_content = ""
# 遍历块并将包含目标英雄的块写入相应的文件
for block in voice_table_blocks:
    if target_hero in block:
        # 重新构建完整的{{OWVoiceTable}}块
        voice_table_block = "{{OWVoiceTable\n" + block.strip().split("}}")[0] + "}}"
        hero1 = block.split('hero1=')[1].split("|")[0]
        # 检查块中包含的英雄数量
        heroes_in_block = [hero.strip().split('|')[0].split('=')[-1] for hero in block.split('|hero') if hero.strip()]
        unique_heroes1 = list(set(heroes_in_block))
        # 剔除掉目标英雄
        unique_heroes = [hero for hero in unique_heroes1 if hero != target_hero]
        print(unique_heroes)

        if len(unique_heroes) == 1:
                        # 根据英雄名称和模板中的#内容决定写入的位置
            hero_name = unique_heroes[0]
            
            # 将 voice_table_block 添加到字典中相应英雄的键下
            if hero_name in unique_heroes_blocks:
                unique_heroes_blocks[hero_name].append(voice_table_block)
            else:
                unique_heroes_blocks[hero_name] = [voice_table_block]

        elif (len(unique_heroes) >= 2) & (target_hero in unique_heroes1):
            if(hero1==target_hero):
                more_than_two_heroes_content += (voice_table_block + '\n')
        else:
            continue
# 遍历 unique_heroes_blocks 字典，将相同英雄的 voice_table_block 整合
for hero_name, blocks in unique_heroes_blocks.items():
    combined_block = "\n".join(blocks)
    
    # 根据英雄名称和模板中的#内容决定写入的位置
    template_position = f"#{hero_name}\n"
    
    # 在模板中找到对应位置并替换
    template = template.replace(template_position, template_position + combined_block)

# 删除模板中没有对应 voice_table_block 的 ==名称== 部分
template = re.sub(r'==[^=]+==\n#.*?\n\n', '', template)
template = re.sub(r'#.*?\n', '', template)

template=f'{{{{Back|{chinese_name}（守望先锋2）|{chinese_name}}}}}\n'+template

# 将 more_than_two_heroes_output_file 的内容融合到 template 的最底部
if len(more_than_two_heroes_content)>2:
    template += '\n==多人==\n'
    template += more_than_two_heroes_content
# 将模板写入输出文件
with open('F:/守望先锋语音/new试验/template_output.txt', 'w', encoding='utf-8') as template_output_file:
    template_output_file.write(template)
# 关闭输出文件
two_heroes_output_file.close()
more_than_two_heroes_output_file.close()
