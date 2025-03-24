// 查找所有具有 'ng-star-inserted' 类的元素
const links = document.querySelectorAll('.ng-star-inserted');

// 初始化计数器
let count = 0;

// 输出每个元素第二个子元素的第一个子元素的 href 属性
links.forEach(link => {
    // 获取第二个元素，索引从 0 开始
    const secondElement = link.children[1]; // 第二个子元素的索引是 1
    
    // 获取第二个元素的第一个子元素
    const firstChildOfSecondElement = secondElement ? secondElement.children[0] : null;

    // 如果第二个子元素和其第一个子元素存在，并且第一个子元素有 href 属性
    if (firstChildOfSecondElement && firstChildOfSecondElement.href) {
        console.log(firstChildOfSecondElement.href); // 打印 href 属性
        count++; // 满足条件时递增计数器
    } else {
        console.log("第二个子元素没有 href 属性");
    }
});

// 输出满足条件的数量
console.log(`共有 ${count} 个元素具有 href 属性`);
