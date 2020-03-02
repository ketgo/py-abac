"""
    MongoDB migrations
"""

import logging

from .storage import MongoStorage
from ..migration import Migration, MigrationSet

DEFAULT_MIGRATION_COLLECTION = "py_abac_migrations"

LOG = logging.getLogger(__name__)


class MongoMigrationSet(MigrationSet):
    """
        Migrations Collection for MongoStorage
    """

    def __init__(self, storage: MongoStorage, collection: str = DEFAULT_MIGRATION_COLLECTION):
        self.storage = storage
        self.collection = self.storage.database[collection]
        self.key = 'version'
        self.filter = {'_id': 'migration_version'}

    def migrations(self):
        return [
            MongoMigration0To0x2x0(self.storage),
        ]

    def save_applied_number(self, number: int):
        self.collection.update_one(self.filter, {'$set': {self.key: number}}, upsert=True)

    def last_applied(self):
        data = self.collection.find_one(self.filter)
        if data:
            return int(data[self.key])
        return 0


class MongoMigration0To0x2x0(Migration):
    """
        Migration between versions 0 and 0.2.0
    """

    def __init__(self, storage: MongoStorage):
        self.storage = storage
        self.index_name = lambda i: i.replace('.', "_") + '_idx'
        self.multi_key_indices = [
            'tags.action.id',
            'tags.subject.id',
            'tags.resource.id',
        ]

    @property
    def order(self):
        return 1

    def up(self):
        for field in self.multi_key_indices:
            self.storage.collection.create_index(field, name=self.index_name(field))

    def down(self):
        for field in self.multi_key_indices:
            self.storage.collection.drop_index(self.index_name(field))
