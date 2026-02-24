import os
import shutil
from tqdm import tqdm

# --- 在这里配置你的路径 ---
SOURCE_DIR = r"G:\守望语音\ow-domina-ver\EN-NPC\NPCVoice\Emre"  # 原始文件夹
TARGET_DIR = r"G:\守望语音\ow-domina-ver\upload\传"  # 目标文件夹
# -----------------------

def get_all_files(source_path):
    """预先获取所有文件列表，用于计算总数"""
    file_list = []
    for root, dirs, files in os.walk(source_path):
        for file in files:
            file_list.append(os.path.join(root, file))
    return file_list

def process_files(file_list, target_path):
    """处理文件复制与重命名"""
    # 使用 tqdm 创建进度条
    for current_full_path in tqdm(file_list, desc="同步进度", unit="file"):
        # 获取文件名
        file = os.path.basename(current_full_path)
        
        # --- 提取并处理文件名逻辑 ---
        # 取前16位 + '_en.ogg'
        name_num = file[0:16]
        new_filename = name_num + '_en.ogg'
        
        # 目标完整路径
        dest_full_path = os.path.join(target_path, new_filename)
        
        # 执行复制
        shutil.copy(current_full_path, dest_full_path)

if __name__ == "__main__":
    # 检查源目录
    if not os.path.exists(SOURCE_DIR):
        print(f"错误: 找不到源目录 {SOURCE_DIR}")
    else:
        # 创建目标目录
        if not os.path.exists(TARGET_DIR):
            os.makedirs(TARGET_DIR)
            print(f"创建目标目录: {TARGET_DIR}")

        print("正在扫描文件...")
        all_files = get_all_files(SOURCE_DIR)
        total_count = len(all_files)
        
        if total_count == 0:
            print("源目录中没有文件。")
        else:
            print(f"找到 {total_count} 个文件，准备开始...")
            process_files(all_files, TARGET_DIR)
            print("\n任务完成！")