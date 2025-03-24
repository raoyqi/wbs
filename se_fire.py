from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
import time
from selenium.webdriver.common.keys import Keys  # 导入 Keys 类以模拟回车键

# 设置 Firefox 配置（如果需要）
firefox_options = Options()
firefox_options.headless = False  # 设置为 False 以便看到浏览器界面
geckodriver_path = 'geckodriver.exe'  # 这里设置 geckodriver 路径

firefox_options.add_argument('--disable-gpu')
firefox_options.add_argument('--no-sandbox')

# 如果你使用的是特定的 Firefox 版本，也可以指定 Firefox 的二进制位置
firefox_path = r'C:\Users\r\Desktop\firefox\firefox.exe'  # 根据实际路径设置
firefox_options.binary_location = firefox_path

service = Service(executable_path=geckodriver_path, log_path='geckodriver.log')
driver = webdriver.Firefox(service=service, options=firefox_options)

# 打开 Web of Science 链接
url = "https://webofscience.clarivate.cn/wos/alldb/basic-search"
driver.get(url)
time.sleep(5)  # 可以根据需要增加等待时间

try:
    # 使用显示等待 (WebDriverWait) 来等待按钮元素加载并点击
    consent_button = driver.find_element(By.ID, "onetrust-accept-btn-handler")
    consent_button.click()
    print("同意隐私政策按钮已点击。")
except Exception as e:
    print("未找到同意按钮，跳过。")

# 等待页面加载完成

# 查找并输入搜索框
search_box = driver.find_element(By.ID, "search-option")
search_box.send_keys("Convolutional Neural Networks")  # 输入搜索内容

# 模拟按下回车键
search_box.send_keys(Keys.RETURN)

# Define the JavaScript code to be executed
time.sleep(5)
js_code = """
const links = Array.from(document.querySelectorAll('.ng-star-inserted'));
const filteredLinks = links.filter(link => !link.hasAttribute('style'));

// 递归查找元素中是否包含 href 属性
function findHref(element) {
    // 如果元素为空，返回 null
    if (!element) return null;

    const secondElement = element.children[1]; // 第二个子元素的索引是 1

    if (!secondElement) return null;

    const firstChildOfSecondElement = secondElement ? secondElement.children[0] : null;

    if (firstChildOfSecondElement && firstChildOfSecondElement.href) {
        return firstChildOfSecondElement.href; // Return the href value instead of the element
    }

    return null;
}

let foundCount = 0;

for (let link of filteredLinks) {
    const href = findHref(link);

    if (href) {
        foundCount++;  // Increment the found count

        // 如果找到第二个符合条件的链接，则跳出循环并在新窗口打开链接
        if (foundCount === 2) {
            console.log(href); // 打印找到的 href 属性
            window.open(href, '_blank'); // Open the href in a new window/tab
            break; // Stop the loop after opening the second link
        }
    } else {
        console.log("第二个子元素或其子元素没有 href 属性");
    }
}
"""

# Execute the JavaScript code
driver.execute_script(js_code)

# 等待搜索结果加载
time.sleep(5000)

# 关闭浏览器
# driver.quit()
