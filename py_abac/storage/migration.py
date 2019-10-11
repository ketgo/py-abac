"""
    Migration utilities for Storage Migrations
"""

import logging
from abc import ABCMeta, abstractmethod

log = logging.getLogger(__name__)


class Migration(metaclass=ABCMeta):
    """
        Manager for maintaining various migration actions of the storage: schema, indices, etc
    """

    @property
    @abstractmethod
    def order(self):
        """ Number of this migration in the row of migrations """
        raise NotImplementedError()

    @abstractmethod
    def up(self):
        """ Migrate DB schema up """
        raise NotImplementedError()

    @abstractmethod
    def down(self):
        """ Migrate DB schema down """
        raise NotImplementedError()


class MigrationSet(metaclass=ABCMeta):
    """
        Collection of migrations.
    """

    @abstractmethod
    def migrations(self):
        """
            Get migrations. Subclasses should defile a list of storage migrations here
        """
        raise NotImplementedError()

    @abstractmethod
    def save_applied_number(self, number: int):
        """
            Save the last applied up migration number
        """
        raise NotImplementedError()

    @abstractmethod
    def last_applied(self):
        """
            Number of the last migration that was applied up
        """
        raise NotImplementedError()

    def _get_migrations(self, number: int = None, reverse: bool = False):
        """
            Get all sorted migrations or a migration by number
        """
        if number is None:
            return sorted(self.migrations(), key=lambda x: x.order, reverse=reverse)
        return [m for m in self.migrations() if m.order == number]

    def up(self, number: int = None):
        """
            Runs migrations up. If number was specified, runs particular migration from the set
        """
        for m in self._get_migrations(number, reverse=False):
            if m.order > self.last_applied():
                log.info('Running migration #%i up', m.order)
                m.up()
                self.save_applied_number(m.order)
                log.info('Completed migration #%i up. Last applied is now %i', m.order, m.order)

    def down(self, number: int = None):
        """
            Runs migrations down. If number was specified, runs particular migration from the set
        """
        for m in self._get_migrations(number, reverse=True):
            if m.order <= self.last_applied():
                log.info('Running migration #%i down', m.order)
                m.down()
                last_applied = m.order - 1
                self.save_applied_number(last_applied)
                log.info('Completed migration #%i down. Last applied is now %i', m.order, last_applied)


class Migrator:
    """
        Migrations executor. Just pass a desired set of migrations to it and run up/down.
        If number was specified, runs particular migration
    """

    def __init__(self, migration_set: MigrationSet):
        self.migration_set = migration_set

    def up(self, number: int = None):
        """
            Runs up of a MigrationSet
        """
        self.migration_set.up(number)

    def down(self, number: int = None):
        """
            Runs down of a MigrationSet
        """
        self.migration_set.down(number)
