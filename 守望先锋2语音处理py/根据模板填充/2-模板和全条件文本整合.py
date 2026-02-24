
hero = 'Mizuki'
condition = '击杀语音'
#击杀语音 交流信号 局内触发 任务相关 地图触发
# 读取文档1和文档2的内容
# with open(f'F:/QQ文件/试验/20231005-{hero_zh}.txt', 'r', encoding='utf-8') as file1:
#     doc1_content = file1.read()

with open(f'G:\守望语音\ow-domina-ver/{hero}-260224.txt', 'r', encoding='utf-8') as file1:
    doc1_content = file1.read()

with open(f'G:\GithubFile\Overwatch2-voicelines-voicewiki\守望先锋2语音处理py\根据模板填充\{condition}模板.txt', 'r', encoding='utf-8') as file2:
    doc2_content = file2.read()

# 将文档2的内容分割成行
doc2_lines = doc2_content.split('\n')

# 初始化一个字典来存储英文标识码和对应的内容
code_to_content = {}

# 遍历文档2的行，解析英文标识码和内容的映射
for line in doc2_lines:
    if '#' in line:
        code = line.split('#')[1].strip()
        code_to_content[code] = ""

# 遍历文档1的内容，查找匹配的英文标识码，并填充内容
for code, content in code_to_content.items():
    start_marker = f'=={hero}\\{code}=='
    end_marker = f'\n\n'
    start_index = doc1_content.find(start_marker)
    
    if start_index != -1:
        end_index = doc1_content.find(end_marker, start_index)
        if end_index != -1:
            content = doc1_content[start_index + len(start_marker):end_index]
            code_to_content[code] = content


# 生成最终的文档
final_doc = ""
for line in doc2_lines:
    if '#' in line:
        code = line.split('#')[1].strip()
        if code_to_content[code]:
            # 替换#标识符为对应的内容，保留原始文档2中的回车符
            final_doc += code_to_content[code].lstrip('\n') + '\n'
            print(final_doc)
        else:
            final_doc += line + '\n'
    else:
        final_doc += line + '\n'

# 将最终文档写入文件
with open(f'G:\守望语音\ow-domina-ver/{condition}output.txt', 'w', encoding='utf-8') as final_file:
    final_file.write(final_doc)
