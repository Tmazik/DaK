# -*- coding: utf-8 -*-
"""
Created on Tue Dec  3 10:14:05 2019

@author: Mazurka
"""

from sqlalchemy import create_engine
engine = create_engine('sqlite:///DaK2.db', echo = False)
conn = engine.connect()


from Tables import Hraci
from Tables import Hraci_Itemy_spojovaci
from Tables import Itemy


def Player_add_DB(name,race="Unidentified",hp=0,damage=0):
     name=name.rstrip()
     name=name.lstrip()
     name=name.lower()
     name=name[0].upper()+name[1:]
     race=race.rstrip()
     race=race.lstrip()
     race=race.lower()
     race=race[0].upper()+race[1:]
     pridej = Hraci.insert().values(name=name,race=race,hp=hp,damage=damage)
     hraci=conn.execute("select Hraci.id, Hraci.name from Hraci").fetchall()
     obsahuje=False
     for i in range(len(hraci)):
         if name.lower()==hraci[i][1].lower():
             obsahuje=True
     if obsahuje:
         print("Daného hráče nelze přidat, neboť daný hráč v databázi již existuje")
     else:
         conn.execute(pridej)
     return 
 
def Player_delete_DB(playerid=None,name=None):
    if type(playerid)==int:
        conn.execute(Hraci.delete().where(Hraci.c.id == playerid))
    elif playerid is None and type(name)==str:
        conn.execute(Hraci.delete().where(Hraci.c.name == name))
    else:
        print("Špatné argumenty, zadejte playerid NEBO name")
    return

def Player_Itemlist(playerid=None,name=None):
    itemlist=[]
    if type(playerid)==int:
        items=conn.execute(Hraci_Itemy_spojovaci.select().where(Hraci_Itemy_spojovaci.c.hracid == playerid)).fetchall()
#        name tu nemusí být, je to pro print
        name=conn.execute(Hraci.select().where(Hraci.c.id == playerid)).fetchall()[0][1]
    elif playerid is None and type(name)==str:
        playerid=conn.execute(Hraci.select().where(Hraci.c.name == name)).fetchall()[0][0]
        items=conn.execute(Hraci_Itemy_spojovaci.select().where(Hraci_Itemy_spojovaci.c.hracid == playerid)).fetchall()       
    else:
        print("Špatné argumenty, zadejte playerid NEBO name")
    print("Hráč",name,"má u sebe následující itemy:")
    for i in range(len(items)):
        item=conn.execute(Itemy.select().where(Itemy.c.id==items[i][2])).fetchall()[0][1:]
        print(item)
        itemlist.append(item)
    return itemlist


#Player_add_DB(name="dan",race=" hive",hp=80,damage=10)
#show=conn.execute(Hraci.select()).fetchall()
#print(show)

#Player_delete_DB(name="Mira")
#show=conn.execute(Hraci.select()).fetchall()
#print(show)
    
#Tmazitems=Player_Itemlist(name="Tmaz")
#Player_Itemlist(2)
    
class Player:
    def __init__(self,myid):
        self.__myid=myid
#        Popremyslet jestli nevytvorit neco jako saveable statistic list
        self.__name=conn.execute("select Hraci.name from Hraci where Hraci.id =:x", x = myid).fetchone()[0]
        self.__race=conn.execute("select Hraci.race from Hraci where Hraci.id =:x", x = myid).fetchone()[0]
        self.__hp=conn.execute("select Hraci.hp from Hraci where Hraci.id =:x", x = myid).fetchone()[0]
        self.__damage=conn.execute("select Hraci.damage from Hraci where Hraci.id =:x", x = myid).fetchone()[0]
#        itemy zatim nasadi automaticky vsechny a secte se staty, pak bude muset byt rozdeleni na basedmg,itemdmg,a totaldmg+sltoy na itemech atd
        bonushp,bonusdamage=self.equipitems(myid)
        self.sethp(self.gethp()+bonushp)
        self.setdamage(self.getdamage()+bonusdamage)
    def getmyid(self):
        return self.__myid
    def getname(self):
        return self.__name
    def setname(self,name):
        if isinstance(name, str):
            name=name.rstrip()
            name=name.lstrip()
            name=name.lower()
            name=name[0].upper()+name[1:]
            self.__name=name
        else:
            print("Zadejte String")
    def getrace(self):
        return self.__race
    def setrace(self,race):
        if isinstance(race, str):
            race=race.rstrip()
            race=race.lstrip()
            race=race.lower()
            if race==("human" or "scorchlander" or "shek" or "hive" or "skeleton"):
                race=race[0].upper()+race[1:]
                self.__race=race
            else:
                print("Zadali jste nesprávnou rasu, zadejte:")
                print("human,scorchlander,shek,hive,skeleton")
        else:
            print("Zadejte String")
    def gethp(self):
        return self.__hp
    def sethp(self,hp):
        if isinstance(hp, int):
            if hp<0:
                hp=0
            self.__hp=hp
        else:
            print("Zadejte Integer")
    def getdamage(self):
        return self.__damage
    def setdamage(self,damage):
        if isinstance(damage, int):
            self.__damage=damage
        else:
            print("Zadejte Integer")
    
    def equipitems(self,myid):
        items=[]
        show=conn.execute(Hraci_Itemy_spojovaci.select().where(Hraci_Itemy_spojovaci.c.hracid==myid)).fetchall()
        for i in range(len(show)):
            items.append(show[i][2])
        bonushp=0
        bonusdamage=0
        for i in range(len(items)):
            itemhp=conn.execute(Itemy.select().where(Itemy.c.id==items[i])).fetchone()[5]
            itemdamage=conn.execute(Itemy.select().where(Itemy.c.id==items[i])).fetchone()[6]
            bonushp+=itemhp
            bonusdamage+=itemdamage
        return bonushp,bonusdamage
            
            
def Player_save_DB(player):
    if isinstance(player,Player):
        staty=[]
        for stat in vars(player).keys():
            stat="get"+stat[9:]
            staty.append(stat)
        print(staty)
        for i in range(1,len(staty)):
            hodnota=(eval(("player."+staty[i]+"()")))
            if isinstance(hodnota,str):
                hodnota="\""+hodnota+"\""
            stat=(staty[i][3:])
            text="conn.execute(Hraci.update().where(Hraci.c.id == 1).values("+stat+"= "+str(hodnota)+"))"
            print("ukládám "+stat)
            eval(text) 
    else:
        print("Zadaný argument není objekt hráč")
    return
        
#Tom=Player(1)
#print(Tom.getname())
#Tom.setname("Tmaz")
#print(Tom.getdamage())
#Tom.setdamage(25)
#Player_save_DB(Tom)
#Tom2=Player(1)
#print(Tom2.getname())
#print(Tom2.getdamage())


