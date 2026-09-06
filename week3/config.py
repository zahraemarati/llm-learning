from pydantic_settings import BaseSettings


class Settings(BaseSettings):

    openrouter_api_key: str
    bai_api_key: str

    chat_model: str = "glm-5.3-flash"
    embed_model: str = "nvidia/nemotron-3-embed-1b:free"


    class Config:
        env_file = ".env"


settings = Settings()