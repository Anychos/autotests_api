import allure
from httpx import Response

from clients.api_coverage import tracker
from clients.base_client import BaseAPIClient
from clients.courses.courses_schema import (
    CreateCourseRequestSchema,
    CreateCourseResponseSchema,
    GetCoursesQuerySchema,
    UpdateCourseRequestSchema,
)
from clients.private_builder import AuthUserSchema, get_private_client
from tools.routes import APIRoutes


class CoursesAPIClient(BaseAPIClient):
    """
    Клиент для работы с курсами
    """
    @allure.step("Получение списка курсов")
    @tracker.track_coverage_httpx(APIRoutes.COURSES)
    def get_courses_api(self, query: GetCoursesQuerySchema) -> Response:
        """
        Получение информации о курсе по id пользователя

        :param query: id пользователя
        :return: Ответ сервера с сущностью курса
        """
        return self.get(APIRoutes.COURSES, params=query.model_dump(by_alias=True))

    @allure.step("Получение курса с id: {course_id}")
    @tracker.track_coverage_httpx(APIRoutes.COURSES + '/{course_id}')
    def get_course_api(self, course_id: str) -> Response:
        """
        Получение информации о курсе по его id

        :param course_id: id курса
        :return: Ответ сервера с сущностью курса
        """
        return self.get(f'{APIRoutes.COURSES}/{course_id}')

    @allure.step("Создание курса")
    @tracker.track_coverage_httpx(APIRoutes.COURSES)
    def create_course_api(self, request_body: CreateCourseRequestSchema) -> Response:
        """
        Создание курса

        :param request_body: Тело запроса с данными курса
        :return: Ответ сервера с сущностью созданного курса
        """
        return self.post(APIRoutes.COURSES, json=request_body.model_dump(by_alias=True))

    @allure.step("Создание курса и валидация ответа по схеме")
    def create_course(self, request_body: CreateCourseRequestSchema) -> CreateCourseResponseSchema:
        response = self.create_course_api(request_body)
        return CreateCourseResponseSchema.model_validate_json(response.text)

    @allure.step("Обновление курса")
    @tracker.track_coverage_httpx(APIRoutes.COURSES + '/{course_id}')
    def update_course_api(self, course_id: str, request_body: UpdateCourseRequestSchema) -> Response:
        """
        Обновление курса

        :param course_id: id курса
        :param request_body: Тело запроса с данными для обновления
        :return: Ответ сервера с обновленной сущностью курса
        """
        return self.patch(f'{APIRoutes.COURSES}/{course_id}', json=request_body.model_dump(by_alias=True))

    @allure.step("Удаление курса")
    @tracker.track_coverage_httpx(APIRoutes.COURSES + '/{course_id}')
    def delete_course_api(self, course_id: str) -> Response:
        return self.delete(f'{APIRoutes.COURSES}/{course_id}')

@allure.step("Получение клиента для работы с API курсов")
def get_private_courses_client(user: AuthUserSchema) -> CoursesAPIClient:
    """
    Функция получения клиента для работы с методами курсов

    :return: Готовый к использованию Client
    """
    return CoursesAPIClient(client=get_private_client(user))