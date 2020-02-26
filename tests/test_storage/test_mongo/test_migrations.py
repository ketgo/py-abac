"""
    MongoDB storage migrations test
"""

import pytest

from py_abac.storage.mongo import MongoStorage
from py_abac.storage.mongo.migrations import MongoMigrationSet, MongoMigration0To0x2x0
from . import create_client

DB_NAME = 'db_test'
COLLECTION = 'policies_migration_test'
MIGRATION_COLLECTION = 'policies_migration_ver_test'


@pytest.fixture
def client():
    return create_client()


class TestMongoMigrationSet:

    @pytest.fixture
    def migration_set(self, client):
        storage = MongoStorage(client, DB_NAME, collection=COLLECTION)
        yield MongoMigrationSet(storage, MIGRATION_COLLECTION)
        client[DB_NAME][COLLECTION].drop()
        client[DB_NAME][MIGRATION_COLLECTION].drop()
        client.close()

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


class TestMongoMigration0To0x2x0:

    @pytest.yield_fixture
    def storage(self, client):
        yield MongoStorage(client, DB_NAME, collection=COLLECTION)
        client[DB_NAME][COLLECTION].drop()
        client.close()

    @pytest.yield_fixture
    def migration(self, storage):
        yield MongoMigration0To0x2x0(storage)

    def test_order(self, migration):
        assert 1 == migration.order

    def test_has_access_to_storage(self, migration):
        assert hasattr(migration, 'storage') and migration.storage is not None

    def test_up(self, migration, storage):
        migration.up()
        index_info = storage.collection.index_information()
        assert 'tags_action_id_idx' in index_info
        assert 'tags_subject_id_idx' in index_info
        assert 'tags_resource_id_idx' in index_info

    def test_down(self, migration, storage):
        migration.down()
        index_info = storage.collection.index_information()
        assert 'tags_action_id_idx' not in index_info
        assert 'tags_subject_id_idx' not in index_info
        assert 'tags_resource_id_idx' not in index_info
