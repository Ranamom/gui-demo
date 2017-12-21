# -*- coding: utf-8 -*-
"""Enum constants"""
import enum
from enum import Enum


class Method(Enum):
    """An rpc api method where:

    .name is the string name of the method
    .autosync tells us if we should autosync that method

    Enum value tuple semantics
    (index, autosync, )
    """
    getblockchaininfo = (1, True,)
    getinfo = (2, True,)
    getruntimeparams = (3, True,)

    @property
    def autosync(self):
        """Wether this method should be autosynced"""
        return self.value[1]


class Stream(Enum):
    """A build in multichain stream where:

    .name is the string name of the stream
    .open tells us if the stream is open
    """

    alias = (1, True,)

    @property
    def open(self):
        """Wether this stream is openly writable"""
        return self.value[1]


ISSUE, CREATE, MINE, ADMIN = 'issue', 'create', 'mine', 'admin'
class PermTypes(enum.Enum):
    issue = 0
    create = 1
    mine = 2
    admin = 3
