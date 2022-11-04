from enum import Enum
from sqlalchemy import BigInteger, Column, MetaData, Table
from sqlalchemy.dialects.postgresql import ENUM


class type_data(str, Enum):
    OPEN = "OPEN"
    CLOSED = "CLOSED"
