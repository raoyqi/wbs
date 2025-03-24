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

