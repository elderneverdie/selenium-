from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class LoginPage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 15)

    # 页面元素定位器
    username_input = (By.NAME, "username")
    password_input = (By.NAME, "password")
    login_button = (By.XPATH, '//*[@id="app"]/div[1]/div/div[1]/div/div[2]/div[2]/form/div[3]/button')

    def open(self):
        self.driver.get("https://opensource-demo.orangehrmlive.com/web/index.php/auth/login")

    def login(self, username, password):
        user_field = self.wait.until(EC.visibility_of_element_located(self.username_input))
        user_field.clear()
        user_field.send_keys(username)

        pwd_field = self.wait.until(EC.visibility_of_element_located(self.password_input))
        pwd_field.clear()
        pwd_field.send_keys(password)

        # 点击登录按钮
        self.wait.until(EC.element_to_be_clickable(self.login_button)).click()

        # 等待 URL 发生变化，确保登录成功
        self.wait.until(lambda driver: "auth/login" not in driver.current_url.lower())