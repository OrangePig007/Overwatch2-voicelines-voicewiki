import os

def file_rename(path):
    for file in os.listdir(path):
        name = os.path.basename(file)
        name_num = name[0:16]
        name_new = name_num + '_en.ogg'            
        os.rename(os.path.join(path,file),os.path.join(path,name_new))

def extract_name(path):
    for file in os.listdir(path):
        name = os.path.basename(file)
        name_num = name.split("-",1)[0]        
        if len(name.split("-"))==2:           
            name_text = name.split("-",1)[-1][0:-4]
        else:
            name_num=name_num[0:-4]
            name_text = "音效"
        text= "{{OWAudio|File=" + name_num + "_zh.ogg|Script=" + name_text + "}}\n"
        #f.write(text)

path = input("请输入文件夹路径: ")
f = open("D:/1.txt", "w+", encoding='utf-8')
# extract_name(path)
f.close()
print("文本完成")
file_rename(path)
print("重命名完成")