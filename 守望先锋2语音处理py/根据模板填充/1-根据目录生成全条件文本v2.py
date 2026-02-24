import os
#这个会把大招文件夹的音频和文件夹都统计


# 定义一个专门记录错误日志的文件路径
filefolder = 'ow-domina-ver'
error_log_path = f'G:\\守望语音\\{filefolder}\\missing_paths_log.txt'

hero = 'Emre'
file = f'G:\\守望语音\\{filefolder}\\{hero}-260224fin.txt'
action_zh = rf'G:\守望语音\ow-domina-ver\ZH-NPC\NPCVoice\埃姆雷'
action_en = rf'G:\守望语音\ow-domina-ver\EN-NPC\NPCVoice\Emre'
actions_en = os.listdir(action_en)

actions = []

def save(file_path, hero, action, zh_path, en_path, first=None):
    current_zh_path = os.path.join(zh_path, action)
    current_en_path = os.path.join(en_path, action)
    
    # 1. 检查中文路径是否存在
    if not os.path.exists(current_zh_path):
        with open(error_log_path, 'a+', encoding='utf-8') as err_f:
            err_f.write(f"[目录缺失] {hero} | {action} | 中文路径不存在\n")
        return

    try:
        # 获取文件列表并过滤掉不包含 .0B2 的文件
        en = sorted([f for f in os.listdir(current_en_path) if ".0B2" in f])
        zh = sorted([f for f in os.listdir(current_zh_path) if ".0B2" in f])
        
        # 如果过滤后该文件夹为空，记录一下并跳过
        if not en:
            with open(error_log_path, 'a+', encoding='utf-8') as err_f:
                err_f.write(f"[跳过] {action} | 文件夹内无有效 .0B2 文件\n")
            return

        print(f"正在处理: {action}")

        with open(file_path, 'a+', encoding='utf-8') as f:
            f.write(f'\n\n=={hero}\\{action}==\n')
            
            # 使用 zip 对齐处理，注意：如果中英文数量不一致，zip 会以短的为准
            for e, z in zip(en, zh):
                # 提取英文文本逻辑
                _e = e.split('-', 1)[-1][0:-4]
                if _e != '':
                    _en1 = _e[-1]
                    __en1 = _e[0:-1]
                    if _en1 == '_': _e = __en1 + '?'
                    elif _en1 == '!': _e = __en1 + '!'
                    else: _e = _e + '.'
                else:
                    _e = '...'
                
                _e1 = _e.replace(")_ ", ") ")
                _e = _e1.replace("_", "?")
                
                # 提取文件 ID (前16位)
                fi = e[0:16]
                if first and fi in first:
                    fi += '|E'
                
                # 处理中文文本
                _z = z.replace('.ogg', '').split('-', 1)
                _z0 = _z[1] if len(_z) > 1 else ""
                _z1 = _z0.replace("（", "(").replace("）：", ")").replace("）", ")")
                
                # 写入 Wiki 模板
                if _e != '':
                    f.write(f'{{{{OW2Audio|File={fi}|en={_e}|zh={_z1}}}}}\n')
                else:
                    f.write(f'{{{{OW2Audio|File={fi}}}}}\n')
                    
    except Exception as err:
        with open(error_log_path, 'a+', encoding='utf-8') as err_f:
            err_f.write(f"[运行报错] {action} | 错误信息: {str(err)}\n")


def collect_actions(directory, actions, base_path):
    # 先检查当前目录是否有音频文件
    has_audio = any(file.lower().endswith('.ogg') for file in os.listdir(directory) 
                   if os.path.isfile(os.path.join(directory, file)))
    
    # 如果有音频文件，添加当前目录到列表
    if has_audio:
        relative_path = os.path.relpath(directory, base_path)
        actions.append(relative_path)
    
    # 递归处理所有子文件夹
    for sub in os.listdir(directory):
        sub_path = os.path.join(directory, sub)
        if os.path.isdir(sub_path):
            collect_actions(sub_path, actions, base_path)

for i in actions_en:
    path = os.path.join(action_en, i)
    collect_actions(path, actions, action_en)

actions.sort()
print(actions)
open(file, 'w+', encoding='utf-8')
#first_gen = set(i.strip() for i in open('E:\守望先锋毛加版本语音\py\Overwatch2-voicelines-voicewiki-main\守望先锋2语音处理py\overall/守望先锋1代所有语音序号.txt', 'r', encoding='utf-8').readlines())
first_gen = ''
for action in actions:
    save(file, hero, action, action_zh, action_en, first_gen)
