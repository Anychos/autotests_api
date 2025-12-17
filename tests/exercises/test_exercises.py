from http import HTTPStatus

import allure
import pytest

from clients.error_schema import InternalErrorResponseSchema
from clients.exercises.exercises_client import ExercisesAPIClient
from clients.exercises.exercises_schema import (
    CreateExerciseRequestSchema,
    CreateExerciseResponseSchema,
    DeleteExerciseQuerySchema,
    GetExerciseQuerySchema,
    GetExerciseResponseSchema,
    GetExercisesQuerySchema,
    GetExercisesResponseSchema,
    UpdateExerciseQuerySchema,
    UpdateExerciseRequestSchema,
    UpdateExerciseResponseSchema,
)
from fixtures.courses import CoursesFixture
from fixtures.exercises import ExercisesFixture
from tools.allure.epics import AllureEpic
from tools.allure.features import AllureFeature
from tools.allure.parent_suite import AllureParentSuite
from tools.allure.stories import AllureStory
from tools.allure.sub_suite import AllureSubSuite
from tools.allure.suite import AllureSuite
from tools.allure.tags import AllureTags
from tools.assertions.exercises import (
    assert_create_exercise_response,
    assert_exercise_not_found_response,
    assert_get_exercise_response,
    assert_get_exercises_response,
    assert_update_exercise_response,
)
from tools.assertions.schema import validate_json_schema
from tools.assertions.base_assertions import assert_status_code


@pytest.mark.regression
@pytest.mark.smoke
@pytest.mark.exercises
@allure.tag(AllureTags.EXERCISES, AllureTags.REGRESSION, AllureTags.SMOKE, AllureTags.POSITIVE)
@allure.epic(AllureEpic.LMS)
@allure.feature(AllureFeature.EXERCISES)
@allure.parent_suite(AllureParentSuite.LMS)
@allure.suite(AllureSuite.EXERCISES)
class TestExercisesPositive:
    @allure.tag(AllureTags.CREATE_ENTITY)
    @allure.story(AllureStory.CREATE_ENTITY)
    @allure.sub_suite(AllureSubSuite.CREATE_ENTITY)
    @allure.title("Создание нового упражнения")
    def test_create_exercise(self, exercises_client: ExercisesAPIClient, function_create_course: CoursesFixture):
        request = CreateExerciseRequestSchema(course_id=function_create_course.response.course.id)

        response = exercises_client.create_exercise_api(request)
        response_data = CreateExerciseResponseSchema.model_validate_json(response.text)

        assert_status_code(response.status_code, HTTPStatus.OK)
        validate_json_schema(instance=response.json(), schema=response_data.model_json_schema())
        assert_create_exercise_response(response_data, request)

    @allure.tag(AllureTags.GET_ENTITY)
    @allure.story(AllureStory.GET_ENTITY)
    @allure.sub_suite(AllureSubSuite.GET_ENTITY)
    @allure.title("Получение данных упражнения")
    def test_get_exercise(self, function_create_exercise: ExercisesFixture, exercises_client: ExercisesAPIClient):
        query = GetExerciseQuerySchema(exercise_id=function_create_exercise.response.exercise.id)
        response = exercises_client.get_exercise_api(query=query)
        response_data = GetExerciseResponseSchema.model_validate_json(response.text)

        assert_status_code(response.status_code, HTTPStatus.OK)
        validate_json_schema(instance=response.json(), schema=response_data.model_json_schema())
        assert_get_exercise_response(response_data, function_create_exercise.response)

    @allure.tag(AllureTags.UPDATE_ENTITY)
    @allure.story(AllureStory.UPDATE_ENTITY)
    @allure.sub_suite(AllureSubSuite.UPDATE_ENTITY)
    @allure.title("Обновление данных упражнения")
    def test_update_exercise(self, function_create_exercise: ExercisesFixture, exercises_client: ExercisesAPIClient):
        query = UpdateExerciseQuerySchema(exercise_id=function_create_exercise.response.exercise.id)
        request = UpdateExerciseRequestSchema()

        response = exercises_client.update_exercise_api(query=query, request_body=request)
        response_data = UpdateExerciseResponseSchema.model_validate_json(response.text)

        assert_status_code(response.status_code, HTTPStatus.OK)
        validate_json_schema(instance=response.json(), schema=response_data.model_json_schema())
        assert_update_exercise_response(response_data, request)

    @allure.tag(AllureTags.DELETE_ENTITY)
    @allure.story(AllureStory.DELETE_ENTITY)
    @allure.sub_suite(AllureSubSuite.DELETE_ENTITY)
    @allure.title("Удаление упражнения")
    def test_delete_exercise(self, function_create_exercise: ExercisesFixture, exercises_client: ExercisesAPIClient):
        delete_query = DeleteExerciseQuerySchema(exercise_id=function_create_exercise.response.exercise.id)
        delete_response = exercises_client.delete_exercise_api(query=delete_query)

        assert_status_code(delete_response.status_code, HTTPStatus.OK)

        get_query = GetExerciseQuerySchema(exercise_id=function_create_exercise.response.exercise.id)
        get_response = exercises_client.get_exercise_api(query=get_query)
        get_response_data = InternalErrorResponseSchema.model_validate_json(get_response.text)

        assert_status_code(get_response.status_code, HTTPStatus.NOT_FOUND)
        assert_exercise_not_found_response(actual=get_response_data)
        validate_json_schema(instance=get_response.json(), schema=get_response_data.model_json_schema())

    @allure.tag(AllureTags.GET_ENTITIES)
    @allure.story(AllureStory.GET_ENTITIES)
    @allure.sub_suite(AllureSubSuite.GET_ENTITIES)
    @allure.title("Получение списка упражнений курса")
    def test_get_exercises(self, function_create_course: CoursesFixture, function_create_exercise: ExercisesFixture, exercises_client: ExercisesAPIClient):
        query = GetExercisesQuerySchema(course_id=function_create_course.response.course.id)
        response = exercises_client.get_exercises_api(query=query)
        response_data = GetExercisesResponseSchema.model_validate_json(response.text)

        assert_status_code(response.status_code, HTTPStatus.OK)
        assert_get_exercises_response(response_data, [function_create_exercise.response])
        validate_json_schema(instance=response.json(), schema=response_data.model_json_schema())
