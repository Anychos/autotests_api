import allure

from clients.users.users_schema import (
    CreateUserRequestSchema,
    CreateUserResponseSchema,
    GetUserResponseSchema,
    UserSchema,
)
from tools.assertions.base_assertions import assert_value
from tools.logger import get_logger

logger = get_logger("USERS_ASSERTIONS")

@allure.step("Проверка ответа на запрос создания пользователя")
def assert_create_user_response(request: CreateUserRequestSchema, response: CreateUserResponseSchema):
    """
    Проверяет, что ответ на создание пользователя соответствует запросу.

    :param request: Исходный запрос на создание пользователя.
    :param response: Ответ API с данными пользователя.
    :raises AssertionError: Если хотя бы одно поле не совпадает.
    """
    logger.info("Проверка ответа на запрос создания пользователя")
    assert_value(response.user.email, request.email, "email")
    assert_value(response.user.last_name, request.last_name, "last_name")
    assert_value(response.user.first_name, request.first_name, "first_name")
    assert_value(response.user.middle_name, request.middle_name, "middle_name")

@allure.step("Проверка пользователя")
def assert_user(actual: UserSchema, expected: UserSchema):
    """
    Проверяет, что ответ на получение пользователя соответствует ответу на создание пользователя.

    :param actual: Схема ответа на создание пользователя
    :param expected: Схема ответа на получение пользователя
    """
    logger.info("Проверка пользователя")
    assert_value(expected.id, actual.id, "id")
    assert_value(expected.email, actual.email, "email")
    assert_value(expected.last_name, actual.last_name, "last_name")
    assert_value(expected.first_name, actual.first_name, "first_name")
    assert_value(expected.middle_name, actual.middle_name, "middle_name")

@allure.step("Проверка ответа на запрос пользователя")
def assert_get_user_response(create_user_response: CreateUserResponseSchema,
                             get_user_response: GetUserResponseSchema):
    """
    Проверяет, что ответ на получение пользователя соответствует ответу на его создание.

    :param get_user_response: Ответ API при запросе данных пользователя.
    :param create_user_response: Ответ API при создании пользователя.
    :raises AssertionError: Если данные пользователя не совпадают.
    """
    logger.info("Проверка ответа на запрос пользователя")
    assert_user(create_user_response.user, get_user_response.user)