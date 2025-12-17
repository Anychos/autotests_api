import allure
from httpx import Response

from clients.api_coverage import tracker
from clients.base_client import BaseAPIClient
from clients.public_builder import get_public_client
from clients.users.users_schema import CreateUserRequestSchema, CreateUserResponseSchema
from tools.routes import APIRoutes


class PublicUserAPIClient(BaseAPIClient):
    """
    Клиент для работы с публичными методами пользователя
    """
    @allure.step("Создание пользователя")
    @tracker.track_coverage_httpx(APIRoutes.USERS)
    def create_user_api(self, request_body: CreateUserRequestSchema) -> Response:
        """
        Выполняет POST запрос для создания пользователя

        :param request_body: словарь с данными пользователя
        :return: ответ сервера
        """
        return self.post(APIRoutes.USERS, json=request_body.model_dump(by_alias=True))

    @allure.step("Создание пользователя и валидация ответа по схеме")
    def create_user(self, request_body: CreateUserRequestSchema) -> CreateUserResponseSchema:
        response = self.create_user_api(request_body)
        return CreateUserResponseSchema.model_validate_json(response.text)

@allure.step("Получение клиента для работы с публичным API")
def get_public_user_client() -> PublicUserAPIClient:
    """
    Функция получения клиента для работы с публичными методами

    :return: Готовый к использованию Client
    """
    return PublicUserAPIClient(client=get_public_client())