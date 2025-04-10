import pytest
import allure
from pages.PIMPage import PIMPage
from pages.LeavePage import LeavePage


@pytest.mark.run(order=4)
@allure.feature("PIM模块")
@allure.story("搜索编辑员工并跳转到请假模块")
def test_pim_employee(driver):
    pim_page = PIMPage(driver)
    new_last_name = "editlastname"

    with allure.step("刷新并打开 PIM 模块，搜索新增员工"):
        pim_page.open_pim_module()
        pim_page.search_employee("Atest")

    with allure.step("编辑员工姓氏"):
        # 确保目标存在后再编辑
        assert pim_page.is_employee_visible("Atest"), "目标员工未出现在列表中"
        pim_page.edit_employee_last_name("Atest", new_last_name)

    with allure.step("验证编辑后的员工信息"):
        # 直接验证输入框值
        pim_page.verify_last_name_updated(new_last_name)

    with allure.step("访问请假模块"):
        leave_page = LeavePage(driver)
        leave_page.open_leave_module()

    with allure.step("验证请假模块页面是否成功打开"):
        assert "leave" in driver.current_url.lower(), "请假模块URL验证失败"
