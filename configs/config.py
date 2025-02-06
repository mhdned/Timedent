import os

from dotenv import dotenv_values

run_environment: str = os.environ.get("ENV")
current_directory = os.getcwd()
path_environment: str

if run_environment == "DEV":
    path_environment = os.path.join(current_directory, "configs\envs\.env.dev")
elif run_environment == "PROD":
    path_environment = os.path.join(current_directory, "configs\envs\.env.prod")
else:
    path_environment = os.path.join(current_directory, "configs\envs\.env")

config_dict = dotenv_values(path_environment)
config_dict["PATH"] = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class Config:
    """
    Type:

    class, configuration

    Description:

    The Config class is a simple and effective way to manage configuration
    settings for your Python application using environment variables.
    """

    def __init__(self):
        self.DATABASE_URL = config_dict["DATABASE_URL"]
        self.SECRET_KEY = config_dict["SECRET_KEY"]
        self.PORT = config_dict["PORT"]
        self.HOST = config_dict["HOST"]
        self.TITLE = config_dict["TITLE"]
        self.PATH = config_dict["PATH"]
        self.UPLOAD_PATH = config_dict["UPLOAD_PATH"]


config = Config()
