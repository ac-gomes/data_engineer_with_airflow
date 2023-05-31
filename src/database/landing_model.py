from sqlalchemy.orm import declarative_base
from sqlalchemy import (
    Column,
    String,
    DateTime,
    BigInteger,
    Integer,
    Double
)

LandingBase = declarative_base()


class Players(LandingBase):
    __tablename__ = "players"
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    clientes_id = Column(BigInteger, index=True)
    datahora_acesso = Column(DateTime, index=True)
    modalidade = Column(String(50), index=True)
    rake = Column(Double, index=True)


class ConsolidatedPlayers(LandingBase):
    __tablename__ = "consolidatedplayers"
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    mes = Column(Integer, index=True)
    rake = Column(Double, index=True)
    jogadores = Column(BigInteger, index=True)
    rake_cash_game = Column(Double, index=True)
    rake_torneio = Column(Double, index=True)
    jogadores_cash_game = Column(BigInteger, index=True)
    jogadores_torneio = Column(BigInteger, index=True)
