本着授人以鱼不如授人以渔的思想，加上可能后续网页有更改，为便于用户修改，这里详细记录了脚本的开发过程，供后来者参考使用。


# Hello World

[示例网页](https://pojisloancalculator.netlify.app/)，这是一个我自己开发用于进行简单的数学计算的网页，结构比较简单，我们就拿它测试。

下面，让我们模拟点击那个叫”计算“的按钮吧。
请把下面这段代码复制到浏览器的控制台中，然后按回车键运行。
```javascript
const calcButton = Array.from(document.querySelectorAll('button')).find(btn => btn.textContent.trim() === '计算');

calcButton.click();
```
好了，你已经掌握了javascript脚本开发了，接下来就可以开发一个自动点击选课的脚本了。
# 点击”确认“
然后选择一个幸运AI，让它生成一段已知按钮XPath点击它的代码
```javascript
// 使用XPath选择目标元素
var element = document.evaluate(
    "/html/body/div[3]/div[2]/div[2]/div[1]",  // 你的XPath路径
    document,
    null,
    XPathResult.FIRST_ORDERED_NODE_TYPE,
    null
).singleNodeValue;

// 检查是否找到元素
if (!element) {
    console.log("未找到元素，请检查XPath路径是否正确！");
} else {
    // 检查元素的类名、data-type属性和文本内容
    if (
        element.classList.contains("cv-sure") &&
        element.classList.contains("cvBtnFlag") &&
        element.getAttribute("data-type") === "sure" &&
        element.textContent.trim() === "确认"
    ) {
        console.log("元素符合预期，正在点击...");
        element.click();  // 触发点击事件
    } else {
        console.log("元素不符合预期，请检查元素的属性和内容。");
    }
}
```

# 根据课程号选课
现在我们已经知道了弹出对话框后点击确认按钮的方法了，接下来还有一个工作，就是
```javascript
// 定义要查找的课程号和校区
const courseNumber = "78005960";  // 课程号
const campus = "苏州校区";  // 校区名称

// 查找所有课程行
const courseRows = document.querySelectorAll("tr.course-tr");

// 标记是否找到匹配的课程
let found = false;

// 遍历所有课程行，寻找匹配的课程号和校区
courseRows.forEach(row => {
    // 获取课程号
    const numberCell = row.querySelector("td.kch a.cv-jxb-detail");
    const number = numberCell ? numberCell.getAttribute("data-number") : null;

    // 获取校区
    const campusCell = row.querySelector("td.xq");
    const campusText = campusCell ? campusCell.textContent.trim() : null;

    // 检查是否匹配
    if (number === courseNumber && campusText === campus) {
        // 找到“选择”按钮并点击
        const choiceButton = row.querySelector("td.cz a.cv-choice");
        if (choiceButton) {
            console.log(`找到课程号为${courseNumber}且校区为${campus}的课程，正在点击“选择”按钮...`);
            choiceButton.click();
        } else {
            console.log(`找到课程号为${courseNumber}且校区为${campus}的课程，但未找到“选择”按钮。`);
        }
        found = true;  // 标记找到匹配的课程
    }
});

// 如果没有找到匹配的课程
if (!found) {
    console.log(`未找到课程号为${courseNumber}且校区为${campus}的课程。`);
}
```