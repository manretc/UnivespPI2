import logging
from logging.config import fileConfig

from alembic import context
from app import create_app
from app.extensions import db  # 👈 importe daqui

# Alembic Config
config = context.config

fileConfig(config.config_file_name)
logger = logging.getLogger("alembic.env")

# Cria a aplicação
app = create_app()


def get_metadata():
    return db.metadata


def run_migrations_offline():
    with app.app_context():
        url = str(db.engine.url).replace("%", "%%")
        context.configure(
            url=url,
            target_metadata=get_metadata(),
            literal_binds=True,
        )

        with context.begin_transaction():
            context.run_migrations()


def run_migrations_online():
    with app.app_context():  # 👈 AQUI está a mágica

        def process_revision_directives(context_, revision, directives):
            if getattr(config.cmd_opts, "autogenerate", False):
                script = directives[0]
                if script.upgrade_ops.is_empty():
                    directives[:] = []
                    logger.info("No changes in schema detected.")

        connectable = db.engine

        with connectable.connect() as connection:
            context.configure(
                connection=connection,
                target_metadata=get_metadata(),
                process_revision_directives=process_revision_directives,
            )

            with context.begin_transaction():
                context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()