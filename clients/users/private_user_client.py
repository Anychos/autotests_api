import allure
from httpx import Response

from clients.api_coverage import tracker
from clients.base_client import BaseAPIClient
from clients.private_builder import AuthUserSchema, get_private_client
from clients.users.users_schema import GetUserResponseSchema, UpdateUserRequestSchema
from tools.routes import APIRoutes


class PrivateUserAPIClient(BaseAPIClient):
    """
    Клиент для работы с методами авторизованного пользователя
    """
    @allure.step("Получение текущего пользователя")
    @tracker.track_coverage_httpx(f'{APIRoutes.USERS}/me')
    def get_user_me_api(self) -> Response:
        """
        Получение информации о текущем пользователе

        :return: ответ сервера
        """
        return self.get(f'{APIRoutes.USERS}/me')

    @allure.step("Получение пользователя по id: {user_id}")
    @tracker.track_coverage_httpx(APIRoutes.USERS + '/{user_id}')
    def get_user_by_id_api(self, user_id: str) -> Response:
        """
        Получение информации о пользователе по id

        :param user_id: id пользователя
        :return: ответ сервера
        """
        return self.get(f'{APIRoutes.USERS}/{user_id}')

    @allure.step("Получение пользователя по id: {user_id} и валидация ответа по схеме")
    def get_user_by_id(self, user_id: str) -> GetUserResponseSchema:
        """
        Функция для получения сущности пользователя

        :param user_id: id пользователя
        :return: ответ сервера
        """
        response = self.get_user_by_id_api(user_id)
        return GetUserResponseSchema.model_validate_json(response.text)

    @allure.step("Обновление пользователя с id: {user_id}")
    @tracker.track_coverage_httpx(APIRoutes.USERS + '/{user_id}')
    def update_user_api(self, user_id: str, request_body: UpdateUserRequestSchema) -> Response:
        """
        Обновление информации о пользователе

        :param user_id: id пользователя
        :param request_body: параметры запроса
        :return: ответ сервера
        """
        return self.patch(f'{APIRoutes.USERS}/{user_id}', json=request_body.model_dump(by_alias=True))

    @allure.step("Удаление пользователя с id: {user_id}")
    @tracker.track_coverage_httpx(APIRoutes.USERS + '/{user_id}')
    def delete_user_api(self, user_id: str) -> Response:
        """
        Удаление пользователя по id

        :param user_id: id пользователя
        :return: ответ сервера
        """
        return self.delete(f'{APIRoutes.USERS}/{user_id}')

@allure.step("Получение клиента для работы с приватным API")
def get_private_user_client(user: AuthUserSchema) -> PrivateUserAPIClient:
    """
    Функция получения клиента для работы с приватными методами

    :return: Готовый к использованию Client
    """
    return PrivateUserAPIClient(client=get_private_client(user))