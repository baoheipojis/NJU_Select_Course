const courseNumber = "00372090";  // 课程号
const campus = "仙林校区";  // 校区名称
const xpath = "/html/body/div[3]/div[2]/div[2]/div";  // 目标元素的XPath路径

// 定义一个函数用于通过XPath选择元素
function getElementByXPath(xpath) {
    const result = document.evaluate(
        xpath,
        document,
        null,
        XPathResult.FIRST_ORDERED_NODE_TYPE,
        null
    );
    return result.singleNodeValue;
}

// 定义一个函数用于阻塞等待目标元素出现
function waitForElement(xpath) {
    return new Promise((resolve) => {
        const interval = setInterval(() => {
            const targetElement = getElementByXPath(xpath);
            if (targetElement) {
                clearInterval(interval); // 停止轮询
                resolve(targetElement); // 解决Promise，返回目标元素
            }
        }, 100); // 每100毫秒检查一次
    });
}

// 定义一个函数用于执行课程选择逻辑
async function selectCourse() {
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

    // 等待目标元素出现
    try {
        const targetElement = await waitForElement(xpath);
        console.log("找到目标元素，正在点击...");
        targetElement.click(); // 触发点击事件
    } catch (error) {
        console.error("出现错误：", error);
    }
}

// 每10ms执行一次selectCourse函数
setInterval(selectCourse, 100);