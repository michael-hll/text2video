import sys
import yaml, subprocess
import shlex
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.remote.webelement import WebElement
from utility import Utility
import time
import random

article_file = './article.yaml'
if len(sys.argv) >= 2:
    article_file = sys.argv[1]

reporters = {
    0: {'name': '慕瑶', 'sex': 'W'},
    1: {'name': '卓妤', 'sex': 'W'},
    2: {'name': '夏青', 'sex': 'W'},
    3: {'name': '蓓瑾', 'sex': 'W'},
    4: {'name': '依丹', 'sex': 'W'},
    5: {'name': '静芙', 'sex': 'W'},
    6: {'name': '梦瑶', 'sex': 'W'},
    7: {'name': '云燕', 'sex': 'W'},
    8: {'name': '廷新', 'sex': 'M'},
    9: {'name': '明泽', 'sex': 'M'},
    10: {'name': '晋龙', 'sex': 'M'},
    11: {'name': '寒云', 'sex': 'M'},
             }    
suggest_reporters = [0,1,2,4,5,7,9]

def exe_command(command):
    command_array = shlex.split(command, posix=True)
    print('Runing command: {0}'.format(command))
    result = subprocess.Popen(command_array, text=True, stdout=sys.stdout, stderr=sys.stderr)
    result.communicate()     
    if result.returncode != 0: 
        print("Running command '{}' failed.".format(command))
    else:
        print("Running command '{}' successfull.".format(command))

def get_init_video(article):
    
    # Using port 9222 (this port could be changed to any port)
    # >>> Google\ Chrome --remote-debugging-port=9222 --user-data-dir='~/ChromeProfile'
    # --auto-open-devtools-for-tabs
    
    # init drivers
    options = Options()
    options.debugger_address = '127.0.0.1:9222'
    # options.add_argument('--incognito')
    # options.add_argument('start-maximized')
    # options.add_argument('auto-open-devtools-for-tabs')
    driver = webdriver.Chrome(service=Service(
        ChromeDriverManager().install()), options=options)
    driver.implicitly_wait(10) # default wait seconds
    driver.switch_to.new_window('tab')
    driver.get('https://zenvideo.qq.com/')
    
    try:
        # get video
        # 数字人播报imageButton
        # src="https://material.gtimg.com/home_tool/dev/nav_virtual.svg
        # img = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH,"//img[contains(@src,'nav_virtual.svg')]")))
        
        img = driver.find_element(
            By.XPATH, "//img[contains(@src,'nav_virtual.svg')]")
        img.click()

        # 随机选择数字人
        # 查看更多数字人
        div = driver.find_element(
            By.XPATH, "//div[contains(@class,'star__more__box___1OtN9')]")
        div.click()

        # 文本驱动对话框
        # 切换到iframe对话框
        WebDriverWait(driver, 10).until(
            EC.frame_to_be_available_and_switch_to_it((By.ID, "ShengkaIframe")))
        time.sleep(2)
        # div = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//div[contains(@class, 'ant-modal-body')]")))
        div = driver.find_element(
            By.XPATH, "//div[contains(@class, 'ant-modal-body')]")
        # 找到第一个按钮: 文本驱动
        # button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.TAG_NAME, "button")))
        button = driver.find_element(By.TAG_NAME, "button")
        time.sleep(0.2)
        button.click()
        time.sleep(3)

        # 数字人设置
        # 找到主要的div
        core_div = driver.find_element(
            By.XPATH, "//div[contains(@class, 'simplebar-content')]")
        buttons = core_div.find_elements(By.TAG_NAME, "button")
        btnGenDraftView = None
        for button in buttons:
            if "画面设置" in button.text:
                btnDigitalManSetting = button
            if "生成预览" in button.text:
                btnGenDraftView = button
            
        # 随机选择一个数字播报员
        select_reporter_index = random.choice(suggest_reporters)   
        line = 'reporter_name={0}'.format(reporters[select_reporter_index]['name']) 
        Utility.write_line_to_file('./reporter.txt', 'w', line)
        #   _1JxXrgZAWgtvq6gz6q99v3            
        divs = driver.find_elements(By.XPATH, "//div[contains(@class, '_1JxXrgZAWgtvq6gz6q99v3')]")
        divs[select_reporter_index].click()
        time.sleep(2)     
        
        # 随机选择一套服装
        #_3LOqC5HR4bvrFTOvsjRykj
        # 点击服装Tab
        divs = driver.find_elements(By.XPATH, "//div[contains(@class, '_3LOqC5HR4bvrFTOvsjRykj')]")
        for div in divs:
            if div.text == "服装":
                div.click()
                time.sleep(2)    
                break    
            
        # 选择衣服和颜色
        #   _1JxXrgZAWgtvq6gz6q99v3            
        divs = driver.find_elements(By.XPATH, "//div[contains(@class, '_1JxXrgZAWgtvq6gz6q99v3')]")
        total = len(divs)
        clothes = 0
        for div in divs:
            # find its parent div
            parent = div.find_element(By.XPATH, '..')
            child_divs = parent.find_elements(By.XPATH, './div')
            clothes = len(child_divs)
            break
        
        cloth_index = random.randrange(0, clothes)
        color_index = random.randrange(clothes, total)
        # 选择衣服
        divs[cloth_index].click()
        time.sleep(2)
        divs = driver.find_elements(By.XPATH, "//div[contains(@class, '_1JxXrgZAWgtvq6gz6q99v3')]")
        # 选择颜色
        divs[color_index].click()
        time.sleep(2)
        
        # 获取弹出对话框的主要div
        divModel = driver.find_element(
            By.XPATH, "//div[contains(@class, 'ant-modal-body')]") \
                .find_element(By.TAG_NAME, 'div')
                
        # 拿到画面设置div
        divs = divModel.find_elements(By.TAG_NAME, "div")
        divHeader = divs[0]
        divHeader.find_elements(By.TAG_NAME, "div")[1].click()
        time.sleep(2)
        
        divModel = driver.find_element(
            By.XPATH, "//div[contains(@class, 'ant-modal-body')]") \
                .find_element(By.TAG_NAME, 'div')
        
        # 自定义按钮
        # _15FKSds2ykmxEZUXdbNY7p
        div = divModel.find_element(By.XPATH, "//div[contains(@class, '_15FKSds2ykmxEZUXdbNY7p')]")
        div.find_elements(By.TAG_NAME, "div")[1].click()
        
        # slice-row-content
        # 设置自定义背景为绿色
        time.sleep(2)
        div = divModel.find_element(By.XPATH, "//div[contains(@class, 'slice-row-content')]") \
            .find_element(By.TAG_NAME, "div")
        divs = div.find_elements(By.TAG_NAME, "div")
        divs[1].click()
        time.sleep(2)
        
        # ant-btn ant-btn-primary
        # 点击完成按钮
        buttons = driver.find_elements(
            By.XPATH, "//button[contains(@class, 'ant-btn ant-btn-primary')]")
        for button in buttons:
            if button.text == "完成":
                button.click()
                time.sleep(2)
        
        # 输入文本
        div = driver.find_element(By.XPATH, "//div[contains(@contenteditable, 'true')]")
        p = div.find_element(By.TAG_NAME, "p")
        script_text = article['hello'] + article['content'] + article['ending']
        driver.execute_script("arguments[0].textContent = arguments[1];", p, script_text)
        
        # 显示字幕按钮
        divs = core_div.find_elements(By.TAG_NAME, 'div')
        for div in divs:
            # print(div.text)
            if "显示字幕" == div.text: 
                buttonShowSubtitle = div.find_element(By.TAG_NAME, "button")
                buttonShowSubtitle.click()
                
        
        # 生成预览
        if btnGenDraftView:
            btnGenDraftView.click()
            time.sleep(2)
        
        # 切换到弹出对话框frame    
        # ant-input
        # 找到视频名称
        #video_name = 'video_init'
        #textBoxVideoName = driver.find_element(By.XPATH, "//input[contains(@class, 'ant-input')]") 
        #for i in range(0, 20):
        #    textBoxVideoName.send_keys(Keys.BACK_SPACE)
        #textBoxVideoName.send_keys(video_name)
        buttons = driver.find_elements(By.TAG_NAME, 'button')
        button = buttons[len(buttons) - 1]
        # 点击生成预览按钮
        button.click()
        
        # 切回到主窗口
        driver.switch_to.parent_frame()
        # https://stackoverflow.com/questions/59130200/selenium-wait-until-element-is-present-visible-and-interactable
        nologo_checkbox = WebDriverWait(driver, 180).until(
            EC.presence_of_element_located((By.XPATH, "//input[contains(@class, 'ant-checkbox-input')]")))       
        nologo_checkbox.click()
        
        # 点击生成视频
        div = driver.find_element(By.XPATH, "//div[contains(@class, 'ant-modal-footer')]")
        buttons = driver.find_elements(By.TAG_NAME, 'button')
        button = buttons[len(buttons) - 1]
        button.click()
        time.sleep(2)
        
        # 找到生成的视频列表并取第一个
        divs = driver.find_elements(By.XPATH, "//div[contains(@class, 'list__box')]")
        
        for div in divs:
            #print(div)
            downDiv = div.find_element(By.XPATH, "//div[contains(@class, 'down__')]")
            while True:
                if downDiv.is_enabled():
                    break
                time.sleep(1)
            
            # 下载
            downDiv.click()
            time.sleep(2)            
            
            # todo: delete 
            # moreDiv = div.find_element(By.XPATH, "//div[contains(@class, 'more__')]")
            # if moreDiv:
            #     moreDiv.click()
            break      
            
    except Exception as e:
        print('=== Exception: ' + str(e))

# reading inputs    
article = Utility.read_yaml_content(article_file)

# get the init video
get_init_video(article)