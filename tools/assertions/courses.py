import allure

from clients.courses.courses_schema import (
    CourseSchema,
    CreateCourseRequestSchema,
    CreateCourseResponseSchema,
    GetCourseByUserResponseSchema,
    UpdateCourseRequestSchema,
    UpdateCourseResponseSchema,
)
from tools.assertions.files import assert_file
from tools.assertions.users import assert_user
from tools.assertions.base_assertions import assert_is_true, assert_value
from tools.logger import get_logger

logger = get_logger("COURSES_ASSERTIONS")

@allure.step("Проверка ответа на запрос обновления курса")
def assert_update_course_response(request: UpdateCourseRequestSchema, response: UpdateCourseResponseSchema):
    """
    Проверяет, что ответ на обновление курса соответствует запросу.

    :param request: Исходный запрос на обновление курса.
    :param response: Ответ API с данными курса.
    :raises AssertionError: Если хотя бы одно поле не совпадает.
    """
    logger.info("Проверка ответа на запрос обновления курса")
    assert_value(response.course.title, request.title, "title")
    assert_value(response.course.max_score, request.max_score, "max_score")
    assert_value(response.course.min_score, request.min_score, "min_score")
    assert_value(response.course.description, request.description, "description")
    assert_value(response.course.estimated_time, request.estimated_time, "estimated_time")

@allure.step("Проверка курса")
def assert_course(actual: CourseSchema, expected: CourseSchema):
    """
    Проверяет, что фактические данные курса соответствует ожидаемым

    :param actual: Фактические данные курса
    :param expected: Ожидаемые данные курса
    :raises AssertionError: Если хотя бы одно поле не совпадает
    """
    logger.info("Проверка курса")
    assert_value(actual.id, expected.id, "id")
    assert_value(actual.title, expected.title, "title")
    assert_value(actual.max_score, expected.max_score, "max_score")
    assert_value(actual.min_score, expected.min_score, "min_score")
    assert_value(actual.description, expected.description, "description")
    assert_value(actual.estimated_time, expected.estimated_time, "estimated_time")

    assert_file(actual.preview_file, expected.preview_file)
    assert_user(actual.created_by_user, expected.created_by_user)

@allure.step("Проверка ответа на запрос получения курса")
def assert_get_courses_response(
        get_courses_response: GetCourseByUserResponseSchema,
        create_courses_response: list[CreateCourseResponseSchema]
):
    """
    Проверяет, что ответ на получение курсов соответствует списку созданных курсов

    :param get_courses_response: Схема ответа на получение курсов
    :param create_courses_response: Схема ответа на создание курсов
    :raises AssertionError: Если хотя бы одно поле не совпадает
    """
    logger.info("Проверка ответа на запрос получения курса")
    assert_value(len(get_courses_response.courses), len(create_courses_response), "courses")

    for index, create_course_response in enumerate(create_courses_response):
        assert_course(get_courses_response.courses[index], create_course_response.course)

@allure.step("Проверка ответа на запрос создания курса")
def assert_create_course_response(response: CreateCourseResponseSchema, request: CreateCourseRequestSchema):
    """
    Проверяет, что ответ на создание курса соответствует запросу

    :param response: Данные запроса на создание курса
    :param request: Данные ответа на создание курса
    :raises AssertionError: Если данные не совпадают
    """
    logger.info("Проверка ответа на запрос создания курса")
    assert_is_true(response.course.id, "id")
    assert_value(response.course.title, request.title, "title")
    assert_value(response.course.max_score, request.max_score, "max_score")
    assert_value(response.course.min_score, request.min_score, "min_score")
    assert_value(response.course.description, request.description, "description")
    assert_value(response.course.estimated_time, request.estimated_time, "estimated_time")
    assert_value(response.course.preview_file.id, request.preview_file_id, "preview_file")
    assert_value(response.course.created_by_user.id, request.created_by_user_id, "created_by_user")