# -*- coding: utf-8 -*-
"""
Created on Mon Dec  2 11:02:48 2019

@author: Mazurka
"""

from sqlalchemy import create_engine
from sqlalchemy import Table, Column, Integer, String, MetaData
engine = create_engine('sqlite:///DaK2.db', echo = False)
meta = MetaData()

Hraci = Table(
   'Hraci', meta, 
   Column('id', Integer, primary_key = True), 
   Column('name', String,nullable=False), 
   Column('race', String),
   Column('hp', Integer),
   Column('damage', Integer))

Npc = Table(
   'Npc', meta, 
   Column('id', Integer, primary_key = True), 
   Column('name', String,nullable=False), 
   Column('hp', Integer),
   Column('damage', Integer))

Itemy = Table(
   'Itemy', meta, 
   Column('id', Integer, primary_key = True), 
   Column('name',String),
   Column('typ', String,nullable=False),
   Column('slot', String,nullable=False),
   Column('trida', String,nullable=False),
   Column('hp', Integer),
   Column('damage', Integer))

Hraci_Itemy_spojovaci= Table(
   'Hraci_Itemy_spojovaci', meta, 
   Column('id', Integer, primary_key = True), 
   Column('hracid', Integer,nullable=False),
   Column('itemid', Integer,nullable=False))


if __name__ == '__main__':
    meta.create_all(engine)
    conn = engine.connect()
    
    print("tohle bys neměl vidět")


