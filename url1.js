// 获取所有具有 'ng-star-inserted' 类的元素，并将其转换为数组
const links = Array.from(document.querySelectorAll('.ng-star-inserted'));

// 过滤掉包含 style 属性的元素
const filteredLinks = links.filter(link => !link.hasAttribute('style'));

// 用来保存所有找到的 href
const urls = [];

// 遍历过滤后的链接，查找符合条件的 href 属性
for (let link of filteredLinks) {
    // 递归查找元素中是否包含 href 属性
    const element = findHref(link);
    
    if (element) {
        const href = element.querySelector('a')?.href;
        if (href) {
            urls.push(href); // 将找到的 href 添加到数组中
        }
    } else {
        console.log("第二个子元素或其子元素没有 href 属性");
    }
}
urls.shift(); // 也可以使用 urls = urls.slice(1) 来避免改变原始数组
// 如果有找到 URL，创建并下载文件
if (urls.length > 0) {
    const blob = new Blob([urls.join('\n')], { type: 'text/plain' }); // 创建包含所有 URL 的文本文件
    const link = document.createElement('a');
    link.href = URL.createObjectURL(blob); // 创建指向 Blob 的 URL
    link.download = 'urls.txt'; // 设置下载的文件名
    link.click(); // 触发下载
} else {
    console.log('没有找到任何符合条件的 URL');
}

// 递归查找元素中是否包含 href 属性
function findHref(element) {
    // 如果元素为空，返回 null
    if (!element) return null;
    const secondElement = element.children[1]; // 第二个子元素的索引是 1
    
    if (!secondElement) return null;

    const firstChildOfSecondElement = secondElement ? secondElement.children[1] : null;

    if (firstChildOfSecondElement && firstChildOfSecondElement.href) {
        return element;
    }

    return null;
}
