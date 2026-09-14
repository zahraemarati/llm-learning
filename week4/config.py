from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):

    openrouter_api_key: str
    bai_api_key: str

    chat_model: str = "mimo-v2.5"
    embed_model: str = "nvidia/nemotron-3-embed-1b:free"

    chroma_path: str = "./chroma_db"
    collection_name: str = "pdf_documents"


    model_config = SettingsConfigDict(
        env_file=".env"
    )


settings = Settings()