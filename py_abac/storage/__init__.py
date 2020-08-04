"""
    Exposed classes and methods
"""

import logging

logger = logging.getLogger(__name__)

try:
    from .mongo import MongoStorage, MongoMigrationSet
    logger.info('mongo storage imported')  
except ImportError:
    # failure to import may mean that only sql extras are installed
    pass

try:
    from .sql import SQLStorage, SQLMigrationSet
    logger.info('sql storage imported')  
except ImportError:
    # failure to import may mean that only mongo extras are installed
    pass