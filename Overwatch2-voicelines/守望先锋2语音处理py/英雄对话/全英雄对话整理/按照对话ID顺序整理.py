
# 读取文档内容(只保留纯==ID==的txt)
with open('F:/守望先锋语音/all-pure-id.txt', 'r', encoding='utf-8') as file:
    lines = file.readlines()

# 创建一个字典来存储ID和内容
data = {}
current_id = None
current_content = []

# 解析文档内容
for line in lines:
    line = line.strip()
    if line.startswith('==') and line.endswith('=='):
        if current_id is not None:
            data[current_id] = '\n'.join(current_content)
            current_content = []
        current_id = line
    else:
        current_content.append(line)

# 处理最后一个条目
if current_id is not None:
    data[current_id] = '\n'.join(current_content)

# 按ID排序字典
sorted_data = dict(sorted(data.items()))

# 输出到另一个文本文件
with open('F:/守望先锋语音/all-pure-id-sorted.txt', 'w', encoding='utf-8') as output_file:
    for id_value, content in sorted_data.items():
        output_file.write(f'{id_value}\n{content}\n')
