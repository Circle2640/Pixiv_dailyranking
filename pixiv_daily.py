#-*- coding = utf-8 -*-
#@Time : 2020/10/14 22:52
#@File : pixiv_daily.py
#@Software : PyCharm

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import requests
import time
import os
import re



#定义一个pixiv类
class pixiv_infos:

    #对象初始化
    def __init__(self):
        url = 'https://accounts.pixiv.net/login'
        self.url = url

        options = webdriver.ChromeOptions()
        options.add_experimental_option("prefs", {"profile.managed_default_content_settings.images": 1}) # 图片加载选项，1为加载2位不加载
        options.add_experimental_option('excludeSwitches', ['enable-automation']) #设置为开发者模式
        self.browser = webdriver.Chrome(options=options)

        self.wait = WebDriverWait(self.browser, 10) #超时时长为10s



    #登录账号
    def login(self):
        #最大化窗口
        self.browser.maximize_window()

        #打开网页
        self.browser.get(self.url)
        self.browser.implicitly_wait(10)

        #输入账号
        self.browser.find_element_by_xpath('//*[@id="LoginComponent"]/form/div[1]/div[1]/input').send_keys(username)

        #输入密码
        self.browser.find_element_by_xpath('//*[@id="LoginComponent"]/form/div[1]/div[2]/input').send_keys(password)

        #登录
        self.browser.implicitly_wait(10)
        self.browser.find_element_by_xpath('//*[@id="LoginComponent"]/form/button').click()

        #等待至账号头像以及每日排行榜加载完成
        self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#root > div:nth-child(2) > div.sc-12xjnzy-0.kBRZkr > div:nth-child(1) > div:nth-child(1) > div > div.sc-4nj1pr-3.iwONkn > div.sc-4nj1pr-4.iUIuEb > div.pkfh0q-0.ixuqpa > div > button > div > div')))
        self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#root > div:nth-child(2) > div.sc-1nr368f-2.gluvRx > div:nth-child(6) > div > section > div.sc-7zddlj-4.gWFZEu')))

    #退出账号
    def logout(self):
        #点击账号头像
        self.browser.find_element_by_xpath('//*[@id="js-mount-point-header"]/div/div/div[1]/div/div[3]/div[1]/div[5]/div/button/div/div').click()

        #点击退出
        self.browser.find_element_by_xpath('//*[@id="js-mount-point-header"]/div/div/div[1]/div/div[3]/div[1]/div[5]/div[2]/div/div/div/div/ul/li[10]/button').click()

        #点击OK
        self.browser.find_element_by_xpath('/html/body/div[8]/div/div/div/div[3]/div[2]/div/div/button[1]').click()


    #关闭浏览器
    def close(self):
        self.browser.quit()



    #图片为单张图片时的保存方法
    def save_pic(self, dic, dir_name, i):
        print('正在爬取第 %s 张图片' % str(i+1))
        #获取图片链接
        self.browser.find_element_by_css_selector('#root > div:nth-child(2) > div.sc-1nr368f-0.kCKAFN > div > div.sc-1nr368f-3.iHKGIi > main > section > div.sc-171jvz-0.ketmXG > div > figure > div > div > div > a > img').click()
        png_url = self.browser.find_element_by_xpath('/html/body/div[3]/div/div/div/img').get_attribute('src')

        # 使用requests保存图片
        header = {
            'user-agent': r'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36'
        }
        header['referer'] = str(dic['referer'])
        response = requests.get(png_url, headers=header)
        filename = dir_name + r'\\' + str(i+1) + '_' + dic['pic_name'] + '_' + dic['aut_name'] + '.png'
        with open(filename, 'wb') as f:
            f.write(response.content)



    #图片为多张图片时的保存方法
    def save_pic_mutli(self, dic, dir_name, i):
        print('正在爬取第 %s 张图片' % str(i+1))
        # 点击显示全部以及获取图片的数量
        nums = self.browser.find_element_by_css_selector('#root > div:nth-child(2) > div.sc-1nr368f-0.kCKAFN > div > div.sc-1nr368f-3.iHKGIi > main > section > div.sc-171jvz-0.ketmXG > div > figure > div > div.sc-1c2qglr-0.ccqCfP > div > div > div > div > div > span').text
        nums = int(nums[2:]) # nums表示图片的数量
        self.browser.find_element_by_css_selector('#root > div:nth-child(2) > div.sc-1nr368f-0.kCKAFN > div > div.sc-1nr368f-3.iHKGIi > main > section > div.sc-171jvz-0.ketmXG > div > figure > div > div.sc-1mz6e1e-1.kyYawS > div.sc-1qpw8k9-0.yjBCb > a > img').click()

        # 伪装
        header = {
            'user-agent': r'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36'
        }
        header['referer'] = str(dic['referer'])

        # 通过requests下载图片，使用css定位，分两次处理
        # 先下载第一张
        time.sleep(1)  # 给予等待时间
        element = self.browser.find_element_by_css_selector('#root > div:nth-child(2) > div.sc-1nr368f-0.kCKAFN > div > div.sc-1nr368f-3.iHKGIi > main > section > div.sc-171jvz-0.ketmXG > div > figure > div > div.sc-1mz6e1e-1.QBVJO.gtm-medium-work-expanded-view > div.sc-1qpw8k9-0.yjBCb > a > img')
        self.browser.execute_script('arguments[0].click();', element)  # 防止上一个元素覆盖下一个元素定位，出现错误
        png_url = self.browser.find_element_by_xpath('/html/body/div[3]/div/div[1]/div/img').get_attribute('src')
        self.browser.find_element_by_xpath('/html/body/div[3]/div/div[1]/div/img').click()
        time.sleep(1) # 给予等待时间
        response = requests.get(png_url, headers=header)
        filename = dir_name + r'\\' + str(i+1) + '_' + dic['pic_name'] + '_' + dic['aut_name'] + '_' + '1' + '.png'
        with open(filename, 'wb') as f:
            f.write(response.content)

        #下载第一张之后的图片
        for j in range(1, nums):
            time.sleep(1)  # 给予等待时间
            element = self.browser.find_element_by_css_selector('#root > div:nth-child(2) > div.sc-1nr368f-0.kCKAFN > div > div.sc-1nr368f-3.iHKGIi > main > section > div.sc-171jvz-0.ketmXG > div > figure > div > div:nth-child(%s) > div.sc-1qpw8k9-0.dEehPv > a > img' % str(j+2))
            self.browser.execute_script('arguments[0].click();', element)  # 防止上一个元素覆盖下一个元素定位，出现错误
            png_url = self.browser.find_element_by_xpath('/html/body/div[3]/div/div[1]/div/img').get_attribute('src')
            self.browser.find_element_by_xpath('/html/body/div[3]/div/div[1]/div/img').click()
            time.sleep(1) # 给予等待时间
            response = requests.get(png_url, headers=header)
            filename = dir_name + r'\\' + str(i+1) + '_' + dic['pic_name'] + '_' + dic['aut_name'] + '_' + str(j+1) + '.png'
            with open(filename, 'wb') as f:
                f.write(response.content)



    #获取作者、图片名字以及对应referer
    def get_name(self, i):
        dic = {}
        #获取伪装所需的referer
        dic['referer'] = self.browser.find_element_by_xpath('//*[@id="%s"]/div[2]/a' % str(i+1)).get_attribute('href')
        ele = self.browser.find_element_by_xpath('//*[@id="%s"]/div[2]/a' % str(i+1))
        self.browser.execute_script('arguments[0].click();', ele) # 防止上一个元素覆盖下一个元素定位，出现错误

        # 跳转至新标签
        handle = self.browser.window_handles
        self.browser.switch_to.window(handle[1])

        # 检测图片是否带有剧透标识，如果有则点击'显示作品'
        try:
            self.browser.find_element_by_css_selector('#root > div:nth-child(2) > div.sc-1nr368f-0.kCKAFN > div > div.sc-1nr368f-3.iHKGIi > main > section > div.sc-171jvz-0.ketmXG > div > figure > div > div.sc-3xfm45-1.ppLVj > div > div > button').click()
        except:
            pass

        # 等待至图片加载完成
        self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#root > div:nth-child(2) > div.sc-1nr368f-0.kCKAFN > div > div.sc-1nr368f-3.iHKGIi > main > section > div.sc-171jvz-0.ketmXG > div > figure > div > div > div > a > img')))

        # 获取作者名字与图片名字
        # 存在图片没有名字的情况，若图片无名则命名为'nameless'
        try:
            dic['pic_name'] = self.browser.find_element_by_css_selector('#root > div:nth-child(2) > div.sc-1nr368f-0.kCKAFN > div > div.sc-1nr368f-3.iHKGIi > main > section > div.sc-171jvz-0.ketmXG > div > figcaption > div > div > h1').text
        except:
            dic['pic_name'] = 'nameless'
        dic['aut_name'] = self.browser.find_element_by_css_selector('#root > div:nth-child(2) > div.sc-1nr368f-0.kCKAFN > div > div.sc-1nr368f-3.iHKGIi > aside > section.sc-171jvz-1.sc-171jvz-3.f30yhg-3.labtod > h2 > div > div > a').text
        dic['pic_name'] = re.sub(r'[/\'?:<>|*]*', '', dic['pic_name'])
        dic['aut_name'] = re.sub(r'[/\'?:<>|*]*', '', dic['aut_name'])
        return dic



    #找到每日排行榜中的图片并保存
    def find_daily(self, R_18, n):
        #鉴于try语句过慢，缩短隐式等待时间
        self.browser.implicitly_wait(7)

        #打开每日排行榜
        self.browser.find_element_by_css_selector('#root > div:nth-child(2) > div.sc-1nr368f-2.gluvRx > div:nth-child(6) > div > section > div.sc-7zddlj-0.gSALnO > a').click()

        #是否打开涩图模式
        if R_18:
            self.browser.find_element_by_xpath('//*[@id="wrapper"]/div[1]/div/div[2]/div/nav[1]/ul[2]/li[2]/a').click()
            # 创建今日文件夹
            dir_name = r'D:\\R-18_' + time.strftime('%Y-%m-%d-%H') #文件保存的路径(请自行更改)
            if not os.path.exists(dir_name):
                os.mkdir(dir_name)

        else:
            # 创建今日文件夹
            dir_name = r'D:\\' + time.strftime('%Y-%m-%d-%H') #文件保存的路径(请自行更改)
            if not os.path.exists(dir_name):
                os.mkdir(dir_name)

        #将页面加载至所需Rank名次
        time.sleep(2)
        if n % 50 == 0:
            t = n // 50
        else:
            t = (n // 50) + 1
        for i in range(t):
            time.sleep(3)
            self.browser.execute_script('window.scrollTo(0, document.body.scrollHeight)')

        #进入图片的单独页面并保存
        for i in range(n):
            #进入页面并获取相关信息
            dic = self.get_name(i)

            #检测是否含有多张图片
            try:
                self.browser.find_element_by_css_selector('#root > div:nth-child(2) > div.sc-1nr368f-0.kCKAFN > div > div.sc-1nr368f-3.iHKGIi > main > section > div.sc-171jvz-0.ketmXG > div > div.rsntqo-0.jEtDYL > div > div.ye57th-1.ghrZCB > button > div').text
            except:
                self.save_pic(dic, dir_name, i)
            else:
                self.save_pic_mutli(dic, dir_name, i)

            #关闭窗口并切换回原窗口
            self.browser.close()
            handle = self.browser.window_handles
            self.browser.switch_to.window(handle[0])

        print('爬取完毕！')



if __name__ == '__main__':

    username = '输入pixiv账号'
    password = '输入pixiv密码'
    n = int(input('请输入想要查找至TOP_X的数字:'))
    R_18 = int(input('是否打开涩图模式?(输入1打开，输入0关闭):')) #需要登录的账号能查看R-18图片

    g_d = pixiv_infos()
    g_d.login()
    g_d.find_daily(R_18, n)
    g_d.logout()
    g_d.close()
