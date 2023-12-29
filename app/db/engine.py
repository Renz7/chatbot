#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""

Time    : 2023/12/29 17:09
Author  : ren
"""
from sqlalchemy import create_engine, Column, BIGINT, VARCHAR
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

import config

engine = create_engine(config.DB_URL)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
Base = declarative_base()


def get_db_dep():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# model
class User(Base):
    id = Column("id", BIGINT, comment="id")
    name = Column("id", VARCHAR(64), comment="id")
    password = Column("id", VARCHAR(256), comment="id")


if __name__ == '__main__':
    import click


    @click.command()
    def initdb():
        Base.metadata.create_all(bind=engine)


    initdb()
