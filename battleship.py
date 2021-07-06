import numpy as np
import random as rand
import re
#initialize the variable, organize by player data where 1st row is AI follow with player1 data
boards=[np.full((8,8),"0",dtype=str),np.full((8,8),"0",dtype=str)]
ships=[[],[]]
pinboards=[[],[]]
hitlocs=[rand.sample(range(0,63),63),[]]
directions={'U':[-8,0,63], 'D':[8,0,63], 'L':[-1,1,8], 'R':[1,1,8]}
ai=0
me=1
finish=False
i=0
#define ship class
class Ship:
    def __init__(self, size, direction, locations):
        self.size =size
        self.direction=direction
        self.locations=locations
#this function convert rowcol location to location number and vise versa depending on the input
def convert_loc(loc): 
    if isinstance(loc, str): return (int(loc[0])-1)*8+int(loc[1])-1
    else: return str(int(loc/8)+1)+str(int(loc%8)+1)
#this function check the rowcol input to ensure that it meet the rowcoll [1-8][1-8] format
def valid_locinput(loc):
    rex = re.compile("[1-8][1-8]")
    return len(loc)<=2 and rex.match(loc)!=None
#this function check the location is available for ship placement
def valid_loc(ship, loc, prompt, player): #player=0 is AI
    validloc=valid_locinput(loc)
    if validloc:
        locs = []
        locnum=convert_loc(loc)
        direction=directions[ship.direction] #get direction data base on ship.direction
        if ship.direction in ['U','D']:
            locboundary=locnum+ship.size*direction[0] #calculate boundary for up and down
        else:
            locboundary=locnum%8+ship.size*direction[0] #calculate boundary for left and right
        validloc=locboundary>=direction[1] and locboundary<=direction[2] #ensure location is whithin board boundary
        if validloc: #ensure location entered is available 
            for i in range(ship.size): #generate ship locations
                loc=locnum+direction[0]*i 
                if loc in pinboards[player]: validloc=False #check against pinboard, if the lot is not available, set the location as not valid
                else: locs.append(loc)  #if lot is available, add the location to the ship location list
        if validloc:
            ship.locations=locs #add the locations to ship
            pinboards[player]=pinboards[player]+locs #add the locations to player pinboard
        elif prompt:
            print ("ship cannot fit on the board, try another location!")
    return validloc
#this function create a ship with valid location that can be drop on to the board
def auto_generateship(size, type=None):
    validloc=False
    while not validloc:
        randdir=rand.choice(['U','D','L','R'])
        randloc=rand.randint(0, 63)
        shiploc = convert_loc(randloc)
        ship=Ship(size,randdir,[])
        validloc=valid_loc(ship, shiploc, False, type)
    return ship

#game preparation
autogenerate = input("do you want to generate the map automatically (Y/N) ? ").upper()
while autogenerate not in ['Y','N']:
        print('invalid input, please try again')
        input("do you want to generate the map automatically (Y/N) ? ").upper()
#create ship
for i in range(6, 1, -1):
    size=3 if i==6 else i
    if autogenerate in ['N','n']: #user to manually assign ship location
        direction = input("please enter 1x" + str(size) + " ship direction (U,D,L,R) : ").upper()
        while direction not in ['U','D','L','R']:
            print('invalid input, please try again')
            direction = input("please re-enter 1x" + str(size) + " ship direction (U,D,L,R) : ").upper()
        myship=Ship(size,direction,[])
        location = input("please enter 1x" + str(size) + " ship location : ")
        while not valid_loc(myship, location, True, 1):
            print('invalid input, please try again. input format in [1-8][1-8] e.g 11 (row=1,col=1)')
            location = input("please re-enter 1x" + str(size) + " ship location : ")
    else:
        myship=auto_generateship(size,1) #autogenerate player1 ships
    ships[me].append(myship) 
    aiship=auto_generateship(size,0) #autogenerate ai ships
    ships[ai].append(aiship)
for ship in ships[me]: #add player1 ships location to the board for display
    for location in ship.locations:
        boards[me][int(location/8),int(location%8)]=ship.size
#game start
i=0
player=ai #default to ai, will be changed to player1 first time 
while not finish:
    hit=True
    player=me if player==ai else ai #change player turn
    opponent=ai if player==me else me
    while hit and not finish: #player turn stay if the player continue to hit the enemy ship
        print("opponent board: \n",re.sub('[\[\]\']', '', np.array_str(boards[opponent])))
        if player==me:
            while True: #capture hit location
                hitloc = input("Your turn - please enter enemy ship coordinate to hit : ")
                pasthit=hitloc in hitlocs[player]
                if valid_locinput(hitloc) and not pasthit: break
                else:
                    if pasthit: print ("you have hit this locaton before. please try again") 
                    else: print('invalid input, please try again. input format in [1-8][1-8] e.g 11 (row=1,col=1)')
            hitnum=convert_loc(hitloc) 
            hitlocs[player].append(hitloc) #add hit location to pasthit list
        else:
            hitnum=hitlocs[ai][i]
            hitloc=convert_loc(hitnum)
            i=i+1
            print("Enemy turn - enemy is hitting coordinate : " + hitloc)
        if hitnum in pinboards[opponent]: #ship was hit, update the board and remove the lot
            boards[opponent][int(hitloc[0])-1,int(hitloc[1])-1]="X"
            if player==ai: pinboards[opponent].remove(hitnum) 
            print ("ship was hit!")
            if len(pinboards[opponent])==0: #no more hitlist, game concluded!
                hit=False
                finish=True
                if player==ai: print("You LOST!!! Try again!")
                else: print("You WIN!!! Congratulation!")
        else:
            boards[opponent][int(hitloc[0])-1,int(hitloc[1])-1]="-" #nothing was hit
            print ("missed!")
            hit=False
#game end


    
    




