import allure

from clients.error_schema import InternalErrorResponseSchema
from clients.exercises.exercises_schema import (
    CreateExerciseRequestSchema,
    CreateExerciseResponseSchema,
    ExerciseSchema,
    GetExerciseResponseSchema,
    GetExercisesResponseSchema,
    UpdateExerciseRequestSchema,
    UpdateExerciseResponseSchema,
)
from tools.assertions.errors import assert_internal_error_response
from tools.assertions.base_assertions import assert_is_true, assert_value
from tools.logger import get_logger

logger = get_logger("EXERCISES_ASSERTIONS")

@allure.step("Проверка ответа на запрос создания упражнения")
def assert_create_exercise_response(response: CreateExerciseResponseSchema, request: CreateExerciseRequestSchema):
    """
    Проверяет, что ответ на создание упражнения соответствует запросу

    :param response: Данные запроса на создание упражнения
    :param request: Данные ответа на создание упражнения
    :raises AssertionError: Если данные не совпадают
    """
    logger.info("Проверка ответа на запрос создания упражнения")
    assert_is_true(response.exercise.id, "id")
    assert_value(response.exercise.title, request.title, "title")
    assert_value(response.exercise.course_id, request.course_id, "course_id")
    assert_value(response.exercise.max_score, request.max_score, "max_score")
    assert_value(response.exercise.min_score, request.min_score, "min_score")
    assert_value(response.exercise.order_index, request.order_index, "order_index")
    assert_value(response.exercise.description, request.description, "description")
    assert_value(response.exercise.estimated_time, request.estimated_time, "estimated_time")

@allure.step("Проверка упражнения")
def assert_exercise(actual: ExerciseSchema, expected: ExerciseSchema):
    """
    Проверяет, что фактические данные упражнения соответствуют ожидаемым

    :param actual: Фактические данные упражнения
    :param expected: Ожидаемые данные упражнения
    :return AssertionError: Если данные не совпадают
    """
    logger.info("Проверка упражнения")
    assert_value(actual.id, expected.id, "id")
    assert_value(actual.title, expected.title, "title")
    assert_value(actual.course_id, expected.course_id, "course_id")
    assert_value(actual.max_score, expected.max_score, "max_score")
    assert_value(actual.min_score, expected.min_score, "min_score")
    assert_value(actual.order_index, expected.order_index, "order_index")
    assert_value(actual.description, expected.description, "description")
    assert_value(actual.estimated_time, expected.estimated_time, "estimated_time")

@allure.step("Проверка ответа на запрос упражнения")
def assert_get_exercise_response(actual: GetExerciseResponseSchema, expected: CreateExerciseResponseSchema):
    """
    Проверяет соответствие ответа на получение упражнения и ответа на создание упражнения

    :param actual: Ответ на получение упражнения по id
    :param expected: Ответ на создание упражнения
    :return AssertionError: Если данные не совпадают
    """
    logger.info("Проверка ответа на запрос упражнения")
    assert_exercise(actual.exercise, expected.exercise)

@allure.step("Проверка ответа на запрос обновления упражнения")
def assert_update_exercise_response(response: UpdateExerciseResponseSchema, request: UpdateExerciseRequestSchema):
    """
    Проверяет соответствие запроса и ответа на обновление упражнения

    :param response: Ответ на получение упражнения по id
    :param request: Ответ на создание упражнения
    :return AssertionError: Если данные не совпадают
    """
    logger.info("Проверка ответа на запрос обновления упражнения")
    assert_is_true(response.exercise.id, "id")
    assert_value(response.exercise.title, request.title, "title")
    assert_is_true(response.exercise.course_id, "course_id")
    assert_value(response.exercise.max_score, request.max_score, "max_score")
    assert_value(response.exercise.min_score, request.min_score, "min_score")
    assert_value(response.exercise.order_index, request.order_index, "order_index")
    assert_value(response.exercise.description, request.description, "description")
    assert_value(response.exercise.estimated_time, request.estimated_time, "estimated_time")

@allure.step("Проверка ответа на запрос ненайденного упражнения")
def assert_exercise_not_found_response(actual: InternalErrorResponseSchema):
    """
    Функция для проверки ошибки, если упражнение не найдено на сервере.

    :param actual: Фактический ответ.
    :raises AssertionError: Если фактический ответ не соответствует ошибке "Exercise not found"
    """
    logger.info("Проверка ответа на запрос ненайденного упражнения")
    expected = InternalErrorResponseSchema(details="Exercise not found")
    assert_internal_error_response(actual, expected)

@allure.step("Проверка ответа на запрос списка упражнений")
def assert_get_exercises_response(
        get_exercises_response: GetExercisesResponseSchema,
        create_exercises_response: list[CreateExerciseResponseSchema]
):
    """
    Проверяет, что ответ на получение упражнений соответствует списку созданных упражнений

    :param get_exercises_response: Схема ответа на получение упражнений
    :param create_exercises_response: Схема ответа на создание упражнений
    :raises AssertionError: Если хотя бы одно поле не совпадает
    """
    logger.info("Проверка ответа на запрос списка упражнений")
    assert_value(len(get_exercises_response.exercises), len(create_exercises_response), "courses")

    for index, create_course_response in enumerate(create_exercises_response):
        assert_exercise(get_exercises_response.exercises[index], create_course_response.exercise)