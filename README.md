自动化测试评估

一、关键要求
  技术栈: Python + Selenium
  设计模式: 必须使用页面对象模型（POM）
  时限: 2天

  必须包含:
    1.显式等待与断言
    2.错误处理
    3.测试报告（Allure/HTML）（加分项）

二、测试场景
  登录模块
  步骤:
    1.导航到 XXX
    2.以管理员和用户身份登录
    3.验证登录成功

  评估标准:
    元素定位器（ID/XPath/CSS）
    参数化登录
    无效登录处理

  文件上传
  步骤:
    1.进入 XXX → 添加员工
    2.上传头像（.jpg）或简历（.pdf）
    3.验证上传成功

  评估标准:
    处理 input[type="file"]
    文件验证（大小/类型）

  表单与表格验证
  步骤:
    1.在 PIM → 员工列表中搜索员工
    2.编辑并保存联系信息
    3.验证更改

  评估标准:
    动态表格 XPath
    表单字段断言

三、代码结构:
  /tests  
  /pages  
    LoginPage.py  
    PIMPage.py  
    LeavePage.py  
  /test_cases  
    test_login.py  
    test_upload.py  
    test_pim_employee.py  
  conftest.py（配置文件） 
  
