#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
@author: Qiaoxueyuan
@time: 2017/8/21 11:41
'''

# 设置用例的浏览器

from selenium import webdriver


def init_driver():
    driver = webdriver.Chrome()
    # driver.maximize_window()
    return driver


def admin_login(driver, url):
    driver.get("http://%s/hc" % url)
    driver.find_element_by_xpath("//*[@href=\"/users/sign_in\"]").click()
    driver.find_element_by_id("user_email").send_keys("admin@%s" % url)
    driver.find_element_by_id("user_password").send_keys("*****")
    driver.find_element_by_xpath("//*[@value=\"登 录\"]").click()


def qiao_login(driver, url):
    driver.get("http://%s/hc" % url)
    driver.find_element_by_xpath("//*[@href=\"/users/sign_in\"]").click()
    driver.find_element_by_id("user_email").send_keys("qiaoxueyuan@%s" % url)
    driver.find_element_by_id("user_password").send_keys("********")
    driver.find_element_by_xpath("//*[@value=\"登 录\"]").click()
