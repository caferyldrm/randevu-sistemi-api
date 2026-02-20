from logging.config import fileConfig
from sqlalchemy import engine_from_config
from sqlalchemy import pool
from alembic import context
import os
from dotenv import load_dotenv

# 1. .env dosyasını oku
load_dotenv()

config = context.config

# 2. .env içindeki DATABASE_URL'yi Alembic'e bağla
database_url = os.getenv("DATABASE_URL")
if not database_url:
    raise ValueError("DATABASE_URL bulunamadı! .env dosyanı kontrol et.")
config.set_main_option("sqlalchemy.url", database_url)

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# 3. Kendi Base ve Modellerimizi import et (ÇOK ÖNEMLİ)
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__))) # Proje kök dizinini yola ekle

from app.db.database import Base
from app.db import models # Tüm modelleri tanıması için

target_metadata = Base.metadata

def run_migrations_offline() -> None:
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online() -> None:
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )
    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata
        )
        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()