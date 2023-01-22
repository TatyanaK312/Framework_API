import pytest
import requests
from lib.base_case import BaseCase
from lib.assertions import Assertions
import random
import string

class TestUserEditFAIL(BaseCase):
    def test_edit_just_created_user_fail(self):

#REGISTER
        register_data=self.prepare_registration_data()
        response1=requests.post("https://playground.learnqa.ru/api/user/",data=register_data)
        Assertions.assert_code_status(response1,200)
        Assertions.assert_json_has_key(response1,"id")

        email=register_data['email']
        first_name = register_data['firstName']
        password = register_data['password']
        user_id = self.get_json_value(response1,"id")

        #LOGIN
        login_data = {
            'email':email,
            'password':password
        }
        response2=requests.post("https://playground.learnqa.ru/api/user/login",data=login_data)
        auth_sid=self.get_cookie(response2,"auth_sid")
        token=self.get_header(response2,"x-csrf-token")
#______________________№1
        #EDIT Попытаемся изменить данные пользователя, будучи неавторизованными
        new_name="Changed Name"
        response3=requests.put(f"https://playground.learnqa.ru/api/user/{user_id}",
                              data={"firstName":new_name})
        print(f"Убеждаемся, что данные пользователя не изменились, будучи неавторизованными,  ",response3.status_code)
        print(response3.text)
        Assertions.assert_code_status(response3,400)

#_________________________________________________№2

        #Попытаемся изменить данные пользователя, будучи авторизованными другим пользователем

        # LOGIN авторизованного  пользователя
        login_data = {
            'email':'vinkotov@example.com',
            'password':'1234'
        }
        response2 = requests.post("https://playground.learnqa.ru/api/user/login", data=login_data)
        auth_sid1 = self.get_cookie(response2, "auth_sid")
        token1 = self.get_header(response2, "x-csrf-token")
        #EDIT
        new_name="Changed Name"
        response3=requests.put(f"https://playground.learnqa.ru/api/user/{user_id}",
                               headers={"x-csrf-token": token1},
                               cookies={"auth_sid": auth_sid1},
                              data={"firstName":new_name})
        print(f"Убеждаемся, что данные пользователя не изменились, будучи авторизованными другим пользователем,  ", response3.status_code)
        print(response3.text)
        Assertions.assert_code_status(response3,400)

#__________________________________№3
#зменяем email пользователя, будучи авторизованными тем же пользователем, на новый email без символа @

                #EDIT
        new_email='tyutyutyuexample.com'
        response3=requests.put(f"https://playground.learnqa.ru/api/user/{user_id}",
                               headers={"x-csrf-token":token},
                               cookies={"auth_sid":auth_sid},
                               data={"email":new_email})

        print(f"Изменяем email пользователя, будучи авторизованными тем же пользователем, на новый email без символа @ ,  ", response3.status_code)
        print(response3.text)
        Assertions.assert_code_status(response3,400)

#________________4
#Изменяем firstName пользователя, будучи авторизованными тем же пользователем, на очень короткое значение в один символ
    # EDIT
        new_name = random.choice(string.ascii_letters)
        response3 = requests.put(f"https://playground.learnqa.ru/api/user/{user_id}",
                             headers={"x-csrf-token": token},
                             cookies={"auth_sid": auth_sid},
                             data={"firstName": new_name})
        Assertions.assert_code_status(response3, 400)
        print(f"Изменяем firstName пользователя, будучи авторизованными тем же пользователем, на очень короткое значение в один символ ,  ",
          response3.status_code)
        print(response3.text)
