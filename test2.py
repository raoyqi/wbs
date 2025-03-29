import time
from bs4 import BeautifulSoup
import os
def extract_and_insert_multiple(file1, output_file, start, end):
    # 读取第一个 HTML 文件
    with open(file1, "r", encoding="utf-8") as f1:
        html1 = f1.read()
    
    # 使用 BeautifulSoup 解析第一个 HTML
    soup1 = BeautifulSoup(html1, "html.parser")

    # 找到第一个文件中的 <app-records-list> 元素
    app_records_list = soup1.find("app-records-list")

    # 如果 <app-records-list> 元素存在
    if app_records_list:
        # 记录开始时间
        start_time = time.time()

        # 遍历第二个 HTML 文件，提取 <app-record> 元素并插入到第一个 HTML 文件中
        for i in range(start, end + 1):
            file2 = f"C:\\Users\\r\\Desktop\\webofsci\\test_webofsci\\ConvolutionalNeuralNetworks_{i}.html"
            try:
                # 记录每个文件处理的开始时间
                file_start_time = time.time()

                # 读取第二个 HTML 文件
                with open(file2, "r", encoding="utf-8") as f2:
                    html2 = f2.read()

                # 使用 BeautifulSoup 解析第二个 HTML 文件
                soup2 = BeautifulSoup(html2, "html.parser")

                # 提取第二个文件中的所有 <app-record> 元素
                app_records = soup2.find_all("app-record")

                # 将所有的 <app-record> 元素添加到 <app-records-list> 中
                for record in app_records:
                    app_records_list.append(record)

                # 计算当前文件的处理时间并打印
                file_end_time = time.time()
                file_duration = file_end_time - file_start_time
                print(f"Processed file {i}, time taken: {file_duration:.2f} seconds.")

            except FileNotFoundError:
                print(f"Warning: {file2} not found, skipping this file.")

            progress = (i - start + 1) / (end - start + 1) * 100
            print(f"Progress: {i - start + 1}/{end - start + 1} files processed ({progress:.2f}%).")

        # 将合并后的 HTML 写入新的文件
        with open(output_file, "w", encoding="utf-8") as out:
            out.write(str(soup1))

        # 计算总时间并打印
        end_time = time.time()
        total_duration = end_time - start_time
        print(f"\nApp records have been successfully extracted and inserted. The new HTML is saved to {output_file}")
        print(f"Total time taken: {total_duration:.2f} seconds.")

    else:
        print("Error: <app-records-list> not found in the first HTML.")

def process_in_batches(total_files, batch_size):
    # 计算批次数量
    batches = (total_files - 1) // batch_size + 1
    
    for batch_num in range(batches):
        start = batch_num * batch_size + 1
        end = min((batch_num + 1) * batch_size, total_files)
        
        # 根据批次号设置第一个 HTML 文件的路径
        file1 = f"C:\\Users\\r\\Desktop\\test_webofsci\\test_webofsci\\ConvolutionalNeuralNetworks_{start}.html"
        
        # 输出文件名
        output_file = f"C:\\Users\\r\\Desktop\\test_webofsci\\merged\\ConvolutionalNeuralNetworks_{start}-{end}.html"
        
        # 打印批次信息
        print(f"\nProcessing files {start} to {end}...")

        # 调用处理函数
        extract_and_insert_multiple(file1, output_file, start, end)


def count_files_scandir(directory_path):
    return len([entry for entry in os.scandir(directory_path) if entry.is_file()])

directory_path="test_webofsci"
total_files = count_files_scandir(directory_path)  # 假设你有 100 个 HTML 文件
batch_size = 10  

process_in_batches(total_files, batch_size)
