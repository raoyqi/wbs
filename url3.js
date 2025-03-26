// 获取所有带有 href 属性的 <a> 标签
var links = document.querySelectorAll('a');

// 创建一个用于存储所有链接的字符串
var linkTexts = '';

// 遍历所有链接并将 href 添加到 linkTexts 字符串中
links.forEach(function(link, index) {
    var href = link.href;  // 获取 href 属性
    if (href) {
        linkTexts += href + '\n';  // 每个链接后加换行符
        console.log(href);  // 在控制台输出链接
    }
});

// 创建一个 Blob 对象用于保存链接到文件
var blob = new Blob([linkTexts], { type: 'text/plain' });

// 创建一个临时的 <a> 元素用于触发文件下载
var link = document.createElement('a');
link.href = URL.createObjectURL(blob);
link.download = 'links1.txt';  // 设置下载文件名

// 触发下载
link.click();

console.log('所有链接已保存到 links.txt 文件中。');
