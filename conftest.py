import pytest
from selenium import webdriver

@pytest.fixture(scope="session")
def driver():
    # 设置 Edge 驱动路径
    edge_driver_path = r'msedgedriver.exe'
    driver = webdriver.Edge(executable_path=edge_driver_path)
    driver.maximize_window()
    yield driver
    driver.quit()
