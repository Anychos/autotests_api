import allure

from clients.auth.auth_schema import LoginResponseSchema
from tools.assertions.base_assertions import assert_is_true, assert_value
from tools.logger import get_logger

logger = get_logger("AUTHENTICATION_ASSERTIONS")

@allure.step("Проверка ответа на логин")
def assert_login_response(response: LoginResponseSchema):
    """
    Функция для проверки ответа на запрос авторизации

    :param response: Схема ответа сервера на запрос авторизации
    :raises AssertionError: Если хотя бы одно поле не совпадает
    """
    logger.info("Проверка ответа на логин")
    assert_value(response.token.token_type, "bearer", "token_type")
    assert_is_true(response.token.access_token, "access_token")
    assert_is_true(response.token.refresh_token, "refresh_token")
