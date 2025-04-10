from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time


class PIMPage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 15)

    # 导航至 PIM 模块
    pim_menu = (By.XPATH, '//*[@id="app"]/div[1]/div[1]/aside/nav/div[2]/ul/li[2]/a')
    add_employee_button = (By.XPATH, '//*[@id="app"]/div[1]/div[2]/div[2]/div/div[2]/div[1]/button')

    # 新增员工页面元素
    file_input = (By.CSS_SELECTOR, "input[type='file']")
    first_name_input = (By.XPATH,
                        '//*[@id="app"]/div[1]/div[2]/div[2]/div/div/form/div[1]/div[2]/div[1]/div[1]/div/div/div[2]/div[1]/div[2]/input')
    middle_name_input = (By.NAME, "middleName")
    last_name_input = (By.NAME, "lastName")
    save_employee_button = (By.XPATH, '//*[@id="app"]/div[1]/div[2]/div[2]/div/div/form/div[2]/button[2]')

    # 搜索和编辑元素
    employee_search_input = (
    By.XPATH, '//*[@id="app"]/div[1]/div[2]/div[2]/div/div[1]/div[2]/form/div[1]/div/div[1]/div/div[2]/div/div/input')
    search_button = (By.CSS_SELECTOR, "form button[type='submit']")

    def open_pim_module(self):
        self.wait.until(EC.element_to_be_clickable(self.pim_menu)).click()

    def add_employee(self, first, middle, last, file_path):
        self.wait.until(EC.element_to_be_clickable(self.add_employee_button)).click()

        # 上传文件
        file_input_elem = self.wait.until(EC.presence_of_element_located(self.file_input))
        file_input_elem.send_keys(file_path)

        # 填写姓名信息
        first_name_elem = self.wait.until(EC.visibility_of_element_located(self.first_name_input))
        first_name_elem.clear()
        first_name_elem.send_keys(first)

        middle_name_elem = self.wait.until(EC.visibility_of_element_located(self.middle_name_input))
        middle_name_elem.clear()
        middle_name_elem.send_keys(middle)

        last_name_elem = self.wait.until(EC.visibility_of_element_located(self.last_name_input))
        last_name_elem.clear()
        last_name_elem.send_keys(last)

        self.wait.until(EC.element_to_be_clickable(self.save_employee_button)).click()
        # 等待新增员工表单关闭，说明保存成功
        self.wait.until(EC.invisibility_of_element_located(self.first_name_input))

    def search_employee(self, employee_name):
        search_field = self.wait.until(EC.visibility_of_element_located(self.employee_search_input))
        search_field.clear()
        search_field.send_keys(employee_name)
        self.wait.until(EC.element_to_be_clickable(self.search_button)).click()
        # 等待表格加载，确保至少出现一条记录
        self.wait.until(EC.presence_of_all_elements_located(("class name", "oxd-table-row")))

    def edit_employee_last_name(self, employee_name, new_last_name):
        # 1. 在列表中定位目标员工所在行
        target_row_xpath = f"//div[contains(@class, 'oxd-table-row') and .//div[contains(text(), '{employee_name}')]]"
        target_row = self.wait.until(
            EC.presence_of_element_located(("xpath", target_row_xpath)),
            message=f"未找到员工 {employee_name} 的记录"
        )

        # 2. 点击该行中的编辑按钮
        edit_button_xpath = ".//i[contains(@class, 'bi-pencil-fill')]"
        edit_button = target_row.find_element_by_xpath(edit_button_xpath)
        try:
            edit_button.click()
        except Exception:
            self.driver.execute_script("arguments[0].click();", edit_button)

        # 3. 在编辑页面中等待“lastname”输入框可点击
        last_name_field = self.wait.until(
            EC.element_to_be_clickable(self.last_name_input),
            message="编辑页面中姓氏输入框不可点击或未加载完成"
        )

        time.sleep(3)

        # 4. 清除原有内容，并输入编辑后的内容
        last_name_field.clear()
        last_name_field.send_keys(new_last_name)

        time.sleep(3)

        # 5. 定位并点击编辑页面中的“save”按钮
        save_button_locator = (
        By.XPATH, '//*[@id="app"]/div[1]/div[2]/div[2]/div/div/div/div[2]/div[1]/form/div[4]/button')
        save_button = self.wait.until(
            EC.element_to_be_clickable(save_button_locator),
            message="编辑页面保存按钮不可点击"
        )
        save_button.click()

        # 6. 等待保存后，重新定位 lastname 输入框，并断言其内容是否与 new_last_name 相等
        #使用 assert 进行断言
        actual_value = self.driver.find_element(*self.last_name_input).get_attribute("value")
        assert new_last_name in actual_value, f"表单中lastName字段断言失败，预期应包含：{new_last_name}，实际：{actual_value}"

    def is_employee_visible(self, name_fragment):
        """检查员工是否出现在列表中"""
        try:
            target_row = (By.XPATH, f"//div[contains(@class, 'oxd-table-row') and contains(., '{name_fragment}')]")
            self.wait.until(EC.visibility_of_element_located(target_row))
            return True
        except TimeoutException:
            return False

    def verify_last_name_updated(self, expected_last_name):
        """验证姓氏输入框值包含预期内容"""
        last_name_field = self.wait.until(
            EC.visibility_of_element_located(self.last_name_input),
            message="姓氏输入框不可见"
        )
        actual_value = last_name_field.get_attribute("value")
        assert expected_last_name in actual_value, \
            f"姓氏验证失败，预期应包含: {expected_last_name}, 实际值: {actual_value}"
