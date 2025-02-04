import os

from starlette.config import Config

env_files = ["dev.env", "prod.env"]

config = Config()
for env_file in env_files:
    if os.path.exists(env_file):
        config = Config(env_file)

# Base
API_V1_PREFIX = config("API_V1_PREFIX", cast=str)
DEBUG = config("DEBUG", cast=bool)
PROJECT_NAME = config("PROJECT_NAME", cast=str)
VERSION = config("VERSION", cast=str, default="1.0.0")

# Scrapers settings
SITE_ENTRYPOINT = config("SITE_ENTRYPOINT", cast=str)