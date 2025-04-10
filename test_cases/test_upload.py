import os
import pytest
import allure
from pages.PIMPage import PIMPage


def validate_file(file_path):
    """
    验证文件是否存在、大小是否不超过2M以及格式是否为jpg。
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"文件不存在: {file_path}")

    max_size = 2 * 1024 * 1024  # 2MB
    file_size = os.path.getsize(file_path)
    if file_size > max_size:
        raise ValueError(f"文件大小超过限制（2M）：实际大小 {file_size} 字节")

    if not file_path.lower().endswith('.jpg'):
        raise ValueError(f"文件格式不符合要求，仅支持jpg格式: {file_path}")


@pytest.mark.run(order=3)
@allure.feature("文件上传")
@allure.story("添加新员工，上传图片并填写姓名")
def test_upload(driver):
    pim_page = PIMPage(driver)
    with allure.step("打开 PIM 模块"):
        pim_page.open_pim_module()

    file_path = r'avatar.jpg'
    first_name = "Atest"
    middle_name = "Btest"
    last_name = "Ctest"

    with allure.step("验证上传文件的属性"):
        # 在触发上传操作前，验证文件大小和格式
        validate_file(file_path)

    with allure.step("添加新员工，上传文件并填写姓名信息"):
        pim_page.add_employee(first_name, middle_name, last_name, file_path)

    with allure.step("重新搜索新员工验证添加成功"):
        pim_page.open_pim_module()
        pim_page.search_employee(first_name)
        assert first_name in driver.page_source, "新员工添加失败"
