import logging

from mongo_adapter import MongoAdapter
from pymongo.collection import Collection
from pymongo.database import Database

LOG = logging.getLogger(__name__)


class ArnoldAdapter(MongoAdapter):
    def setup(self, db_name: str):
        """Setup connection to a database"""

        if self.client is None:
            raise SyntaxError("No client is available")
        self.db: Database = self.client[db_name]
        self.db_name: str = db_name
        self.sample_collection: Collection = self.db.sample
        self.prep_collection: Collection = self.db.prep

        LOG.info("Use database %s.", db_name)
