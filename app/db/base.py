from app.db.session import Base

# Import all models here so that they are registered with SQLAlchemy
# (IMPORTANT for Alembic and table creation)

from app.db import models  # noqa