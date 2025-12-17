from http import HTTPStatus

import allure
import pytest

from clients.users.private_user_client import PrivateUserAPIClient
from clients.users.public_user_client import PublicUserAPIClient
from clients.users.users_schema import CreateUserRequestSchema, CreateUserResponseSchema, GetUserResponseSchema
from fixtures.users import UserFixture
from tools.allure.epics import AllureEpic
from tools.allure.features import AllureFeature
from tools.allure.parent_suite import AllureParentSuite
from tools.allure.stories import AllureStory
from tools.allure.sub_suite import AllureSubSuite
from tools.allure.suite import AllureSuite
from tools.allure.tags import AllureTags
from tools.assertions.schema import validate_json_schema
from tools.assertions.users import assert_get_user_response
from tools.assertions.base_assertions import assert_status_code, assert_value
from tools.data_generator import fake


@pytest.mark.regression
@pytest.mark.smoke
@pytest.mark.users
@allure.tag(AllureTags.USERS, AllureTags.REGRESSION, AllureTags.SMOKE, AllureTags.POSITIVE)
@allure.epic(AllureEpic.LMS)
@allure.feature(AllureFeature.USERS)
@allure.parent_suite(AllureParentSuite.LMS)
@allure.suite(AllureSuite.USERS)
class TestUser:
    @pytest.mark.parametrize('email', ['mail.ru', 'gmail.com', 'example.com'])
    @allure.tag(AllureTags.CREATE_ENTITY)
    @allure.story(AllureStory.CREATE_ENTITY)
    @allure.sub_suite(AllureSubSuite.CREATE_ENTITY)
    @allure.title("Создание нового пользователя")
    def test_create_user(self, email: str, public_user_client: PublicUserAPIClient):
        allure.dynamic.title(f"Email пользователя: {email}") # создание динамического наименования для теста
        request = CreateUserRequestSchema(email=fake.email(email))

        response = public_user_client.create_user_api(request)

        response_data = CreateUserResponseSchema.model_validate_json(response.text)
        assert_status_code(response.status_code, HTTPStatus.OK)
        assert_value(response_data.user.email, request.email, 'email')
        validate_json_schema(instance=response.json(), schema=response_data.model_json_schema())

    @allure.tag(AllureTags.GET_ENTITY)
    @allure.story(AllureStory.GET_ENTITY)
    @allure.sub_suite(AllureSubSuite.GET_ENTITY)
    @allure.title("Получение данных текущего пользователя")
    def test_get_user_me(self, function_create_user: UserFixture, private_user_client: PrivateUserAPIClient):
        response = private_user_client.get_user_me_api()

        response_data = GetUserResponseSchema.model_validate_json(response.text)
        assert_status_code(response.status_code, HTTPStatus.OK)
        assert_get_user_response(function_create_user.response, response_data)
        validate_json_schema(instance=response.json(), schema=response_data.model_json_schema())
