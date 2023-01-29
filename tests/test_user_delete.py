import pytest
import requests
from lib.base_case import BaseCase
from lib.assertions import Assertions
from lib.my_requests import MyRequests

class TestUserDelete(BaseCase):
    def test_user_delete_auth_id2(self):
# LOGIN авторизованного  пользователя
        login_data = {
         'email': 'vinkotov@example.com',
         'password': '1234'
            }
        response = MyRequests.post("/user/login", data=login_data)
        auth_sid = self.get_cookie(response, "auth_sid")
        token = self.get_header(response, "x-csrf-token")
#DELETE user id=2
        response2=MyRequests.delete(f"/user/2",
                               headers={"x-csrf-token": token},
                               cookies={"auth_sid": auth_sid},
                              data=login_data)
        print(response2.text, f"Не удалить пользователя")
        Assertions.assert_code_status(response2,400)


# #Запросить удаляемого пользователя - ПРОВЕРКА
        response4 = MyRequests.get(f"/user/2",
                           headers={"x-csrf-token": token},
                           cookies={"auth_sid": auth_sid}
                           )

        print(f"Ответ запроса на регистрацию удаляемого {2} пользователя: ", response4.text)

    def test_user_delete_new_user(self):
# REGISTER
        register_data = self.prepare_registration_data()
        response1 = MyRequests.post("/user/", data=register_data)
        Assertions.assert_code_status(response1, 200)
        Assertions.assert_json_has_key(response1, "id")

        email = register_data['email']
        first_name = register_data['firstName']
        password = register_data['password']
        user_id = self.get_json_value(response1, "id")

        # LOGIN
        login_data = {
            'email': email,
            'password': password
        }
        response2 = MyRequests.post("/user/login", data=login_data)
        auth_sid = self.get_cookie(response2, "auth_sid")
        token = self.get_header(response2, "x-csrf-token")
 # DELETE new user
        response3 = MyRequests.delete(f"/user/{user_id}",
                                    headers={"x-csrf-token": token},
                                    cookies={"auth_sid": auth_sid},
                                    data=login_data)

        Assertions.assert_code_status(response3,200)
# #Запросить удаленного пользователя - ПРОВЕРКА
        response4=MyRequests.get(f"/user/{user_id}",
                               headers={"x-csrf-token": token},
                               cookies={"auth_sid": auth_sid}
                               )

        print(f"Ответ запроса на регистрацию удаленного {user_id} пользователя: ",response4.text)
        Assertions.assert_code_status(response4,404)

    def test_user_delete_user_auth(self):
# REGISTER
        register_data = self.prepare_registration_data()
        response1 = MyRequests.post("/user/", data=register_data)
        Assertions.assert_code_status(response1, 200)
        Assertions.assert_json_has_key(response1, "id")

        email = register_data['email']
        first_name = register_data['firstName']
        password = register_data['password']
        user_id = self.get_json_value(response1, "id")

 # LOGIN авторизованного  пользователя
        login_data = {
            'email': 'vinkotov@example.com',
            'password': '1234'
        }
        response2 = MyRequests.post("/user/login", data=login_data)
        auth_sid1 = self.get_cookie(response2, "auth_sid")
        token1 = self.get_header(response2, "x-csrf-token")

# DELETE other user
        response3 = MyRequests.delete(f"/user/{user_id}")

        #print(f"User {user_id} не удалить  ", response3.text,response3.status_code)
        Assertions.assert_code_status(response3,400)
# Запросить удаленного пользователя - ПРОВЕРКА

        response4 = MyRequests.get(f"/user/{user_id}",
                               headers={"x-csrf-token": token1},
                               cookies={"auth_sid": auth_sid1}
                               )
        print(f"Ответ запроса на регистрацию удаленного {user_id} пользователя: ",response4.text)