from sqlalchemy import Column, BigInteger, String, sql

from tgbot.services.db_api.db_gino import BaseModel


class User(BaseModel):
    __tablename__ = "users"

    id = Column(BigInteger, primary_key=True)
    name = Column(String(50))

    authenticated = Column(String(10), default="False")  # str: True/False
    auth_data = Column(String(3000), default="None")

    query: sql.Select
