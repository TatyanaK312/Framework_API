import pytest
import random
import string
import requests
from lib.base_case import BaseCase
from lib.assertions import Assertions
from datetime import datetime
from lib.my_requests import MyRequests

class TestUserRegister(BaseCase):

    def setup_method(self):
        base_part = "learnqa"
        domain = "example.com"
        random_part = datetime.now().strftime("%m%d%Y%H%M%S")
        self.email = f"{base_part}{random_part}@{domain}"
    def test_create_user_succesfully(self):
        data = {
            'password':'123',
            'username':'Tatyana',
            'firstName':'Tatyana',
            'lastName':'Tatyana',
            'email':self.email
        }
        response = MyRequests.post("/user/", data=data)
        Assertions.assert_code_status(response, 200)
        Assertions.assert_json_has_key(response, "id")

    def test_create_user_with_existing_email(self):
        email = 'vinkotov@example.com'
        data = {
            'password': '123',
            'username': 'Tatyana',
            'firstName': 'Tatyana',
            'lastName': 'Tatyana',
            'email': email
        }
        response = MyRequests.post("/user/", data=data)
        Assertions.assert_code_status(response,400)
        assert response.content.decode("utf-8") == f"Users with email '{email}' already exists", f"Неожиданмый response.content {response.content}"

    def test_create_user_with_bad_email(self):
        base_part = "learnqa"
        domain = "example.com"
        random_part = datetime.now().strftime("%m%d%Y%H%M%S")
        email = f"{base_part}{random_part}{domain}"
        data = {
            'password': '123',
            'username': 'Tatyana',
            'firstName': 'Tatyana',
            'lastName': 'Tatyana',
            'email': email
        }
        response = MyRequests.post("/user/", data=data)
        Assertions.assert_code_status(response,400)
        assert response.content.decode("utf-8") == f"Invalid email format", f"Неожидаемый response.content {response.content}"
        print('Задан некорректный email:  ',email)

class TestParams:

    heads = [
            ("username", "firstName", "lastName", "email","no password"),
            ("username", "firstName", "lastName", "no email","password"),
            ("username", "firstName", "no lastName", "email", "password"),
            ("username", "no firstName", "lastName", "email", "password"),
            ("no username", "firstName", "lastName", "email", "password")
        ]

    @pytest.mark.parametrize('expected1, expected2,expected3,expected4,expected5', heads)
    def test_create_user_without_params(self, expected1, expected2,expected4,expected3,expected5):
        base_part = "learnqa"
        domain = "example.com"
        random_part = str(random.random())
        email1 = f"{base_part}{random_part}@{domain}"
        print(f"Создание пользователя без указания одного из полей")
        data = {
          expected1: 'Tatyana',
          expected2: 'Tatyana',
          expected3: 'Tatyana',
          expected4: email1,
          expected5: '123123'
        }
        response = MyRequests.post("/user/", data=data)
        Assertions.assert_code_status(response, 400)
        print(response.text)

    def test_create_user_short_name(self):
        base_part = "learnqa"
        domain = "example.com"
        random_part = str(random.random())
        email1 = f"{base_part}{random_part}@{domain}"
        randomLetter = random.choice(string.ascii_letters)

        data = {
            'password': '123',
            'username': randomLetter,
            'firstName': 'Tatyana',
            'lastName': 'Tatyana',
            'email': email1
        }
        response = MyRequests.post("/user/", data=data)
        Assertions.assert_code_status(response, 400)
        print(response.text)


    def test_create_user_long_name(self):
        base_part = "learnqa"
        domain = "example.com"
        random_part = str(random.random())
        email1 = f"{base_part}{random_part}@{domain}"
        randomstr = ''.join(random.choices(string.ascii_uppercase + string.digits, k=260))
        data = {
            'password': '123',
            'username': randomstr,
            'firstName': 'Tatyana',
            'lastName': 'Tatyana',
            'email': email1
        }
        response = MyRequests.post("/user/", data=data)
        Assertions.assert_code_status(response, 400)
        print(response.text)

