# -*- coding: utf-8 -*-
"""
Created on Mon Dec  2 13:24:24 2019

@author: Mazurka
"""


from sqlalchemy import create_engine
engine = create_engine('sqlite:///DaK2.db', echo = False)
conn = engine.connect()

from Tables import Itemy
from Tables import Hraci_Itemy_spojovaci
    
#typ,slot a trida jsou predefinované stringy
def Item_add_DB(name="Unidentified",typ="",slot="",trida="",hp=0,damage=0):
    prikaz = Itemy.insert().values(name=name,typ=typ,slot=slot,trida=trida,hp=hp,damage=damage)
    conn.execute(prikaz)
    return

def Item_delete_DB(my_id):
    if my_id=="all":
        conn.execute(Itemy.delete())
    elif (type(my_id)==int):
        conn.execute(Itemy.delete().where(Itemy.c.id == my_id))
    else:
        print("Zadej cislo nebo all")
    return

def Item_addto_Player(hracid,itemid):
#    tady by to chtělo nějaký check jestli daný hráč existuje
    conn.execute(Hraci_Itemy_spojovaci.insert().values(hracid=hracid,itemid=itemid))
    return

def Item_removefrom_Player(hracid,itemid,pocetkesmazani=1):
#    udělane takto jinak by automaticky mazalo vsechny souhlasne zaznamy
    if pocetkesmazani=="all":
        conn.execute(Hraci_Itemy_spojovaci.delete().where(Hraci_Itemy_spojovaci.c.hracid==hracid).where(Hraci_Itemy_spojovaci.c.itemid==itemid))
    else:    
        pocet=conn.execute(Hraci_Itemy_spojovaci.select(Hraci_Itemy_spojovaci).where(Hraci_Itemy_spojovaci.c.hracid==hracid).where(Hraci_Itemy_spojovaci.c.itemid==itemid)).fetchall()
        IDs=[]
        for i in range(len(pocet)):
            IDs.append(pocet[i][0])
        if len(IDs)<pocetkesmazani:
            pocetkesmazani=len(IDs)
        for i in range(pocetkesmazani):
            currentid=IDs[-(i+1)]
            conn.execute(Hraci_Itemy_spojovaci.delete().where(Hraci_Itemy_spojovaci.c.id==currentid))   
    return

#Item_add_DB()
#Item_add_DB(name="meč",damage=10)
#Item_add_DB(name="zbroj",hp=300)
#Item_delete_DB(7)
#show=conn.execute("select Itemy.id, Itemy.name from Itemy").fetchall()
#print(show)

#Item_addto_Player(3,4)
#show=conn.execute("select Hraci_Itemy_spojovaci.id,Hraci_Itemy_spojovaci.hracid,Hraci_Itemy_spojovaci.itemid from Hraci_Itemy_spojovaci").fetchall()
#print(show)

#Item_removefrom_Player(1,4)
#show=conn.execute("select Hraci_Itemy_spojovaci.id,Hraci_Itemy_spojovaci.hracid,Hraci_Itemy_spojovaci.itemid from Hraci_Itemy_spojovaci").fetchall()
#print(show)


