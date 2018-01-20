#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
@author: Qiaoxueyuan
@time: 2017/10/11 10:55
'''

import unittest
import threading
import random
from time import sleep
from selenium.common import exceptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from appium import webdriver
from test_env import set_log, set_driver


class TestSDK350(unittest.TestCase):
    '''测试SDK3.5.0版本，包含：SDK登录、'''

    def setUp(self):
        self.desired_caps = {}
        self.desired_caps['platformName'] = 'Android'  # 设备系统
        self.desired_caps['platformVersion'] = '4.3'  # 设备系统版本
        self.desired_caps['deviceName'] = '192.168.121.101:5555'  # 设备名称
        self.desired_caps['noReset'] = False
        # self.desired_caps['app'] = PATH(r"D:\udesksdkdemo_10_af0329fd-b1b0-4071-8d79-853a71b56ab3.apk")
        self.desired_caps['appPackage'] = 'udesk.sdk.demo'
        self.desired_caps['appActivity'] = 'udesk.sdk.demo.activity.UdeskInitKeyActivity'
        self.driverA = webdriver.Remote("http://localhost:4723/wd/hub", self.desired_caps)
        self.driverB = set_driver.init_driver()
        self.log = set_log.init_log("testSDK3.5.0")

    def test_login(self):
        driverA = self.driverA
        driverB = self.driverB
        log = self.log
        send_msg1 = "欢迎光临切尔西酒店！"
        respond_msg1 = "Can you speak english?"
        send_msg2 = "Of course!Welcome to QieErXi Hotel."

        def web_login():
            # 客服web端登录
            set_driver.qiao_login(driverB, "brazil.udesk.cn")

        def sdk_login():
            # 登录SDK
            driverA.find_element_by_id("udesk.sdk.demo:id/udesk_domain").send_keys("brazil.udesk.cn")
            driverA.find_element_by_id("udesk.sdk.demo:id/udesk_appkey").send_keys("586faa75a4560bb74c24859e47a25bc3")
            driverA.find_element_by_id("udesk.sdk.demo:id/appid").send_keys("2d49493acf3dc504")
            driverA.find_element_by_id("udesk.sdk.demo:id/udesk_start").click()
            log.debug("【SDK】登陆SDK")

        # threads = []
        t1 = threading.Thread(target=web_login())
        # threads.append(t1)
        t2 = threading.Thread(target=sdk_login())
        # threads.append(t2)
        # for t in threads:
        #     t.setDaemon(True)
        #     t.start()
        # t.join()
        t1.start()
        t2.start()
        # t1.join()
        # t2.join()



        # （WEB）客服IM调至在线
        sleep(3)
        driverB.find_element_by_xpath("//li[contains(@class,'nav-im')]").click()
        state = WebDriverWait(driverB, 5, 0.5).until(
            EC.presence_of_element_located((By.CLASS_NAME, "agent-status-text")))
        log.debug("（WEB）客服登陆成功")
        if state.text != "在线":
            state.click()
            driverB.find_element_by_xpath("//i[contains(@class,'circle online')]").click()
        log.debug("（WEB）客服IM状态调至在线")
        sleep(3)

        # 【SDK】进入咨询会话
        driverA.find_element_by_id("udesk.sdk.demo:id/udesk_group_conversation").click()
        log.debug("【SDK】进入咨询会话模块")
        try:
            driverA.find_element_by_name("雪源自动化测试(勿动)").click()
            log.debug("【SDK】选择客服组")
        except exceptions.NoSuchElementException:
            log.debug("【SDK】未选择客服组直接进入了会话")

        # （WEB）发送会话
        try:
            sleep(5)  # 等待进入
            driverB.find_element_by_xpath("//div[@id='im-chats']/div[4]/ul").click()
        except:
            driverB.find_element_by_xpath("//div[@id='im-chats']/div[4]/ul[1]").click()
        driverB.find_element_by_xpath("//div[@class='input-box']/textarea").send_keys(send_msg1)
        driverB.find_element_by_id("btnSend").click()
        log.debug("（WEB）客服接通对话并发送消息")
        sleep(1)

        # 【SDK】回复会话
        try:
            msg_list = driverA.find_elements_by_id("udesk.sdk.demo:id/udesk_tv_msg")
            if msg_list[len(msg_list) - 1].text == send_msg1:
                driverA.find_element_by_id("udesk.sdk.demo:id/udesk_bottom_input").click()
                driverA.find_element_by_id("udesk.sdk.demo:id/udesk_bottom_input").send_keys(respond_msg1)
                driverA.find_element_by_id("udesk.sdk.demo:id/udesk_bottom_send").click()
                log.debug("【SDK】接收到消息并回复")
            else:
                raise Exception("【SDK】未收到web端消息")
        except Exception as e:
            log.error(e)

        # （WEB）回复会话

        driverB.find_element_by_xpath("//div[@class='input-box']/textarea").send_keys(send_msg2)
        driverB.find_element_by_id("btnSend").click()
        log.debug("（WEB）客服接通对话并发送消息")
        sleep(1)

        # （WEB）邀请评价满意度
        driverB.find_element_by_id("btnPushSurvey").click()
        sleep(2)

        # 【SDK】回复满意度
        choices = driverA.find_elements_by_id("udesk.sdk.demo:id/text_context")
        i = random.randint(0, 3)
        choices[i].click()  # 随机选择一项评价
        driverA.find_element_by_id("udesk.sdk.demo:id/udesk_ok").click()


    def tearDown(self):
        # self.driverA.quit()
        # self.driverB.quit()
        sleep(5)


if __name__ == "__main__":
    unittest.main()
