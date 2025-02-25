from config import account, password

# account = "account"
# password = "password"
def run_course_selection()->bool:
    from selenium import webdriver
    from selenium.webdriver.chrome.service import Service
    from selenium.webdriver.chrome.options import Options
    from selenium.common.exceptions import WebDriverException
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from time import sleep
    # 设置 Chrome 选项（可选配置）
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # 无头模式（不显示浏览器界面）
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_experimental_option("detach", True)  # 保持浏览器打开
    try:
        
        service = Service()
        driver = webdriver.Chrome(service=service, options=chrome_options)

        # 访问目标网页
        driver.get("https://xk.nju.edu.cn")

        # 等待输入框可见，然后填入数据
        input_xpath = "/html/body/div[1]/article/section/div[3]/div[1]/div[1]/input"
        input_element = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, input_xpath))
        )
        input_element.send_keys(account)

        # 等待第二个输入框可见，然后填入数据
        input_xpath2 = "/html/body/div[1]/article/section/div[3]/div[1]/div[2]/input"
        input_element2 = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, input_xpath2))
        )
        input_element2.send_keys(password)


        # 获取验证码图片的 src 属性
        image_xpath = "/html/body/div[1]/article/section/div[3]/div[1]/div[3]/img"
        img_element = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, image_xpath))
        )
        img_src = img_element.get_attribute("src")
        print("验证码图片链接:", img_src)



        import ddddocr
        ocr = ddddocr.DdddOcr()
        import requests

        image = requests.get(img_src).content
        result = ocr.classification(image)
        # 等待第二个输入框可见，然后填入数据
        input_xpath3 = "/html/body/div[1]/article/section/div[3]/div[1]/div[3]/input"
        input_element3 = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, input_xpath3))
        )
        input_element3.send_keys(result)

        # 点击登录按钮
        # 点击登录按钮
        button_xpath = "/html/body/div[1]/article/section/div[3]/div[1]/button"
        login_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, button_xpath))
        )
        login_button.click()
        print("已点击登录按钮")   

        # 点击 "开始选课" 按钮
        course_button_xpath = "/html/body/div[1]/article/section/div[3]/div[2]/button"
        course_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, course_button_xpath))
        )
        course_button.click()
        print("已点击 '开始选课' 按钮")

        # 点击 "公共" 标签
        # public_tab_xpath = "/html/body/header/div[2]/ul/li[2]/a"
        # public_tab = WebDriverWait(driver, 10).until(
        #     EC.element_to_be_clickable((By.XPATH, public_tab_xpath))
        # )
        # public_tab.click()
        # print("已点击 '公共' 标签")
            # 等待 "公共" 标签可以点击
        sleep(0.5)
        public_tab_xpath = "/html/body/div[1]/header/div[2]/ul/li[2]/a"
        public_tab = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, public_tab_xpath))
        )
        public_tab.click()
        print("元素 '公共' 可点击，文本为：", public_tab.text)
        # 点击 "公共" 标签后执行的 JavaScript 代码
        js_code = """
        const campus = "仙林校区";  // 校区名称
        const excludedCourseNumbers = ["00372090", "00341420","37100720"];  // 排除的课程号数组
        const xpath = "/html/body/div[3]/div[2]/div[2]/div";  // 目标元素的XPath路径
        const buttonXPath = "/html/body/div[1]/article/div[1]/div[3]/button[2]";  // 按钮的XPath路径

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

            // 遍历所有课程行，寻找匹配的校区且排除特定课程号
            courseRows.forEach(row => {
                // 获取课程号
                const numberCell = row.querySelector("td.kch a.cv-jxb-detail");
                const number = numberCell ? numberCell.getAttribute("data-number") : null;

                // 获取校区
                const campusCell = row.querySelector("td.xq");
                const campusText = campusCell ? campusCell.textContent.trim() : null;

                // 检查是否匹配校区且课程号不在排除列表中
                if (campusText === campus && !excludedCourseNumbers.includes(number)) {
                    // 找到“选择”按钮并点击
                    const choiceButton = row.querySelector("td.cz a.cv-choice");
                    if (choiceButton) {
                        console.log(`找到校区为${campus}的课程，课程号不在排除列表中，正在点击“选择”按钮...`);
                        choiceButton.click();
                    } else {
                        console.log(`找到校区为${campus}的课程，课程号不在排除列表中，但未找到“选择”按钮。`);
                    }
                    found = true;  // 标记找到匹配的课程
                }
            });

            // 如果没有找到匹配的课程
            if (!found) {
                console.log(`未找到校区为${campus}且课程号不在排除列表中的课程。`);
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

        // 每1000ms执行一次selectCourse函数
        setInterval(selectCourse, 1000);

        // 每隔1000ms点击指定按钮
        async function clickButtonPeriodically() {
            try {
                const button = await waitForElement(buttonXPath);
                console.log("找到按钮，正在点击...");
                button.click(); // 触发点击事件
            } catch (error) {
                console.error("按钮未找到或点击失败：", error);
            }
        }

        setInterval(clickButtonPeriodically, 1000);
        """

        # 执行上述 JavaScript 代码
        driver.execute_script(js_code)
        print("已注入并执行 JavaScript 课程选择逻辑代码")
        return True
        # # 打印当前页面标题
        # def run_course_selection(driver):
        #     """
        #     启动定时任务线程，执行课程选择和按钮点击逻辑。
        #     参数:
        #         driver: Selenium WebDriver 对象
        #     """
        #     import threading
        #     import time
        #     from selenium.webdriver.common.by import By
        #     from selenium.webdriver.support.ui import WebDriverWait
        #     from selenium.webdriver.support import expected_conditions as EC

        #     # 参数设置
        #     campus = "仙林校区"  # 校区名称
        #     excluded_course_numbers = ["00372090", "00341420", "37100720"]  # 排除的课程号数组
        #     target_xpath = "/html/body/div[3]/div[2]/div[2]/div"  # 目标元素的XPath路径
        #     button_xpath = "/html/body/div[1]/article/div[1]/div[3]/button[2]"  # 按钮的XPath路径

        #     def wait_for_element(xpath, timeout=10):
        #         """等待指定 XPath 的元素出现，并返回元素对象。"""
        #         return WebDriverWait(driver, timeout).until(
        #             EC.presence_of_element_located((By.XPATH, xpath))
        #         )

        #     def select_course():
        #         """查找课程行，点击符合条件的“选择”按钮，然后等待并点击目标元素。"""
        #         while True:
        #             found = False
        #             try:
        #                 # 查找所有课程行
        #                 course_rows = driver.find_elements(By.CSS_SELECTOR, "tr.course-tr")
        #                 for row in course_rows:
        #                     try:
        #                         number_cell = row.find_element(By.CSS_SELECTOR, "td.kch a.cv-jxb-detail")
        #                         course_number = number_cell.get_attribute("data-number")
        #                     except Exception:
        #                         course_number = None
        #                     try:
        #                         campus_cell = row.find_element(By.CSS_SELECTOR, "td.xq")
        #                         campus_text = campus_cell.text.strip() if campus_cell.text else ""
        #                     except Exception:
        #                         campus_text = ""
        #                     # 检查是否匹配校区且课程号不在排除列表中
        #                     if campus_text == campus and course_number not in excluded_course_numbers:
        #                         try:
        #                             choice_button = row.find_element(By.CSS_SELECTOR, "td.cz a.cv-choice")
        #                             print(f"找到校区为 {campus} 的课程，课程号 {course_number} 不在排除列表中，正在点击“选择”按钮...")
        #                             choice_button.click()
        #                         except Exception as ce:
        #                             print(f"找到匹配的课程，但未找到“选择”按钮。错误：{ce}")
        #                         found = True
        #                 if not found:
        #                     print(f"未找到校区为 {campus} 且课程号不在排除列表中的课程。")
                        
        #                 # 等待目标元素出现，并点击
        #                 try:
        #                     target_element = wait_for_element(target_xpath, timeout=10)
        #                     print("找到目标元素，正在点击...")
        #                     target_element.click()
        #                 except Exception as e:
        #                     print("等待或点击目标元素时出现错误:", e)
        #             except Exception as ex:
        #                 print("select_course 执行异常:", ex)
                    
        #             time.sleep(1)  # 每隔1秒执行一次

        #     def click_button_periodically():
        #         """每隔一定时间点击指定按钮。"""
        #         while True:
        #             try:
        #                 button = wait_for_element(button_xpath, timeout=10)
        #                 print("找到按钮，正在点击...")
        #                 button.click()
        #             except Exception as e:
        #                 print("按钮未找到或点击失败:", e)
        #             time.sleep(1)  # 每隔1秒执行一次

        #     # 启动后台线程定时执行上述两个函数
        #     threading.Thread(target=select_course, daemon=True).start()
        #     threading.Thread(target=click_button_periodically, daemon=True).start()

        #     # 防止主线程退出
        #     while True:
        #         time.sleep(10)

    except WebDriverException as e:
        print("浏览器操作异常:", str(e))

import time

def schedule_run():
    while True:
        try:
            result = run_course_selection()
            if result is True:
                print("run_course_selection 执行成功，等待10分钟后再执行")
                time.sleep(600)  # 10分钟
            else:
                print("run_course_selection 未正确返回，立即重试")
        except Exception as e:
            print("运行过程中出现异常:", e)
            print("立即重新执行...")

if __name__ == "__main__":
    schedule_run()