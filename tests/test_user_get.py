import pytest
import requests
from lib.base_case import BaseCase
from lib.assertions import Assertions

class TestUserGet(BaseCase):
    def test_get_user_details_not_auth(self):
        response=requests.get("https://playground.learnqa.ru/api/user/1")
        Assertions.assert_json_has_key(response,"username")
        Assertions.assert_json_has_not_key(response,"email")
        Assertions.assert_json_has_not_key(response,"firstName")
        Assertions.assert_json_has_not_key(response,"lastName")
    def test_get_user_details_auth(self):
        data={
            'email':'vinkotov@example.com',
            'password':'1234'
        }
        response1 = requests.post("https://playground.learnqa.ru/api/user/login", data=data)
        auth_sid = self.get_cookie(response1,"auth_sid")
        token = self.get_header(response1,"x-csrf-token")
        user_id_from_auth_metod = self.get_json_value(response1,"user_id")
        response2=requests.get(f"https://playground.learnqa.ru/api/user/{user_id_from_auth_metod}",
            headers={"x-csrf-token":token},
            cookies={"auth_sid":auth_sid}
                               )
        expected_fields = ["username", "email", "firstName", "lastName"]
        Assertions.assert_json_has_keys(response2, expected_fields)

    def test_get_user_other(self):
        data={
            'email':'vinkotov@example.com',
            'password':'1234'
        }
        response1 = requests.post("https://playground.learnqa.ru/api/user/login", data=data)
        auth_sid = self.get_cookie(response1,"auth_sid")
        token = self.get_header(response1,"x-csrf-token")
        user_id_from_auth_metod = self.get_json_value(response1,"user_id")
        print(f"авторизация c id ", user_id_from_auth_metod)
        response3 = requests.get(f"https://playground.learnqa.ru/api/user/1",
                                 headers={"x-csrf-token": token},
                                 cookies={"auth_sid": auth_sid}
                                 )
        print("Получаем только username с id=1?")
        Assertions.assert_json_has_key(response3,"username")
        Assertions.assert_json_has_not_key(response3,"email")
        Assertions.assert_json_has_not_key(response3,"firstName")
        Assertions.assert_json_has_not_key(response3,"lastName")



