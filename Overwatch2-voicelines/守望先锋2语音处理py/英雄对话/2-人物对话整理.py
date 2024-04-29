import os
def save(file_path, hero, action, zh_path, en_path, first=None):
    e = sorted(os.listdir(os.path.join(en_path, action)))
    print(action)
    z = sorted(os.listdir(os.path.join(zh_path, action)))
    with open(file_path, 'a+', encoding='utf-8') as f:
        f.write(f'\n=={action}==\n')
        f.write("{{OWVoiceTable\n")
        for en, zh in zip(e, z):
            num = en.split('-', 3)[0]
            name = en.split('-', 3)[1]
            # name_zh = zh.split('-', 3)[1]
            fi = en.split('-', 3)[2]
            en1 = en.split('-', 3)[3][0:-4]
            if en1 != '':
                _en1 = en1[-1]
                __en1 = en1[0:-1]
                if _en1=='_':
                    en1 = __en1 + '?'
                elif  _en1=='!':
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


hero = 'all-conv'
file = f'F:\守望先锋语音整理\ow-240426/{hero}.txt'
action_en = r'F:\守望先锋语音整理\ow-240426\EN-conv\HeroConvo'
action_zh = r'F:\守望先锋语音整理\ow-240426\ZH-conv\HeroConvo'
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
open(file, 'w+',encoding='utf-8')
for action in actions:
    save(file, hero, action, action_zh, action_en)