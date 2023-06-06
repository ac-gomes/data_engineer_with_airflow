from sqlalchemy.orm import declarative_base
from sqlalchemy import (
    Column,
    String,
    DateTime,
    BigInteger,
    Double
)

SourceBase = declarative_base()


class Players(SourceBase):
    __tablename__ = "players"
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    clientes_id = Column(BigInteger, index=True)
    datahora_acesso = Column(DateTime, index=True)
    modalidade = Column(String(50), index=True)
    rake = Column(Double, index=True)
