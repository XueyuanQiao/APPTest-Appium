#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
@author: Qiaoxueyuan
@time: 2017/8/15 14:45
'''
import os, time, unittest
from appium import webdriver

PATH = lambda p: os.path.abspath(os.path.join(os.path.dirname(__file__), p))


class FirstTest(unittest.TestCase):
    def setUp(self):
        self.desired_caps = {}
        self.desired_caps['platformName'] = 'Android'  # 设备系统
        self.desired_caps['platformVersion'] = '4.3'  # 设备系统版本
        self.desired_caps['deviceName'] = '192.168.121.101:5555'  # 设备名称
        self.desired_caps['noReset'] = False

    def test_login(self):
        # self.desired_caps['app'] = PATH(r"D:\com.udesk_mvp_2.0_liqucn.com.apk")
        self.desired_caps['appPackage'] = 'com.udesk_mvp'
        self.desired_caps['appActivity'] = 'cn.udesk.mvp.loginmvp.WelcomActivity'
        self.driver = webdriver.Remote("http://localhost:4723/wd/hub", self.desired_caps)
        driver = self.driver
        driver.find_elements_by_id("com.udesk_mvp:id/login_edit")[0].send_keys("brazil")
        driver.find_elements_by_id("com.udesk_mvp:id/login_edit")[1].send_keys("qiaoxueyuan@brazil.udesk.cn")
        driver.find_elements_by_id("com.udesk_mvp:id/login_edit")[2].send_keys("*********")
        driver.find_element_by_name("登录").click()

    def tearDown(self):
        self.driver.quit()


if __name__ == "__main__":
    unittest.main()
