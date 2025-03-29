import os
import sys
import shutil
import ctypes

source_folder = r"C:\Users\r\Desktop\ungoogled-chromium_131.0.6778.85-1.1_windows_x64\ungoogled-chromium_131.0.6778.85-1.1_windows_x64"
destination_folder = r"C:\Program Files\Chromium\Application"

# 检测是否以管理员权限运行
def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

if not is_admin():
    # 重新以管理员权限运行
    print("⚠️ 需要管理员权限，正在重新启动...")
    ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
    sys.exit()

# 确保目标文件夹存在
os.makedirs(destination_folder, exist_ok=True)

# 递归复制并覆盖文件
for root, dirs, files in os.walk(source_folder):
    relative_path = os.path.relpath(root, source_folder)  # 计算相对路径
    target_dir = os.path.join(destination_folder, relative_path)  # 目标目录

    os.makedirs(target_dir, exist_ok=True)  # 创建目标目录

    for file in files:
        src_file = os.path.join(root, file)  # 源文件
        dst_file = os.path.join(target_dir, file)  # 目标文件

        shutil.copy2(src_file, dst_file)  # 复制并覆盖
        print(f"📂 复制 {src_file} -> {dst_file}")

print(f"✅ 成功将 '{source_folder}' 复制并覆盖到 '{destination_folder}'")
