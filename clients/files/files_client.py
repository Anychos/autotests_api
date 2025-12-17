import allure
from httpx import Response

from clients.api_coverage import tracker
from clients.base_client import BaseAPIClient
from clients.files.files_schema import CreateFileRequestSchema, CreateFileResponseSchema
from clients.private_builder import AuthUserSchema, get_private_client
from tools.routes import APIRoutes


class FilesAPIClient(BaseAPIClient):
    """
    Клиент для работы с файлами
    """
    @allure.step("Получение файла")
    @tracker.track_coverage_httpx(APIRoutes.FILES + '/{file_id}')
    def get_file_api(self, file_id: str) -> Response:
        """
        Получение информации о файле по id

        :param file_id: id файла
        :return: Ответ сервера
        """
        return self.get(f'{APIRoutes.FILES}/{file_id}')

    @allure.step("Создание файла")
    @tracker.track_coverage_httpx(APIRoutes.FILES)
    def create_file_api(self, request_body: CreateFileRequestSchema) -> Response:
        """
        Загрузка файла

        :param request_body: Тело запроса
        :return: Ответ сервера
        """
        return self.post(
            APIRoutes.FILES,
            data=request_body.model_dump(by_alias=True, exclude={'upload_file'}),
            files={'upload_file': request_body.upload_file.read_bytes()}
        )

    @allure.step("Создание файла и валидация ответа по схеме")
    def create_file(self, request_body: CreateFileRequestSchema) -> CreateFileResponseSchema:
        response = self.create_file_api(request_body)
        return CreateFileResponseSchema.model_validate_json(response.text)

    @allure.step("Удаление файла")
    @tracker.track_coverage_httpx(APIRoutes.FILES + '/{file_id}')
    def delete_file_api(self, file_id: str) -> Response:
        """
        Удаление файла по id

        :param file_id: id файла
        :return: Ответ сервера
        """
        return self.delete(f'{APIRoutes.FILES}/{file_id}')

@allure.step("Получение клиента для работы с API файлов")
def get_private_files_client(user: AuthUserSchema) -> FilesAPIClient:
    """
    Функция получения клиента для работы с методами файлов

    :return: Готовый к использованию Client
    """
    return FilesAPIClient(client=get_private_client(user))