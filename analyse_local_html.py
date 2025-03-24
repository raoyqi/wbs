from bs4 import BeautifulSoup

# 打开并读取下载的 HTML 文件
with open('CNNvideo.html', 'r', encoding='utf-8') as file:
    html_content = file.read()

# 使用 BeautifulSoup 解析 HTML 内容
soup = BeautifulSoup(html_content, 'lxml')

# 查找所有具有 'ng-star-inserted' 类的元素
links = soup.find_all(class_='ng-star-inserted')

# 初始化计数器
count = 0
href_list = []  # 用于存储符合条件的 href

# 遍历所有具有 'ng-star-inserted' 类的元素
for link in links:
    # 获取第二个子元素
    second_child = link.find_all(recursive=False)[1] if len(link.find_all(recursive=False)) > 1 else None

    # 检查第二个子元素是否存在并且有 href 属性
    if second_child and second_child.get('href'):
        href_list.append(second_child['href'])  # 将 href 添加到列表
        count += 1  # 递增计数器
    else:
        print("第二个子元素没有 href 属性")

# 输出符合条件的链接数量
print(f"共有 {count} 个元素具有 href 属性")

# 输出所有符合条件的 href 链接
for href in href_list:
    print(href)

