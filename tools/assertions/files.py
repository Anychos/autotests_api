import allure

from clients.error_schema import InternalErrorResponseSchema, ValidationErrorResponseSchema, ValidationErrorSchema
from clients.files.files_schema import (
    CreateFileRequestSchema,
    CreateFileResponseSchema,
    FileSchema,
    GetFileResponseSchema,
)
from config import settings
from tools.assertions.errors import assert_internal_error_response, assert_validation_error_response
from tools.assertions.base_assertions import assert_value
from tools.logger import get_logger

logger = get_logger("FILES_ASSERTIONS")

@allure.step("Проверка ответа на запрос создания файла")
def assert_create_file_response(request: CreateFileRequestSchema, response: CreateFileResponseSchema):
    """
    Функция для проверки ответа на запрос создания файла

    :param request: Схема запроса на создание файла
    :param response: Схема ответа сервера на запрос создания файла
    :raises AssertionError: Если хотя бы одно поле не совпадает
    """
    logger.info("Проверка ответа на запрос создания файла")
    expected_url = f"{settings.http_client.url}static/{request.directory}/{request.filename}" # динамически формируем url

    assert_value(response.file.filename, request.filename, "filename")
    assert_value(response.file.directory, request.directory, "directory")
    assert_value(str(response.file.url), expected_url, "url") # преобразуем url в строку

@allure.step("Проверка файла")
def assert_file(actual: FileSchema, expected: FileSchema):
    """
    Проверяет, что фактические данные файла соответствуют ожидаемым.

    :param actual: Фактические данные файла.
    :param expected: Ожидаемые данные файла.
    :raises AssertionError: Если хотя бы одно поле не совпадает.
    """
    logger.info("Проверка файла")
    assert_value(actual.id, expected.id, "id")
    assert_value(actual.url, expected.url, "url")
    assert_value(actual.filename, expected.filename, "filename")
    assert_value(actual.directory, expected.directory, "directory")

@allure.step("Проверка ответа на запрос файла")
def assert_get_file_response(
        get_file_response: GetFileResponseSchema,
        create_file_response: CreateFileResponseSchema
):
    """
    Проверяет, что ответ на получение файла соответствует ответу на его создание.

    :param get_file_response: Ответ API при запросе данных файла.
    :param create_file_response: Ответ API при создании файла.
    :raises AssertionError: Если данные файла не совпадают.
    """
    logger.info("Проверка ответа на запрос файла")
    assert_file(get_file_response.file, create_file_response.file)

@allure.step("Проверка ответа на запрос создания файла без имени")
def assert_create_file_with_empty_filename_response(actual: ValidationErrorResponseSchema):
    """
    Проверяет, что ответ на создание файла с пустым именем файла соответствует ожидаемой валидационной ошибке.

    :param actual: Ответ от API с ошибкой валидации, который необходимо проверить.
    :raises AssertionError: Если фактический ответ не соответствует ожидаемому.
    """
    logger.info("Проверка ответа на запрос создания файла без имени")
    expected = ValidationErrorResponseSchema(
        details=[
            ValidationErrorSchema(
                type="string_too_short",
                input="",
                context={"min_length": 1},
                message="String should have at least 1 character",
                location=["body", "filename"]
            )
        ]
    )
    assert_validation_error_response(actual, expected)

@allure.step("Проверка ответа на запрос создания файла без директории")
def assert_create_file_with_empty_directory_response(actual: ValidationErrorResponseSchema):
    """
    Проверяет, что ответ на создание файла с пустым значением директории соответствует ожидаемой валидационной ошибке.

    :param actual: Ответ от API с ошибкой валидации, который необходимо проверить.
    :raises AssertionError: Если фактический ответ не соответствует ожидаемому.
    """
    logger.info("Проверка ответа на запрос создания файла без директории")
    expected = ValidationErrorResponseSchema(
        details=[
            ValidationErrorSchema(
                type="string_too_short",
                input="",
                context={"min_length": 1},
                message="String should have at least 1 character",
                location=["body", "directory"]
            )
        ]
    )
    assert_validation_error_response(actual, expected)

@allure.step("Проверка ответа с ненайденным файлом")
def assert_file_not_found_response(actual: InternalErrorResponseSchema):
    """
    Функция для проверки ошибки, если файл не найден на сервере.

    :param actual: Фактический ответ.
    :raises AssertionError: Если фактический ответ не соответствует ошибке "File not found"
    """
    logger.info("Проверка ответа с ненайденным файлом")
    expected = InternalErrorResponseSchema(details="File not found")
    assert_internal_error_response(actual, expected)

@allure.step("Проверка ответа на запрос файла с некорректным id")
def assert_get_file_with_incorrect_file_id_response(actual: ValidationErrorResponseSchema):
    """
    Проверяет, что ответ на запрос файла с некорректным uuid соответствует ожидаемой валидационной ошибке.

    :param actual: Ответ от API с ошибкой валидации, который необходимо проверить.
    :raises AssertionError: Если фактический ответ не соответствует ожидаемому.
    """
    logger.info("Проверка ответа на запрос файла с некорректным id")
    expected = ValidationErrorResponseSchema(
        details=[
            ValidationErrorSchema(
                type="uuid_parsing",
                input="incorrect-file-id",
                context={"error": "invalid character: expected an optional prefix of `urn:uuid:` followed by [0-9a-fA-F-], found `i` at 1"},
                message="Input should be a valid UUID, invalid character: expected an optional prefix of `urn:uuid:` followed by [0-9a-fA-F-], found `i` at 1",
                location=["path", "file_id"]
            )
        ]
    )
    assert_validation_error_response(actual, expected)
