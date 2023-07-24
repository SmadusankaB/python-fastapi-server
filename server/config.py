import os
import pathlib


class BaseConfig:
    # global env
    BASE_DIR: pathlib.Path = pathlib.Path(__file__).parent.parent
    UPLOADS_DEST: str = str(BASE_DIR / "uploads")
    ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif"}
    LOGGER_NAME = "tg_logger"

    # mongo env
    DATABASE_HOST: str = os.environ.get("DATABASE_HOST", "localhost")
    DATABASE_PORT: str = os.environ.get("DATABASE_PORT", "27017")
    DATABASE_NAME: str = os.environ.get("DATABASE_NAME", "celery_db")
    DATABASE_USER: str = os.environ.get("DATABASE_USER")
    DATABASE_PASSWORD: str = os.environ.get("DATABASE_PASSWORD")

    MONGO_CONNECTION_STRING = f"mongodb://{DATABASE_HOST}:{int(DATABASE_PORT)}"
    if DATABASE_USER and DATABASE_PASSWORD:
        MONGO_CONNECTION_STRING: str = f"mongodb://{DATABASE_USER}:{DATABASE_PASSWORD}@{DATABASE_HOST}:{int(DATABASE_PORT)}"

    # rabbitmq env
    RABBITMQ_HOST: str = os.environ.get("RABBITMQ_HOST", "localhost")
    RABBITMQ_PORT: str = os.environ.get("RABBITMQ_PORT", "5672")
    RABBITMQ_USER: str = os.environ.get("RABBITMQ_USER", "guest")
    RABBITMQ_PASSWORD: str = os.environ.get("RABBITMQ_PASSWORD", "guest")
    
    CELERY_BROKER_URL: str = os.environ.get(
            "CELERY_BROKER_URL",
            f"amqp://{RABBITMQ_HOST}:{RABBITMQ_PORT}/",
        )
    if RABBITMQ_USER and RABBITMQ_PASSWORD:
        CELERY_BROKER_URL: str = os.environ.get(
            "CELERY_BROKER_URL",
            f"amqp://{RABBITMQ_USER}:{RABBITMQ_PASSWORD}@{RABBITMQ_HOST}:{RABBITMQ_PORT}/",
        )

    CELERY_RESULT_BACKEND: str = f"{MONGO_CONNECTION_STRING}/{DATABASE_NAME}"


class DevelopmentConfig(BaseConfig):
    LOG_LEVEL: str = os.environ.get("LOG_LEVEL", "DEBUG").upper()


class ProductionConfig(BaseConfig):
    LOG_LEVEL: str = os.environ.get("LOG_LEVEL", "INFO").upper()


class TestingConfig(BaseConfig):
    pass


def get_settings():
    """
    Create correct config class based on value in APP_CONFIG env

    Returns
    -------
    is_correct_file: cls object
        Return DevelopmentConfig,  ProductionConfig or TestingConfig
    """
    config_cls_dict = {
        "development": DevelopmentConfig,
        "production": ProductionConfig,
        "testing": TestingConfig,
    }

    config_name = os.environ.get("APP_CONFIG", "development")
    config_cls = config_cls_dict[config_name]
    return config_cls()


settings = get_settings()
