// 输出每个元素第二个子元素的 href 属性
links = document.querySelectorAll('.ng-star-inserted');

filtered_links = [link for link in links if not link.get_attribute('style')]

filtered_links.forEach(link => {
    // 获取第二个子元素，索引从 0 开始
    console.log(link)
});