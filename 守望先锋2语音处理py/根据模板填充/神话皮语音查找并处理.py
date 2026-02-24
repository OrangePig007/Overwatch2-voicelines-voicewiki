import os
import shutil
import subprocess
import tempfile
import re

# 定义目录路径
zh_dir = r"G:\守望语音\ow-lupa-ver\ZHS"
en_dir = r"G:\守望语音\ow-lupa-ver\EN"
target_dir = r"G:\守望语音\ow-lupa-ver\待上传"
doc_path = r"G:\守望语音\ow-lupa-ver\mythic-og.txt"  # 修改为你的文档路径
es_exe_path = r'C:\Program Files\Everything\es.exe'  # es.exe的路径

def extract_serial_numbers():
    """从文档中提取符合格式的序号：12个字母/数字 + .0B2 并去重"""
    # 优化正则表达式，专门匹配类似"000000069468.0B2"的格式
    # 考虑到序号出现在"Media:"之后，增加了这一匹配条件
    pattern = r'([A-F0-9]{12}\.0B2)'
    
    try:
        # 读取文件内容
        with open(doc_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
        
        # 查找所有匹配的序号
        matches = re.findall(pattern, content, re.IGNORECASE)
        
        # 去除重复项并保持顺序
        unique_numbers = []
        seen = set()
        for num in matches:
            if num not in seen:
                seen.add(num)
                unique_numbers.append(num)
        
        print(f"成功提取 {len(unique_numbers)} 个不重复的序号")
        # 显示提取的序号列表，方便验证
        print("提取的序号列表：")
        for i, num in enumerate(unique_numbers[:10]):  # 只显示前10个
            print(f"{i+1}. {num}")
        if len(unique_numbers) > 10:
            print(f"... 还有 {len(unique_numbers)-10} 个序号")
        
        return unique_numbers
        
    except FileNotFoundError:
        print(f"错误：未找到文档 {doc_path}")
        return []
    except Exception as e:
        print(f"处理文档时发生错误：{str(e)}")
        return []

def search_files_with_es(es_path, search_term, search_dir):
    """使用es.exe搜索包含指定序号的文件"""
    # 创建临时文件来存储搜索结果
    with tempfile.NamedTemporaryFile(mode='w+', delete=False, suffix='.txt') as temp_file:
        temp_txt_path = temp_file.name
    
    try:
        # 构建搜索命令，使用精确匹配提高准确性
        command = f'"{es_path}" "{search_term}" -path "{search_dir}" -export-txt "{temp_txt_path}" -name'
        subprocess.run(command, shell=True, check=True)
        
        # 读取搜索结果
        with open(temp_txt_path, 'r', encoding='utf-8') as f:
            results = [line.strip() for line in f if line.strip()]
        
        return results
    except subprocess.CalledProcessError as e:
        print(f"搜索命令执行失败: {e}")
        return []
    except Exception as e:
        print(f"搜索文件时发生错误: {str(e)}")
        return []
    finally:
        # 清理临时文件
        if os.path.exists(temp_txt_path):
            try:
                os.remove(temp_txt_path)
            except:
                pass

def copy_and_rename_files():
    # 确保目标目录存在，如果不存在则创建
    os.makedirs(target_dir, exist_ok=True)
    
    # 从文档中提取序号列表
    serial_numbers = extract_serial_numbers()
    if not serial_numbers:
        print("没有提取到有效的序号，无法继续操作")
        return
    
    # 遍历每个序号并处理
    for num in serial_numbers:
        print(f"\n处理序号: {num}")
        
        # 提取前12个字符作为基础名称
        name_num = num[0:12]
        
        # 构建新的文件名
        zh_new_name = f"{name_num}.0B2_zh.ogg"
        en_new_name = f"{name_num}.0B2_en.ogg"
        
        # 搜索中文目录中的文件
        zh_files = search_files_with_es(es_exe_path, num, zh_dir)
        if zh_files:
            # 取第一个搜索结果
            zh_source = zh_files[0]
            zh_target = os.path.join(target_dir, zh_new_name)
            shutil.copy2(zh_source, zh_target)
            print(f"已复制中文文件：{os.path.basename(zh_source)} -> {zh_new_name}")
        else:
            print(f"警告：在中文目录未找到包含序号 {num} 的文件")
        
        # 搜索英文目录中的文件
        en_files = search_files_with_es(es_exe_path, num, en_dir)
        if en_files:
            # 取第一个搜索结果
            en_source = en_files[0]
            en_target = os.path.join(target_dir, en_new_name)
            shutil.copy2(en_source, en_target)
            print(f"已复制英文文件：{os.path.basename(en_source)} -> {en_new_name}")
        else:
            print(f"警告：在英文目录未找到包含序号 {num} 的文件")
    
    print("\n所有文件处理完成")

if __name__ == "__main__":
    # 检查es.exe是否存在
    if not os.path.exists(es_exe_path):
        print(f"错误：未找到es.exe文件，请检查路径是否正确：{es_exe_path}")
    else:
        # 检查文档是否存在
        if not os.path.exists(doc_path):
            print(f"错误：未找到文档文件，请检查路径是否正确：{doc_path}")
        else:
            copy_and_rename_files()
    