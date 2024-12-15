import unittest
from unittest import TestCase

from check_email import check_email
from quadratic_equation import quadratic_equation
from votes import vote

import os
from dotenv import load_dotenv
from YandexInterface import YAInterface

import time
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions

load_dotenv()
yandex_token = os.getenv('yandex_token')
yandex_user = os.getenv('yandex_user')
yandex_pswrd = os.getenv('yandex_pswrd')
auth_url = 'https://passport.yandex.ru/auth/'


class TestEquation(TestCase):

    @unittest.skip
    def test_quadratic_equation_1(self):
        expected = 3.5
        a = -4
        b = 28
        c = -49
        actual = quadratic_equation(a, b, c)
        self.assertEqual(expected, actual)

    def test_equation_params(self):
        for i, (a, b, c, expected) in enumerate((
                (1, 8, 15, [-3.0, -5.0]),
                (1, -13, 12, [12.0, 1.0]),
                (-4, 28, -49, 3.5),
                (1, 1, 1, None)
        )):
            with self.subTest(i):
                actual = quadratic_equation(a, b, c)
                self.assertEqual(expected, actual)


class TestCheckEmail(TestCase):
    def test_mail(self):
        for i, (email, expected) in enumerate((
                ('Helloworld@.ru', True),
                ('мояпочта@нетология.ру', True),
                ('python@email@net', False),
                (' em@il.ru', False)
        )):
            with self.subTest(i):
                actual = check_email(email)
                self.assertEqual(expected, actual)


class TestVotes(TestCase):
    def test_votes(self):
        for i, (votes, expected) in enumerate((
                ((1, 1, 1, 2, 3), 1),
                ((1, 2, 3, 2, 2), 2)
        )):
            with self.subTest(i):
                actual = vote(votes)
                self.assertEqual(expected, actual)


class TestYaApi(TestCase):
    def setUp(self):
        self.folder_name = 'first_folder'
        self.ya_disk = YAInterface(yandex_token)
        self.ya_disk.delete_folder(self.folder_name)

    def test_create_success_1(self):
        expected = 201
        actual = self.ya_disk.create_folder(self.folder_name)
        self.assertEqual(expected, actual.status_code)

    def test_create_failed_1(self):
        self.ya_disk.create_folder(self.folder_name)
        expected = 409
        actual = self.ya_disk.create_folder(self.folder_name)
        self.assertEqual(expected, actual.status_code)

    @unittest.expectedFailure
    def test_create_failed_2(self):
        ya_disk = YAInterface('some_no_valid_token')
        expected = 201
        actual = ya_disk.create_folder(self.folder_name)
        self.assertEqual(expected, actual.status_code)

    @unittest.expectedFailure
    def test_create_failed_3(self):
        actual = self.ya_disk.create_folder('')
        expected = 201
        self.assertEqual(expected, actual.status_code)


class TestYaAuth(TestCase):
    def setUp(self):
        chrome_path = ChromeDriverManager().install()
        browser_service = Service(executable_path=chrome_path)
        self.browser = Chrome(service=browser_service)

    def test_auth_success_1(self):
        user = yandex_user
        password = yandex_pswrd
        self.browser.get(auth_url)
        self.assertIn('Авторизация', self.browser.title)

        elem = self.browser.find_element(by=By.NAME, value='login')
        elem.send_keys(user)
        elem.send_keys(Keys.RETURN)
        time.sleep(1)
        print(self.browser.current_url)
        self.assertEqual('https://passport.yandex.ru/auth/welcome', self.browser.current_url)
        elem = self.browser.find_element(by=By.NAME, value='passwd')
        elem.send_keys(password)
        elem.send_keys(Keys.RETURN)
        time.sleep(5)
        self.assertEqual('https://id.yandex.ru/', self.browser.current_url)
        time.sleep(1)

    @unittest.expectedFailure
    def test_auth_failed_1(self):
        user = '123456'
        password = yandex_pswrd
        self.browser.get(auth_url)
        self.assertIn('Авторизация', self.browser.title)

        elem = self.browser.find_element(by=By.NAME, value='login')
        elem.send_keys(user)
        elem.send_keys(Keys.RETURN)
        time.sleep(1)
        self.assertEqual('https://passport.yandex.ru/auth/welcome', self.browser.current_url)

        elem = self.browser.find_element(by=By.NAME, value='passwd')
        elem.send_keys(password)
        elem.send_keys(Keys.RETURN)
        time.sleep(5)

        self.assertEqual('https://id.yandex.ru/', self.browser.current_url)
        time.sleep(1)
