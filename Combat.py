# -*- coding: utf-8 -*-
"""
Created on Thu Dec  5 13:01:41 2019

@author: Mazurka
"""

from Players import Player
import random as rn

P1=Player(1)
P2=Player(2)
P3=Player(3)
P4=Player(4)


def Combat_round(Attacker,Defender):
    print("Hráč",Attacker.getname(),"útočí na hráče",Defender.getname())
    A_damage=Attacker.getdamage()
    D_hp=Defender.gethp()
    D_hp-=A_damage
    print("Hráči",Defender.getname(),"zbývá",D_hp,"životů")
    return D_hp


def Combat(LeftSideList,RightSideList):
    L=LeftSideList
    R=RightSideList
    try:
        if isinstance(L,list):
            pass
        else:
            L=[L]
        if isinstance(R,list):
            pass
        else:
            R=[R]
    except:
        print("Na vstupu musí být List a nebo objekt na něj konvertovatelný(string, integer atd...")
        return
#    boj na náhodný cíl
#        pocet kol
    for n in range(4):
#        v kazdem kole kazdy utoci jednou na nahodny cil
        for l in range(len(L)):
            randomindex=rn.randint(0, len(R)-1)
            R[randomindex].sethp(Combat_round(L[l],R[randomindex]))
        for r in range(len(R)):
            randomindex=rn.randint(0, len(L)-1)
            L[randomindex].sethp(Combat_round(R[r],L[randomindex]))
    
    return

Combat(P1,[P2,P3,P4])





