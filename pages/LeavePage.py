from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class LeavePage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    leave_menu = (By.XPATH, '//*[@id="app"]/div[1]/div[1]/aside/nav/div[2]/ul/li[3]/a')

    def open_leave_module(self):
        self.wait.until(EC.element_to_be_clickable(self.leave_menu)).click()

    def is_leave_page_loaded(self):
        """综合验证请假页面加载状态"""
        try:
            # 检查URL特征
            assert "leave" in self.driver.current_url.lower()
            # 检查页面关键元素
            self.wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".oxd-leave-card")))
            return True
        except Exception:
            return False
