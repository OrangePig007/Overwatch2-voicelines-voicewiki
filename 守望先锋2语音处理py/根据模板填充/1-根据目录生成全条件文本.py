import os


def save(file_path, hero, action, zh_path, en_path, first=None):
    en = sorted(os.listdir(os.path.join(en_path, action)))
    print(action)
    zh = sorted(os.listdir(os.path.join(zh_path, action)))
    with open(file_path, 'a+', encoding='utf-8') as f:
        f.write(f'\n\n=={hero}\{action}==\n')
        for e, z in zip(en, zh):
            _e = e.split('-', 1)[-1][0:-4]
            if _e != '':
                _en1 = _e[-1]
                __en1 = _e[0:-1]
                if _en1=='_':
                    _e = __en1 + '?'
                elif  _en1=='!':
                    _e = __en1 + '!'
                else:
                    _e = _e + '.'
            else:
                _e = '...'
            _e1 = _e.replace(")_ ", ") ")
            _e = _e1.replace("_", "?")
            fi = e[0:16]
            if first and fi in first:
                fi += '|E'
            has_lang = _e != ''
            _z = z.replace('.ogg', '').split('-', 1)
            _z0 = _z[1] if len(_z) > 1 else ""
            _z1 = _z0.replace("（", "(")
            _z2 = _z1.replace("）：", ")")
            _z3 = _z2.replace("）", ")")
            if has_lang:
                f.write(f'{{{{OW2Audio|File={fi}|en={_e}|zh={_z3}}}}}\n')
            else:
                f.write(f'{{{{OW2Audio|File={fi}}}}}\n')


hero = '索杰恩'
file = f'F:/QQ文件/试验/20231005-{hero}.txt'
action_en = 'F:/守望先锋语音/EN/HeroVoice/Sojourn'
action_zh = f'F:/守望先锋语音/ZHS/HeroVoice/{hero}'
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
open(file, 'w+', encoding='utf-8')
first_gen = set(i.strip() for i in open('F:/QQ文件/试验/守望先锋1代所有语音序号.txt', 'r', encoding='utf-8').readlines())
for action in actions:
    save(file, hero, action, action_zh, action_en, first_gen)
