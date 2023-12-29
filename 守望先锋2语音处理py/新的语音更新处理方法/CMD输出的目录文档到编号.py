with open('E:\QQ文件/1005ow.txt', 'r') as file:
    for line in file.readlines():
        if '.0B2' in line:
            num = line.split('.0B2')[0][-12:]
            
            # Writing num to another text file
            with open('E:\守望先锋毛加版本语音\py/old_num_file.txt', 'a') as output_file:
                output_file.write(num + '\n')
