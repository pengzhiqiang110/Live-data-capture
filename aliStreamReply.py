import gc
import os.path
from time import sleep

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import StaleElementReferenceException

from autoReplay import AutoRelay
import db, asyncio
import random
# from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service as ChromeService
import logging

os.environ["OPENAI_API_KEY"] = "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"

# 内存泄露检测
import objgraph
import psutil
from pympler import tracker, muppy, summary
import guppy
tr = tracker.SummaryTracker()
hp = guppy.hpy() # 初始化了SessionContext，使用它可以访问heap信息


# 设置msedgedriver的路径
options = webdriver.ChromeOptions()
    
# 保持浏览器打开状态
options.add_experimental_option("detach", True)

# 无头模式
options.add_argument("--headless") 

# 调试内存变量


messageList = ["欢迎新进直播间的宝子们，咱们家是袋鼠官方首次入驻支付宝！秋冬福利看过来！",
                   "欢迎新进直播间的宝子们,咱们家是中国袋鼠官方首次入驻支付宝平台，暖冬福利限时放送！"]

logger = logging.getLogger('aliStreamReply')

def getDriver():
    # driver = webdriver.Edge(options=options)
    driver = webdriver.Chrome(options=options)
    # driver = webdriver.Chrome(ChromeDriverManager().install(),options=options)
    driver.maximize_window()
    # driver.get('https://b.alipay.com/page/live-console/detail/A202311274086601600001099?appId=2030093915638103')
    driver.get("https://b.alipay.com/page/live-console")
    driver.delete_all_cookies()
    return driver


def getQrcode(qr_path, bot):
    # 截屏抓取二维码
    try:
        recode = WebDriverWait(bot.driver, 60).until(
            # barcoce 外面一层J-qrcode-img barcode
            EC.presence_of_element_located((By.CLASS_NAME, 'barcode'))
        )
        # 如果qr_path上一级目录不存在，则创建
        if not os.path.exists(os.path.dirname(qr_path)):
            os.makedirs(os.path.dirname(qr_path))
        recode.screenshot(qr_path)
    except TimeoutException:
        logger.error(f"获取二维码失败")
        return None

async def auth(bot : db.Bot = None):
# def auth(bot : db.Bot = None):
    # 等待商家扫码登录  由于以上操作需要时间，所以这一步会等待 120s，如果超时了，则商家需要重新请求开启bot
    # driver.refresh()
    qr_path = "./data/shopname-botid/qrcode/qr_code.png"
    if bot != None:
        qr_path = bot.get_live_qrcode_path()
    while True:
        if os.path.exists(qr_path):
            os.remove(qr_path)
        getQrcode(qr_path, bot)
        if os.path.exists(qr_path):
            logger.info("二维码地址：%s", qr_path)
            await asyncio.sleep(30)
            break
        await asyncio.sleep(30)

def del_qrcode(bot : db.Bot = None):
    # 删除二维码
    qr_path = "./data/shopname-botid/qrcode/qr_code.png"
    if bot != None:
        qr_path = bot.get_live_qrcode_path()
    if os.path.exists(qr_path):
        os.remove(qr_path)

async def select_shop(bot : db.Bot = None):
    shopper_id = "2088741204488103"
    shopper_name = ""
    driver = bot.driver
    if bot != None:
        shopper_id = bot.get_shopper_id()
        shopper_name = bot.get_shopper_name()
    try:
        shopTab = WebDriverWait(bot.driver, 40).until(
            EC.presence_of_element_located(
                (By.XPATH, '//div[@data-aspm-param="principalId='+shopper_id+'"]')
            )
        )
        if shopTab is not None:
            logger.info("选择商户 %s", shopTab.text)
            shopTab.click()
            del_qrcode(bot)
        await asyncio.sleep(20)
    except TimeoutException:
        logger.error(f"选择商户号失败,重新搜索")
        # ant-pagination-item-link 多页的时候下一页的class  disabled 是否可以点击
        # ant-input 搜索商户输入框
        # ant-input-group-addon 搜索商户确定按钮
        searchInput = WebDriverWait(bot.driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, '//input[@class="ant-input"]')
            )
        )
        searchButton = WebDriverWait(bot.driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, '//span[@class="ant-input-group-addon"]')
            )
        )
        reply(None,searchInput,searchButton,shopper_name)
        shopTab = WebDriverWait(bot.driver, 20).until(
            EC.presence_of_element_located(
                (By.XPATH, '//div[@data-aspm-param="principalId='+shopper_id+'"]')
            )
        )
        if shopTab is not None:
            logger.info("选择商户 %s", shopTab.text)
            shopTab.click()
            del_qrcode(bot)
            await asyncio.sleep(20)
        else:
            return None


async def open_live(bot : db.Bot = None):
# def open_live(bot : db.Bot = None):
    # 进入指定的直播间
    driver = bot.driver
    driver.execute_script("window.open('');")
    all_windows = driver.window_handles
    driver.close()
    # 切换到新打开的窗口
    driver.switch_to.window(all_windows[1])
    live_url = "https://b.alipay.com/page/live-console/detail/A202311284101468101001099?appId=2030093915638103"
    if bot != None:
        live_url = bot.get_live_url()
    driver.get(live_url)
    # current_window = driver.current_window_handle
    # driver.switch_to.window(all_windows[0])
    # driver.close()
    # driver.switch_to.window(current_window)


def getInputBox(driver):
    # 定位网页聊天输入框
    try:
        input_box = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, '//textarea[@class="ant-input cmtField___gwWD0"]')
            )
        )
        logger.debug("获取输入框成功")
        return input_box
    except TimeoutException as e:
        logger.error("获取输入框失败")
        return None


def getInteractBox(driver):
    # 聊天及其他消息
    try:
        username_box = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                    (By.XPATH, "(//span[@class='userName___xHJUj userNameCanHover___D89if'])[last()]")
            )
        )

        message_box = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, "(//span[@class='cmtContent___w4tVa'])[last()]")
            )
        )
        logger.debug("获取用户发送的消息成功")
        return username_box, message_box
    except TimeoutException as e:
        logger.info("获取用户发送的消息失败")
        return None,None 

def getIncomingUserNameBox(driver):
    # 新进直播间消息
    try:
        incoming_user_box = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, "(//span[@class='roomUserStyle___ZRyLt'])[last()]")
            )
        )
        logger.debug("获取新进直播间用户成功")
        return incoming_user_box
    except TimeoutException as e:
        logger.info("获取新进直播间用户失败")
        return None 


def getSendButton(driver):
    # 发送按钮
    try:
        send_button = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (
                    By.XPATH,
                    '//button[@class="ant-btn ant-btn-primary ant-btn-sm cmtBtn___K7NWO"]',
                )
            )
        )
        logger.debug("获取发送按钮成功")
        return send_button
    except TimeoutException as e:
        logger.error("获取发送按钮失败")
        return None #f"获取发送按钮失败:{str(e)}"

# 定位直播间弹幕互动消息框，并发送消息
def reply(autoReplay, input_box, send_button, msg):
    if autoReplay != None:
        msgReplay = autoReplay.getAutoReplay(msg)
    else:
        msgReplay = msg
    input_box.send_keys(msgReplay)
    if send_button != None:
       logger.debug("发送消息成功 %s:", msgReplay)
       send_button.click()

# 获取直播状态
def getLiveState(bot : db.Bot = None):
    # current_url = driver.current_url
    # if current_url != live_url:
    #     driver.get(live_url)
    driver = bot.driver
    shopper_id = bot.get_shopper_id()
    try:
        logger.debug("获取直播状态")
        live_state_button = WebDriverWait(bot.driver, 50).until(
            EC.presence_of_element_located(
                (By.XPATH, '//button[@class="ant-btn ant-btn-primary ant-btn-dangerous"]')
            )
        )
        live_state = live_state_button.text
        # API -> db更新直播状态
        if live_state == "结束直播":
            db.set_live_status(shopper_id, 1)
        else:
            db.set_live_status(shopper_id, 0)
        logger.debug("直播中")
        return live_state
    except TimeoutException as e:
        logger.info("未开启直播或直播url不正确")
        return None  #f"未直播或获取直播状态失败:{e}"
    
def getBotStatus(bot : db.Bot = None):
    # API -> db获取bot状态
    bot_status = db.get_bot_status(bot.get_id())
    return bot_status


async def message_replay(bot : db.Bot = None):
    driver = bot.driver
    LAST_INCOMING_USER_MESSAGE = ""
    LAST_INTERACT_MESSAGE = ""
    autoReplay = AutoRelay(bot)
    # 循环获取弹幕互动消息内容
    while True:
        # action
        # 如果直播间关闭，或用户关闭bot,则停止
        logger.info("------------------"*4)
        logger.debug("开始循环抓取聊天记录")
        live_state = getLiveState(bot) 
        if live_state == None or getBotStatus(bot) == 0:
            if getBotStatus(bot) == 0:
                logger.info("用户主动停止 bot")
            if live_state == None:
                logger.info("用户关闭直播间")
                db.update_bot_status(bot.get_id(), 0)
            logger.info("即将退出bot")
            break;
        logger.debug("直播间机器人已开启")
        db.update_bot_status(bot.get_id(), 2)
        # 从弹幕互动消息框中获取弹幕互动消息内容
        input_box = getInputBox(driver)
        send_button = getSendButton(driver)
        username_box, message_box = getInteractBox(driver)
        incoming_user_box = getIncomingUserNameBox(driver)

        if input_box == None or send_button == None:
            logger.warning("输入框或发送按钮未获取")
            continue

        if message_box != None and username_box != None and username_box.text != '主播助理：':
            logger.info("用户昵称:%s 消息: %s", username_box.text, message_box.text)
            if message_box.text != LAST_INTERACT_MESSAGE:
                reply(autoReplay, input_box, send_button,message_box.text)
                LAST_INTERACT_MESSAGE = message_box.text

        # 欢迎新用户
        if incoming_user_box != None:
            is_execute = random.choice([True] * 1 + [False] * 9)
            if is_execute and incoming_user_box.text != LAST_INCOMING_USER_MESSAGE:
                logger.info("新用户提示 %s", incoming_user_box.text)
                # print("新用户提示", incoming_user_box.text)
                LAST_INCOMING_USER_MESSAGE = incoming_user_box.text
                random_execute = random.choice([True, False])
                if random_execute:
                    incoming_send_message(input_box, send_button)
                else:
                    incoming_send_message_user(incoming_user_box, input_box, send_button)

        # 检查内存泄露
        is_check_property = random.choice([True] * 1 + [False]* 0)
        if is_check_property:
            #查看有无内存泄露
            # objgraph.show_most_common_types()  # 打印最常见的对象类型及其数量
            #CPU监控
            # print(f"CPU的逻辑数量:{psutil.cpu_count()}")  # 12
            # print(f"CPU的物理核心数量:{psutil.cpu_count(logical=False)}")  # 6
            # print(f"CPU的统计信息:{psutil.cpu_stats()}")
            # print(f"CPU的使用频率:{psutil.cpu_freq()}")
            #内存情况 total: 总内存 available: 可用内存 percent: 内存使用率 used: 已使用的内存
            # print(f"内存使用情况:{psutil.virtual_memory()}")
            logger.debug("内存使用情况:%s", psutil.virtual_memory())
            # print ("memory total")
            # all_objects = muppy.get_objects()
            # sum1 = summary.summarize(all_objects)
            # summary.print_(sum1)
            # print ("memory difference")
            # tr.print_diff()
            logger.debug("memory difference %s", tr.print_diff())
            # print("heap total")
            # heap = hp.heap() # 返回heap内存详情
            # references = heap[0].byvia # byvia返回该对象的被哪些引用， heap[0]是内存消耗最大的对象
            # print(references)
            # print(references[0].kind)
            # print(references[0].shpaths)
            # print(references[0].rp)
            # print(f"交换内存信息:{psutil.swap_memory()}")
            #磁盘相关
            # print(f"磁盘使用情况:{psutil.disk_partitions()}")
            # 在每次循环结束时明确地删除变量并触发垃圾回收
            # print("清除变量内存")

            # 再次打印所有对象的摘要  
            # all_objects = muppy.get_objects()
            # print("After delete:")
            # summary.print_(summary.summarize(all_objects))
        logger.debug("清除变量内存")
        del input_box,send_button,username_box,message_box,incoming_user_box
        gc.collect()

        await asyncio.sleep(5)


    

def incoming_send_message_user(user_box, input_box, send_button):
    if user_box != None:
        reply(None, input_box, send_button, f'欢迎[{user_box.text}]亲！ 中国袋鼠入驻支付宝平台，优惠多多福利多多! ')

def incoming_send_message(input_box,send_button):
    message = random.choice(messageList)
    reply(None, input_box, send_button, message)



if __name__ == "__main__":
    driver = getDriver()
    # 截取二维码并存储到指定目录[TODO 静态资源服务器]
    auth()
    # 选择商户号 并进入对应商家直播管理平台
    select_shop()
    # 进入直播间
    open_live()
    # 循环获取弹幕互动消息内容
    message_replay()
