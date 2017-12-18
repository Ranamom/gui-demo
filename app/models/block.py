# -*- coding: utf-8 -*-
import logging
from binascii import unhexlify

from sqlalchemy import LargeBinary, Column, DateTime, Integer, exists

from app.models.db import data_db, data_base

log = logging.getLogger(__name__)


class Block(data_base):

    __tablename__ = "blocks"
    """Blocks"""

    hash = Column(LargeBinary, primary_key=True)
    time = Column(DateTime)
    height = Column(Integer)

    class Meta:
        database = data_db

    def __repr__(self):
        return "Block(h=%s, t=%s, txs=%s)" % (self.height, self.time, self.txcount)

    @classmethod
    def multi_tx_blocks(cls): # todo: wahrscheinlich ab jetzt unnötig, mal gucken
        # return cls.select().where(cls.txcount > 1)
        pass

    @staticmethod
    def block_exists(data_db, block_hash):
        return data_db.query(exists().where(Block.hash == unhexlify(block_hash))).scalar()

