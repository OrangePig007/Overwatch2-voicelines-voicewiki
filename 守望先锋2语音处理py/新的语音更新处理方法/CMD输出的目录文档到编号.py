# 用集合存储已处理的 num 以避免重复
#dir /b /s > filelist.txt

num_set = set()

# # 对话---读取输入文件
# with open(r'D:\ow-240826\对话(en)/filelist.txt', 'r') as file:
#     for line in file.readlines():
#         if '.0D0' in line:
#             # 获取 num 值
#             num = line.split('.0D0')[0][-12:]
            
#             # 如果 num 不在集合中，说明它是新的
#             if num not in num_set:
#                 # 将 num 添加到集合中
#                 num_set.add(num)
                
#                 # 将 num 写入输出文件
#                 with open(r'守望先锋2语音处理py\新的语音更新处理方法\all-conv-num-240426.txt', 'a+') as output_file:
#                     output_file.write(num + '\n')


# 语音---读取输入文件
with open(r'G:\守望语音\ow-freja-ver\upload/filelist.txt', 'r') as file:
    for line in file.readlines():
        if '.0B2' in line:
            # 获取 num 值
            num = line.split('.0B2')[0][-12:]
            
            # 如果 num 不在集合中，说明它是新的
            if num not in num_set:
                # 将 num 添加到集合中
                num_set.add(num)
                
                # 将 num 写入输出文件
                with open(r'守望先锋2语音处理py\新的语音更新处理方法\all-vo-num-240827.txt', 'a+') as output_file:
                    output_file.write(num + '\n')