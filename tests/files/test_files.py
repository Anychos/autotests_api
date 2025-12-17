from http import HTTPStatus

import allure
import pytest

from clients.error_schema import InternalErrorResponseSchema, ValidationErrorResponseSchema
from clients.files.files_client import FilesAPIClient
from clients.files.files_schema import CreateFileRequestSchema, CreateFileResponseSchema, GetFileResponseSchema
from fixtures.files import FileFixture
from tools.allure.epics import AllureEpic
from tools.allure.features import AllureFeature
from tools.allure.parent_suite import AllureParentSuite
from tools.allure.stories import AllureStory
from tools.allure.sub_suite import AllureSubSuite
from tools.allure.suite import AllureSuite
from tools.allure.tags import AllureTags
from tools.assertions.files import (
    assert_create_file_response,
    assert_create_file_with_empty_directory_response,
    assert_create_file_with_empty_filename_response,
    assert_file_not_found_response,
    assert_get_file_response,
    assert_get_file_with_incorrect_file_id_response,
)
from tools.assertions.schema import validate_json_schema
from tools.assertions.base_assertions import assert_status_code


@pytest.mark.files
@pytest.mark.regression
@pytest.mark.smoke
@allure.tag(AllureTags.FILES, AllureTags.REGRESSION, AllureTags.SMOKE, AllureTags.POSITIVE)
@allure.epic(AllureEpic.LMS)
@allure.feature(AllureFeature.FILES)
@allure.parent_suite(AllureParentSuite.LMS)
@allure.suite(AllureSuite.FILES)
class TestFilesPositive:
    @allure.tag(AllureTags.CREATE_ENTITY)
    @allure.story(AllureStory.CREATE_ENTITY)
    @allure.sub_suite(AllureSubSuite.CREATE_ENTITY)
    @allure.title("Создание файла")
    def test_create_file(self, files_client: FilesAPIClient):
        request = CreateFileRequestSchema()

        response = files_client.create_file_api(request)
        response_data = CreateFileResponseSchema.model_validate_json(response.text)

        assert_status_code(response.status_code, HTTPStatus.OK)
        validate_json_schema(instance=response.json(), schema=response_data.model_json_schema())
        assert_create_file_response(request, response_data)

    @allure.tag(AllureTags.GET_ENTITY)
    @allure.story(AllureStory.GET_ENTITY)
    @allure.sub_suite(AllureSubSuite.GET_ENTITY)
    @allure.title("Получение данных файла")
    def test_get_file(self, function_create_file: FileFixture, files_client: FilesAPIClient):
        response = files_client.get_file_api(function_create_file.response.file.id)
        response_data = GetFileResponseSchema.model_validate_json(response.text)

        assert_status_code(response.status_code, HTTPStatus.OK)
        validate_json_schema(instance=response.json(), schema=response_data.model_json_schema())
        assert_get_file_response(response_data, function_create_file.response)

    @allure.tag(AllureTags.DELETE_ENTITY)
    @allure.story(AllureStory.DELETE_ENTITY)
    @allure.sub_suite(AllureSubSuite.DELETE_ENTITY)
    @allure.title("Удаление файла")
    def test_delete_file(self, files_client: FilesAPIClient, function_create_file: FileFixture):
        delete_response = files_client.delete_file_api(function_create_file.response.file.id)

        assert_status_code(delete_response.status_code, HTTPStatus.OK)

        get_response = files_client.get_file_api(function_create_file.response.file.id)
        get_response_data = InternalErrorResponseSchema.model_validate_json(get_response.text)

        assert_status_code(get_response.status_code, HTTPStatus.NOT_FOUND)
        assert_file_not_found_response(get_response_data)
        validate_json_schema(get_response.json(), get_response_data.model_json_schema())

@pytest.mark.files
@pytest.mark.regression
@allure.tag(AllureTags.REGRESSION, AllureTags.FILES, AllureTags.NEGATIVE)
@allure.epic(AllureEpic.LMS)
@allure.feature(AllureFeature.FILES)
@allure.parent_suite(AllureParentSuite.LMS)
@allure.suite(AllureSuite.FILES)
class TestFilesNegative:
    @allure.tag(AllureTags.CREATE_ENTITY)
    @allure.story(AllureStory.CREATE_ENTITY)
    @allure.sub_suite(AllureSubSuite.CREATE_ENTITY)
    @allure.title("Создание файла без указания имени")
    def test_create_file_without_filename(self, files_client: FilesAPIClient):
        request = CreateFileRequestSchema(filename='')

        response = files_client.create_file_api(request)
        response_data = ValidationErrorResponseSchema.model_validate_json(response.text)

        assert_status_code(response.status_code, HTTPStatus.UNPROCESSABLE_ENTITY)
        assert_create_file_with_empty_filename_response(response_data)
        validate_json_schema(instance=response.json(), schema=response_data.model_json_schema())

    @allure.tag(AllureTags.CREATE_ENTITY)
    @allure.story(AllureStory.CREATE_ENTITY)
    @allure.sub_suite(AllureSubSuite.CREATE_ENTITY)
    @allure.title("Создание файла без указания директории")
    def test_create_file_without_directory(self, files_client: FilesAPIClient):
        request = CreateFileRequestSchema(directory='')

        response = files_client.create_file_api(request)
        response_data = ValidationErrorResponseSchema.model_validate_json(response.text)

        assert_status_code(response.status_code, HTTPStatus.UNPROCESSABLE_ENTITY)
        assert_create_file_with_empty_directory_response(response_data)
        validate_json_schema(instance=response.json(), schema=response_data.model_json_schema())

    @allure.tag(AllureTags.GET_ENTITY)
    @allure.story(AllureStory.GET_ENTITY)
    @allure.sub_suite(AllureSubSuite.GET_ENTITY)
    @allure.title("Получение файла с некорректным id")
    def test_get_file_with_incorrect_file_id(self, files_client: FilesAPIClient):
        response = files_client.get_file_api(file_id="incorrect-file-id")
        response_data = ValidationErrorResponseSchema.model_validate_json(response.text)

        assert_status_code(response.status_code, HTTPStatus.UNPROCESSABLE_ENTITY)
        assert_get_file_with_incorrect_file_id_response(response_data)
        validate_json_schema(instance=response.json(), schema=response_data.model_json_schema())