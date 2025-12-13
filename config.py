from typing import Self

from pydantic import BaseModel, FilePath, HttpUrl, DirectoryPath
from pydantic_settings import BaseSettings, SettingsConfigDict


class HTTPClientSettings(BaseModel):
    base_url: HttpUrl
    timeout: int = 10

    @property
    def url(self) -> str:
        return str(self.base_url)

class TestDataSettings(BaseModel):
    image_png_file: FilePath

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        extra="allow", # позволяет создавать другие env переменные
        env_file=".env",
        env_file_encoding="utf-8",
        env_nested_delimiter='.'
    )

    test_data: TestDataSettings
    http_client: HTTPClientSettings
    allure_results_dir: DirectoryPath

    @classmethod
    def initialize(cls) -> Self:
        allure_results_dir = DirectoryPath("./allure-results")
        allure_results_dir.mkdir(exist_ok=True)
        return Settings(allure_results_dir=allure_results_dir)

settings = Settings.initialize()

