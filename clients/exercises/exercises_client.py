import allure
from httpx import Response

from clients.api_coverage import tracker
from clients.base_client import BaseAPIClient
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
from clients.private_builder import AuthUserSchema, get_private_client
from tools.routes import APIRoutes


class ExercisesAPIClient(BaseAPIClient):
    """
    Клиент для работы с упражнениями
    """
    @allure.step("Получение списка упражнений")
    @tracker.track_coverage_httpx(APIRoutes.EXERCISES)
    def get_exercises_api(self, query: GetExercisesQuerySchema) -> Response:
        """
        Выполняет GET запрос для получения списка упражнений

        :param query: Параметры запроса
        :return: Ответ сервера
        """
        return self.get(APIRoutes.EXERCISES, params=query.model_dump(by_alias=True))

    @allure.step("Получение списка упражнений и валидация ответа по схеме")
    def get_exercises(self, course_id: GetExercisesQuerySchema) -> GetExercisesResponseSchema:
        response = self.get_exercises_api(course_id)
        return response.json()

    @allure.step("Получение данных упражнения с id: {query}")
    @tracker.track_coverage_httpx(APIRoutes.EXERCISES + '/{exercise_id}')
    def get_exercise_api(self, query: GetExerciseQuerySchema) -> Response:
        """
        Выполняет GET запрос для получения упражнения по его id

        :param query: id упражнения
        :return: Ответ сервера
        """
        return self.get(f"{APIRoutes.EXERCISES}/{query.exercise_id}")

    @allure.step("Получение упражнения с id: {query}")
    def get_exercise(self, query: GetExerciseQuerySchema) -> GetExerciseResponseSchema:
        response = self.get_exercise_api(query=query)
        return GetExerciseResponseSchema.model_validate_json(response.text)

    @allure.step("Создание нового упражнения")
    @tracker.track_coverage_httpx(APIRoutes.EXERCISES)
    def create_exercise_api(self, request_body: CreateExerciseRequestSchema) -> Response:
        """
        Выполняет POST запрос для создания упражнения

        :param request_body: Тело запроса 
        :return: Ответ сервера
        """
        return self.post(APIRoutes.EXERCISES, json=request_body.model_dump(by_alias=True))

    @allure.step("Создание упражнения и валидация ответа по схеме")
    def create_exercise(self, request_body: CreateExerciseRequestSchema) -> CreateExerciseResponseSchema:
        response = self.create_exercise_api(request_body)
        return CreateExerciseResponseSchema.model_validate_json(response.text)

    @allure.step("Обновление упражнения с id: {query}")
    @tracker.track_coverage_httpx(APIRoutes.EXERCISES + '/{exercise_id}')
    def update_exercise_api(self, query: UpdateExerciseQuerySchema, request_body: UpdateExerciseRequestSchema) -> Response:
        """
        Выполняет PATCH запрос для обновления упражнения

        :param query: id упражнения
        :param request_body: Тело запроса
        :return: Ответ сервера
        """
        return self.patch(f"{APIRoutes.EXERCISES}/{query.exercise_id}", json=request_body.model_dump(by_alias=True))

    @allure.step("Обновление упражнения с id: {query} и валидация ответа по схеме")
    def update_exercise(self, exercise_id: UpdateExerciseQuerySchema, request_body: UpdateExerciseRequestSchema) -> UpdateExerciseResponseSchema:
        response = self.update_exercise_api(exercise_id, request_body)
        return UpdateExerciseResponseSchema.model_validate_json(response.text)

    @allure.step("Удаления упражнения с id: {query}")
    @tracker.track_coverage_httpx(APIRoutes.EXERCISES + '/{exercise_id}')
    def delete_exercise_api(self, query: DeleteExerciseQuerySchema) -> Response:
        """
        Выполняет DELETE запрос для удаления упражнения

        :param query: id упражнения
        :return: Ответ сервера
        """
        return self.delete(f"{APIRoutes.EXERCISES}/{query.exercise_id}")

@allure.step("Получение клиента для работы с API упражнений")
def get_private_exercises_client(user: AuthUserSchema) -> ExercisesAPIClient:
    """
    Функция получения клиента для работы с упражнениями

    :return: Готовый к использованию Client
    """
    return ExercisesAPIClient(client=get_private_client(user))