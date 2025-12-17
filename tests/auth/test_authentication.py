from http import HTTPStatus

import allure
import pytest

from clients.auth.auth_client import AuthAPIClient
from clients.auth.auth_schema import LoginRequestSchema, LoginResponseSchema
from fixtures.users import UserFixture
from tools.allure.epics import AllureEpic
from tools.allure.features import AllureFeature
from tools.allure.parent_suite import AllureParentSuite
from tools.allure.stories import AllureStory
from tools.allure.sub_suite import AllureSubSuite
from tools.allure.suite import AllureSuite
from tools.allure.tags import AllureTags
from tools.assertions.auth import assert_login_response
from tools.assertions.schema import validate_json_schema
from tools.assertions.base_assertions import assert_status_code


@pytest.mark.regression
@pytest.mark.smoke
@pytest.mark.authentication
@allure.tag(AllureTags.AUTHENTICATION, AllureTags.REGRESSION, AllureTags.SMOKE, AllureTags.POSITIVE)
@allure.epic(AllureEpic.LMS)
@allure.feature(AllureFeature.AUTHENTICATION)
@allure.parent_suite(AllureParentSuite.LMS)
@allure.suite(AllureSuite.AUTHENTICATION)
class TestAuthentication:
    @allure.story(AllureStory.LOGIN)
    @allure.sub_suite(AllureSubSuite.LOGIN)
    @allure.title("Логин существующего пользователя")
    def test_login(self,
            function_create_user: UserFixture,
            auth_client: AuthAPIClient
    ):

        request = LoginRequestSchema(
            email=function_create_user.email,
            password=function_create_user.password
        )

        response = auth_client.login_api(request)
        response_data = LoginResponseSchema.model_validate_json(response.text)

        assert_status_code(response.status_code, HTTPStatus.OK)
        assert_login_response(response_data)
        validate_json_schema(instance=response.json(), schema=response_data.model_json_schema())


