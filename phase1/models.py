from sqlalchemy import (Column, BigInteger, Integer, String,)
from database import Base


class Transaction(Base):
    __tablename__ = 'transactions'

    id = Column(Integer, primary_key=True)
    custid = Column(Integer)
    type = Column(String(10), nullable=False)
    date = Column(Integer)
    amt = Column(Integer)


class Balance(Base):
    __tablename__ = 'balances'

    id = Column(Integer, primary_key=True)
    custid = Column(Integer, unique=True)
    balance = Column(Integer)
