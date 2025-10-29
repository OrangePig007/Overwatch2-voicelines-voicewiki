import os

def save(file_path, hero, action, zh_path, en_path, first=None):
    # 先检查英文和中文路径是否都存在
    en_full_path = os.path.join(en_path, action)
    zh_full_path = os.path.join(zh_path, action)
    
    # 检查路径是否存在
    if not os.path.exists(en_full_path):
        print(f"警告: 英文路径不存在，已跳过 - {en_full_path}")
        return
    if not os.path.exists(zh_full_path):
        print(f"警告: 中文路径不存在，已跳过 - {zh_full_path}")
        return
    
    try:
        e = sorted(os.listdir(en_full_path))
        z = sorted(os.listdir(zh_full_path))
        
        with open(file_path, 'a+', encoding='utf-8') as f:
            f.write(f'\n=={action}==\n')
            f.write("{{OWVoiceTable\n")
            for en, zh in zip(e, z):
                num = en.split('-', 3)[0]
                name = en.split('-', 3)[1]
                fi = en.split('-', 3)[2]
                en1 = en.split('-', 3)[3][0:-4]
                
                if en1 != '':
                    _en1 = en1[-1]
                    __en1 = en1[0:-1]
                    if _en1 == '_':
                        en1 = __en1 + '?'
                    elif _en1 == '!':
                        en1 = __en1 + '!'
                    else:
                        en1 = en1 + '.'
                else:
                    en1 = '...'
                
                _e1 = en1.replace(")_ ", ") ")
                _e2 = _e1.replace("_", "?")

                zh1 = zh.split('-', 3)[3][0:-4]
                _z1 = zh1.replace("（", "(")
                _z2 = _z1.replace("）：", ")")
                _z3 = _z2.replace("）", ")")
                
                f.write(f'|hero{num}={name}|file{num}={fi}|en{num}={_e2}|zh{num}={_z3}\n')
            f.write('}}')
    except Exception as e:
        print(f"处理 {action} 时出错: {str(e)}")


hero = 'AllConv'
file = f'G:\\守望语音\\ow-wuyang-ver\\{hero}250919.txt'
action_en = r'G:\守望语音\ow-wuyang-ver\对话(en)\HeroConvo'
action_zh = r'G:\守望语音\ow-wuyang-ver\对话(zh)\HeroConvo'
actions_en = os.listdir(action_en)

actions = []
for i in actions_en:
    path = os.path.join(action_en, i)
    all_ogg = True
    for sub in os.listdir(path):
        sub_path = os.path.join(path, sub)
        if os.path.isdir(sub_path):
            all_ogg = False
            actions.append(os.path.join(i, sub))
    if all_ogg:
        actions.append(i)

actions.sort()
print(actions)

# 清空文件
with open(file, 'w+', encoding='utf-8') as f:
    pass

for action in actions:
    save(file, hero, action, action_zh, action_en)
