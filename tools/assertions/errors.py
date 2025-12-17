import allure

from clients.error_schema import InternalErrorResponseSchema, ValidationErrorResponseSchema, ValidationErrorSchema
from tools.assertions.base_assertions import assert_length, assert_value
from tools.logger import get_logger

logger = get_logger("ERRORS_ASSERTIONS")

@allure.step("Проверка ошибки валидации")
def assert_validation_error(actual: ValidationErrorSchema, expected: ValidationErrorSchema):
    """
    Проверяет, что объект ошибки валидации соответствует ожидаемому значению.

    :param actual: Фактическая ошибка.
    :param expected: Ожидаемая ошибка.
    :raises AssertionError: Если значения полей не совпадают.
    """
    logger.info("Проверка ошибки валидации")
    assert_value(actual.type, expected.type, "type")
    assert_value(actual.input, expected.input, "input")
    assert_value(actual.context, expected.context, "context")
    assert_value(actual.message, expected.message, "message")
    assert_value(actual.location, expected.location, "location")

@allure.step("Проверка ответа с ошибкой валидации")
def assert_validation_error_response(
        actual: ValidationErrorResponseSchema,
        expected: ValidationErrorResponseSchema
):
    """
    Проверяет, что объект ответа API с ошибками валидации (`ValidationErrorResponseSchema`)
    соответствует ожидаемому значению.

    :param actual: Фактический ответ API.
    :param expected: Ожидаемый ответ API.
    :raises AssertionError: Если значения полей не совпадают.
    """
    logger.info("Проверка ответа с ошибкой валидации")
    assert_length(actual.details, expected.details, "details")

    for index, detail in enumerate(expected.details): # цикл сравнивает ожидаемые и актуальные ошибки в ValidationErrorResponseSchema
        assert_validation_error(actual.details[index], detail)

@allure.step("Проверка ответа с ошибкой internal error")
def assert_internal_error_response(
        actual: InternalErrorResponseSchema,
        expected: InternalErrorResponseSchema
):
    """
    Функция для проверки внутренней ошибки. Например, ошибки 404 (File not found).

    :param actual: Фактический ответ API.
    :param expected: Ожидаемый ответ API.
    :raises AssertionError: Если значения полей не совпадают.
    """
    logger.info("Проверка ответа с ошибкой internal error")
    assert_value(actual.details, expected.details, "details")