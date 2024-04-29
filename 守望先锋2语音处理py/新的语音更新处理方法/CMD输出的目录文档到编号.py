# 用集合存储已处理的 num 以避免重复
num_set = set()

# 读取输入文件
with open(r'F:\守望先锋语音整理\ow-240426\ZH-conv/filenames.txt', 'r') as file:
    for line in file.readlines():
        if '.0D0' in line:
            # 获取 num 值
            num = line.split('.0D0')[0][-12:]
            
            # 如果 num 不在集合中，说明它是新的
            if num not in num_set:
                # 将 num 添加到集合中
                num_set.add(num)
                
                # 将 num 写入输出文件
                with open(r'F:\守望先锋语音整理\ow-240426\ZH-conv/all-conv-num-240426.txt', 'a') as output_file:
                    output_file.write(num + '\n')


# # 读取输入文件
# with open(r'F:\守望先锋语音整理\ow-240426\EN/filenames.txt', 'r') as file:
#     for line in file.readlines():
#         if '.0B2' in line:
#             # 获取 num 值
#             num = line.split('.0B2')[0][-12:]
            
#             # 如果 num 不在集合中，说明它是新的
#             if num not in num_set:
#                 # 将 num 添加到集合中
#                 num_set.add(num)
                
#                 # 将 num 写入输出文件
#                 with open(r'F:\守望先锋语音整理\ow-240426\EN/all-vo-num-240426.txt', 'a') as output_file:
#                     output_file.write(num + '\n')