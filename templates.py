import os
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO, format='[%(asctime)s]: %(message)s:')

project_name = "fin_guard_api"

list_of_files = [

    # APP ENTRY
    "app/__init__.py",
    "app/main.py",

    # CORE CONFIG
    "app/core/__init__.py",
    "app/core/config.py",
    "app/core/security.py",

    # DATABASE
    "app/db/__init__.py",
    "app/db/session.py",
    "app/db/base.py",
    "app/db/models.py",

    # API ROUTES
    "app/api/__init__.py",
    "app/api/routes/__init__.py",
    "app/api/routes/auth.py",
    "app/api/routes/users.py",
    "app/api/routes/records.py",
    "app/api/routes/dashboard.py",

    # SCHEMAS (Pydantic)
    "app/schemas/__init__.py",
    "app/schemas/user.py",
    "app/schemas/auth.py",
    "app/schemas/record.py",
    "app/schemas/dashboard.py",


    # SERVICES (BUSINESS LOGIC)
    "app/services/__init__.py",
    "app/services/user_service.py",
    "app/services/auth_service.py",
    "app/services/record_service.py",
    "app/services/dashboard_service.py",

    # DEPENDENCIES (AUTH / ROLE)
    "app/dependencies/__init__.py",
    "app/dependencies/auth.py",
    "app/dependencies/roles.py",

    # MIDDLEWARES(LOGGING)
    "app/middlewares/__init__.py",
    "app/middlewares/logging.py",

    # UTILS
    "app/utils/__init__.py",
    "app/utils/logger.py",

    # CACHE
    "app/cache/__init__.py",
    "app/cache/redis_client.py",

    # TESTS
    "tests/__init__.py",
    "tests/test_auth.py",
    "tests/test_users.py",
    "tests/test_records.py",

    # CONFIG FILES
    "requirements.txt",
    ".env",
    ".gitignore",
    "README.md",

    # DOCKER
    "dockerfile",
    "docker-compose.yml",

]

# Create structure
for filepath in list_of_files:
    filepath = Path(filepath)
    filedir, filename = os.path.split(filepath)

    if filedir != "":
        os.makedirs(filedir, exist_ok=True)
        logging.info(f"Creating directory: {filedir} for file {filename}")

    if not os.path.exists(filepath):
        with open(filepath, 'w'):
            pass
        logging.info(f"Creating file: {filepath}")
    else:
        logging.info(f"{filename} already exists")