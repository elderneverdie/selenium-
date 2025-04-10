import pytest
import allure
from selenium.common.exceptions import TimeoutException
from pages.LoginPage import LoginPage


@pytest.mark.run(order=1)
@allure.feature("登录模块")
@allure.story("用户登录失败测试")
def test_user_login_failure(driver):
    with allure.step("1. 使用无效用户凭证尝试登录"):
        login_page = LoginPage(driver)
        login_page.open()
        try:
            login_page.login("kevins", "kevins123")
        except TimeoutException:
            pass  # 预期中的异常

    with allure.step("2. 验证登录失败仍停留在登录页"):
        assert "auth/login" in driver.current_url.lower()


@pytest.mark.run(order=2)
@allure.feature("登录模块")
@allure.story("管理员登录成功测试")
def test_admin_login_success(driver):
    with allure.step("1. 使用有效管理员凭证登录"):
        login_page = LoginPage(driver)
        login_page.open()
        login_page.login("Admin", "admin123")

    with allure.step("2. 验证登录成功后跳转到主页"):
        assert "dashboard/index" in driver.current_url.lower()