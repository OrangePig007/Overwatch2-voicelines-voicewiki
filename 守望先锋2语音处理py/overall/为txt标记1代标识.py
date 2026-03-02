import re

def process_audio_file(source_file, list_file, output_file):
    # 1. 加载需要修改的序号列表，去除空格和换行
    with open(list_file, 'r', encoding='utf-8') as f:
        target_ids = {line.strip() for line in f if line.strip()}

    # 2. 定义正则模式：捕获 File= 后的序号，并定位 |en= 的位置
    # 模式解释：匹配 File= 后面跟着的十六进制/数字序号，直到遇到 |
    pattern = re.compile(r'File=([0-9A-F.]+)\|')

    processed_lines = []

    # 3. 处理主文件
    with open(source_file, 'r', encoding='utf-8') as f:
        for line in f:
            # 只处理以 {{OW2Audio 开头的行
            if line.strip().startswith('{{OW2Audio'):
                match = pattern.search(line)
                if match:
                    file_id = match.group(1)
                    # 如果序号在我们的目标集合中
                    if file_id in target_ids:
                        # 在 |en= 前插入 |E
                        line = line.replace('|en=', '|E|en=')
            
            processed_lines.append(line)

    # 4. 保存结果
    with open(output_file, 'w', encoding='utf-8') as f:
        f.writelines(processed_lines)

    print(f"处理完成！结果已保存至: {output_file}")

# 绝对路径示例
source_path = r"G:\守望语音\新更新-250428.txt"
list_path = r"G:\GithubFile\Overwatch2-voicelines-voicewiki\守望先锋2语音处理py\overall\守望先锋1代所有语音序号.txt"
output_path = r"G:\守望语音\新更新-250428-1代标了序号.txt"

process_audio_file(source_path, list_path, output_path)