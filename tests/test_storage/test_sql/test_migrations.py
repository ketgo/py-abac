import pytest
from sqlalchemy.orm import sessionmaker, scoped_session

from py_abac.storage.sql import SQLStorage
from py_abac.storage.sql.migrations import SQLMigrationSet, Migration0To0x2x1
from py_abac.storage.sql.model import Base, PolicyModel, SubjectTargetModel, ResourceTargetModel, ActionTargetModel
from . import create_test_sql_engine


@pytest.fixture
def engine():
    return create_test_sql_engine()


@pytest.fixture
def session(engine):
    session = scoped_session(sessionmaker(bind=engine))
    yield session
    Base.metadata.drop_all(engine)


class TestSQLMigrationSet:

    @pytest.fixture
    def migration_set(self, session):
        storage = SQLStorage(scoped_session=session)
        yield SQLMigrationSet(storage)
        session.remove()

    def test_application_of_migration_number(self, migration_set):
        assert 0 == migration_set.last_applied()
        migration_set.save_applied_number(6)
        assert 6 == migration_set.last_applied()
        migration_set.save_applied_number(2)
        assert 2 == migration_set.last_applied()

    def test_up_and_down(self, migration_set):
        migration_set.save_applied_number(0)
        migration_set.up()
        assert 1 == migration_set.last_applied()
        migration_set.up()
        assert 1 == migration_set.last_applied()
        migration_set.down()
        assert 0 == migration_set.last_applied()
        migration_set.down()
        assert 0 == migration_set.last_applied()


class TestMigration0To0x2x1:

    @pytest.fixture
    def migration(self, session):
        storage = SQLStorage(scoped_session=session)
        yield Migration0To0x2x1(storage)
        session.remove()

    def test_order(self, migration):
        assert 1 == migration.order

    def test_has_access_to_storage(self, migration):
        assert hasattr(migration, 'storage') and migration.storage is not None

    def test_up(self, migration, engine):
        migration.up()
        assert Base.metadata.tables[PolicyModel.__tablename__].exists(engine)
        assert Base.metadata.tables[SubjectTargetModel.__tablename__].exists(engine)
        assert Base.metadata.tables[ResourceTargetModel.__tablename__].exists(engine)
        assert Base.metadata.tables[ActionTargetModel.__tablename__].exists(engine)

    def test_down(self, migration, engine):
        migration.down()
        assert not Base.metadata.tables[PolicyModel.__tablename__].exists(engine)
        assert not Base.metadata.tables[SubjectTargetModel.__tablename__].exists(engine)
        assert not Base.metadata.tables[ResourceTargetModel.__tablename__].exists(engine)
        assert not Base.metadata.tables[ActionTargetModel.__tablename__].exists(engine)
