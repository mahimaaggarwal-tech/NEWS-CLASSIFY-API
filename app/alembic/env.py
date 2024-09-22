# alembic/env.py
import sys
from pathlib import Path

# Add the app directory to the system path
sys.path.append(str(Path(__file__).resolve().parent.parent))

from app.db.news_items import NewsItem
from app.db.job_status import JobStatus


from alembic import context
from sqlalchemy import engine_from_config, pool
from logging.config import fileConfig

# Import your models and Base
from app.db.base import Base  # or app.core.models, depending on where you have your models

# This is the Alembic Config object, which provides access to the .ini file values
config = context.config

# Interpret the config file for Python logging.
fileConfig(config.config_file_name)

# Add your models' MetaData object here
target_metadata = Base.metadata

def run_migrations_offline():
    """Run migrations in 'offline' mode."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(url=url, target_metadata=target_metadata, literal_binds=True)

    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online():
    """Run migrations in 'online' mode."""
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)

        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
