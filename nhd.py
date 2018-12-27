#!/usr/bin/env python3
# -*- coding: UTF-8 -*-


import requests
from selenium import webdriver


class NexusHD:
    def __init__(self, username, passowrd):
        self.username = username
        self.password = passowrd

        self.urlRoot = 'http://www.nexushd.org/'
        self.loginPath = 'takelogin.php'
        self.driverPath = 'path/to/phantomjs.exe'

        self.cookies = None

    def update_cookies(self):
        s = requests.post(self.urlRoot + self.loginPath, data={'username': self.username, 'password': self.password})
        self.cookies = s.history[0].cookies.get_dict()

    def sign_in(self):
        assert self.cookies is not None, 'should update cookies first'

        driver = webdriver.PhantomJS(executable_path=self.driverPath)
        for name, value in self.cookies.items():
            cookie = {
                'domain': '.nexushd.org',  # Note: If 'domain' part is missed or with value 'www.nexushd.org',
                                           # PhantomJS will print the following words:
                                           # "errorMessage":"Can only set Cookies for the current domain"
                                           # But actually the script still works.
                                           # Chrome driver does not have this bug.
                'name': name,
                'value': value,
                'path': '/'
            }
            try:
                driver.add_cookie(cookie)
            except Exception as e:
                print(name, 'wrong', '\n', e)

        driver.get('http://www.nexushd.org/signin.php')
        driver.find_element_by_tag_name('textarea').send_keys(' [em4] ')
        driver.find_element_by_id('qr').click()
        driver.save_screenshot('result.png')

        driver.quit()


if __name__ == '__main__':
    nhd = NexusHD('your username', 'your password')
    nhd.update_cookies()
    nhd.sign_in()
