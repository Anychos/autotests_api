from http import HTTPStatus

import allure
import pytest

from clients.courses.courses_client import CoursesAPIClient
from clients.courses.courses_schema import (
    CreateCourseRequestSchema,
    CreateCourseResponseSchema,
    GetCourseByUserResponseSchema,
    GetCoursesQuerySchema,
    UpdateCourseRequestSchema,
    UpdateCourseResponseSchema,
)
from fixtures.courses import CoursesFixture
from fixtures.files import FileFixture
from fixtures.users import UserFixture, function_create_user
from tools.allure.epics import AllureEpic
from tools.allure.features import AllureFeature
from tools.allure.parent_suite import AllureParentSuite
from tools.allure.stories import AllureStory
from tools.allure.sub_suite import AllureSubSuite
from tools.allure.suite import AllureSuite
from tools.allure.tags import AllureTags
from tools.assertions.courses import (
    assert_create_course_response,
    assert_get_courses_response,
    assert_update_course_response,
)
from tools.assertions.schema import validate_json_schema
from tools.assertions.base_assertions import assert_status_code


@pytest.mark.regression
@pytest.mark.smoke
@pytest.mark.courses
@allure.tag(AllureTags.COURSES, AllureTags.REGRESSION, AllureTags.SMOKE, AllureTags.POSITIVE)
@allure.epic(AllureEpic.LMS)
@allure.feature(AllureFeature.COURSES)
@allure.parent_suite(AllureParentSuite.LMS)
@allure.suite(AllureSuite.COURSES)
class TestCoursesPositive:
    @allure.tag(AllureTags.CREATE_ENTITY)
    @allure.story(AllureStory.CREATE_ENTITY)
    @allure.sub_suite(AllureSubSuite.CREATE_ENTITY)
    @allure.title("Создание нового курса")
    def test_create_course(self, courses_client: CoursesAPIClient, function_create_user: UserFixture, function_create_file: FileFixture):
        request = CreateCourseRequestSchema(
            preview_file_id=function_create_file.response.file.id,
            created_by_user_id=function_create_user.response.user.id
        )

        response = courses_client.create_course_api(request)
        response_data = CreateCourseResponseSchema.model_validate_json(response.text)

        assert_status_code(response.status_code, HTTPStatus.OK)
        validate_json_schema(instance=response.json(), schema=response_data.model_json_schema())
        assert_create_course_response(response_data, request)

    @allure.tag(AllureTags.UPDATE_ENTITY)
    @allure.story(AllureStory.UPDATE_ENTITY)
    @allure.sub_suite(AllureSubSuite.UPDATE_ENTITY)
    @allure.title("Обновление данных курса")
    def test_update_course(self, function_create_course: CoursesFixture, courses_client: CoursesAPIClient):
        request = UpdateCourseRequestSchema()

        response = courses_client.update_course_api(function_create_course.response.course.id, request)
        response_data = UpdateCourseResponseSchema.model_validate_json(response.text)

        assert_status_code(response.status_code, HTTPStatus.OK)
        validate_json_schema(instance=response.json(), schema=response_data.model_json_schema())
        assert_update_course_response(request, response_data)

    @allure.tag(AllureTags.GET_ENTITIES)
    @allure.story(AllureStory.GET_ENTITIES)
    @allure.sub_suite(AllureSubSuite.GET_ENTITY)
    @allure.title("Получение списка курсов")
    def test_get_courses(self, courses_client: CoursesAPIClient, function_create_user: UserFixture, function_create_course: CoursesFixture):
        query = GetCoursesQuerySchema(user_id=function_create_user.response.user.id)
        response = courses_client.get_courses_api(query)
        response_data = GetCourseByUserResponseSchema.model_validate_json(response.text)

        assert_status_code(response.status_code, HTTPStatus.OK)
        assert_get_courses_response(response_data, [function_create_course.response])
        validate_json_schema(instance=response.json(), schema=response_data.model_json_schema())