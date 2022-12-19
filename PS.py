#DECLARE FUNCTIONS

def getdata(stat):
    return list(testchart[stat])

#gets columns from updatedpokemon spreadsheet, converts them into their own lists


def accuracy_check(move_accuracy):
    if move_accuracy < random.randint(1,100):
        return "miss"
    else:
        return "hit"
    
#only called when a move does not have 100% accuracy, determines if a move will hit or miss based on its actual accuracy


def damage_calc(bp, p_atk, p_def, m_type, p_type1,p_type2,multiplier):
    if (m_type == p_type1 or m_type == p_type2): 
        STAB = 1.5
    else:
        STAB = 1.0
    roll = round(random.uniform(.85, 1.00), 2) #removes decimals from float
    crit = 1
    crit_chance = (random.randint(1,24)) #critical hits have a 1/24 chance of occuring
    if (crit_chance == 1 and multiplier != 0):
        print("A critical hit!")
        sleep(.5)
        crit = 1.5 #critical hits deal 50% extra damage
    damage = (((42.0 * float(bp) * (p_atk/p_def))/50.0)+2.0) * roll * STAB * crit
    
    return damage

#main damage calculator for pokemon battles, takes into account damage roll and STAB


def getmove_data(stat):
    return list(moveschart[stat])

#does the same as getdata function, except for the moves spreadsheet


def switch(team,mon,player):
    print(f"Player {player}'s team: {', '.join(f'{key} ({round((value[0]/value[1])*100,1)}%)' for key, value in team.items())}\n")
    sleep(.5)
    while True:
        try:
            next_mon=int(input(f"Player {player}: Pick 1-{len(team)} to choose your pokemon to switch in: "))
            if list(team)[next_mon-1] == mon:
                print(f'{mon} is being switched out!')
                raise ValueError
            if (next_mon < 1 or next_mon > len(team)):
                raise ValueError
            break
        except ValueError:
            print('Pick a valid choice')
        except IndexError:
            print('Pick a valid choice')            
    print(f'\nPlayer {player} sends out {list(team)[next_mon-1]}!')
    sleep(.5)
    return next_mon-1



def raw_stat(stat):
    raw_stat=[]
    for i in stat:
        raw_stat.append((2*i)+5)
    return raw_stat

#converts base stats into usable raw in-game stats


def move_order(mon1,mon2): 
    if spe[name.index(mon1)] > spe[name.index(mon2)]:
        return 1
    elif spe[name.index(mon1)] < spe[name.index(mon2)]:
        return 2
    else: 
        return "tie"
''' 
every turn, checks to see which mon has a higher speed stat. The mon with the higher speed stat goes first
if their speed stats are identical (tie), then who goes first is determined by a 50/50 coin flip
'''

def switch_in(team,player):
    print(f"Player {player}'s team: {', '.join(f'{key} ({round((value[0]/value[1])*100,1)}%)' for key, value in team.items())}\n")
    sleep(.5)
    while True:
        try:
            next_mon=int(input(f"Player {player}: Pick 1-{len(team)} to choose your pokemon to switch in: "))
            if (next_mon < 1 or next_mon > (len(team))):
                raise ValueError
            break
        except ValueError:
            print('Pick a valid choice')
    print(f'\nPlayer {player} sent out {list(team)[next_mon-1]}!')
    sleep(.5)
    return next_mon-1
'''
switch_in is called when a mon is KO'd, and the player whose mon was KO'd is prompted to pick a new one from their team
the function will only accept a valid number for the team
'''

def main_loop(team1,mon1,team2,mon2,counter,ko_check):
    if ko_check == False:
        if (len(team1)==0 or len(team2)==0):
            return None
        else:
            turn(team1,mon1,team2,mon2,counter)
    else:
        if (team1[mon1][0]==0):
            del team1[mon1] #deletes the pokemon from the team if the HP is zero
            if len(team1)==0:
                sleep(.5)
                print(f'\nPlayer 1 has no remaining pokemon!\n\nPlayer 2 is the winner!')
                return None
            else:
                turn(team1,list(team1)[switch_in(team1,1)],team2,mon2,counter)
        elif (team2[mon2][0]==0):
            del team2[mon2] #deletes the pokemon from the team if the HP is zero
            if len(team2)==0:
                sleep(.5)
                print(f'\nPlayer 2 has no remaining pokemon!\n\nPlayer 1 is the winner!')
                return None
            else:
                turn(team1,mon1,team2,list(team2)[switch_in(team2,2)],counter)
'''
#main_loop is called at the end of every turn. It is passed all the updated team data, and if a pokemon was KO'd
if a mon isn't KO'd, nothing changes, and the next turn is started
if a mon is KO'd, the player whose mon fainted is prompted to switch in a new one, through the switch_in function
switch_in function returns the index of the dictionary for the pokemon the player picks
because of this, the square bracket will have the index of that pokemon, for example,
list(team2)[1] will be the second entry in the dictionary of player 2's team
this is entered as one of the arguments in the turn call, acting as player 2's current mon
'''

def move_used(p1_name, m_name, m_type, m_category, m_bp, m_accuracy, p2_name, defender_hp, full_hp):
    print(f'\n{p1_name} used {m_name}!')
    sleep(.5)
    if accuracy_check(m_accuracy) == "miss":
        print(f'The opposing {p2_name} avoided the attack!') 
        sleep(.5)
        return defender_hp #if the attack misses, function ends, defender loses no HP
    attacker_move_index=pokemon_types.index(m_type)
    defender_type1=pokemon_types.index(type1[name.index(p2_name)])
    if m_category != "Status":
        if (pd.isna(type2[name.index(p2_name)])==True): #checks if defending pokemon is a single type, TRUE means it's a single type
            damage_multiplier=(damage_array[attacker_move_index][defender_type1]) 
        if (pd.isna(type2[name.index(p2_name)])==False): #checks if defending pokemon is a single type
            defender_type2=pokemon_types.index(type2[name.index(p2_name)])
            damage_multiplier=(damage_array[attacker_move_index][defender_type1]*damage_array[attacker_move_index][defender_type2])
        if m_category == "Physical": #calls damage calc using physical attack and defense
            dmg_done=math.trunc(damage_calc(m_bp,attack[name.index(p1_name)],defense[name.index(p2_name)], m_type, type1[name.index(p1_name)],type2[name.index(p1_name)],damage_multiplier)*damage_multiplier)
        elif m_category == "Special": #calls damage calc using special attack and special defense
            dmg_done=math.trunc(damage_calc(m_bp,SpA[name.index(p1_name)],SpD[name.index(p2_name)], m_type, type1[name.index(p1_name)],type2[name.index(p1_name)],damage_multiplier)*damage_multiplier)
        percent_lost=round((dmg_done)/(full_hp) * 100,1)
        if(damage_multiplier==2 or damage_multiplier==4):
            print("It's super effective!")
        elif(damage_multiplier==.5 or damage_multiplier==.25):
            print("It's not very effective...")
        elif(damage_multiplier==0):
            print(f"It doesn't affect {p2_name}...")
            return defender_hp #no damage is done
        if percent_lost > 100.0:
            percent_lost=100.0
        if(dmg_done >= defender_hp):
            percent_lost=round((defender_hp)/(full_hp) * 100,1) #if the attack KO's, only % lost is what remains at the time of the attack, e.g. attack that does 70% against a mon with 10% HP remaining, displays as 10% 
        sleep(.5)
        print(f"{p2_name} lost {percent_lost}% of its health!")
        sleep(.5)
        if(dmg_done >= defender_hp):
            percent_lost=round((defender_hp)/(full_hp) * 100,1)
            print(f'{p2_name} fainted!\n')
            sleep(.5)
            defender_hp=0
            return 0
        else:
            return (defender_hp-dmg_done)
    else:
        print("This is a status move! Status moves are not implemented yet.")
        return defender_hp
    
    
def turn(team_1,mon_1,team_2,mon_2,turn_count):
    p1_switched = False
    p2_switched = False
    KO = False
    turn_count+=1
    print(f'\n================================================================================\nTURN {turn_count}\n')
    sleep(.5)
    p1_moveset=team_1[mon_1][2]
    p1_hp=team_1[mon_1][0]
    P1_FULL_HP=team_1[mon_1][1]
    p2_moveset=team_2[mon_2][2]
    p2_hp=team_2[mon_2][0]
    P2_FULL_HP=team_2[mon_2][1]
    print(f"{mon_1}'s moves: {p1_moveset}") 
    print(f"{mon_1}'s current HP: {round((p1_hp/P1_FULL_HP)*100,1)}%\n")
    sleep(.5)
    print(f"{mon_2}'s moves: {p2_moveset}") 
    print(f"{mon_2}'s current HP: {round((p2_hp/P2_FULL_HP)*100,1)}%\n")
    faster=move_order(mon_1,mon_2)
    #PICK MOVE, player 1
    while True:
        if len(team_1) > 1:
            try:
                p1_move_chosen=int(input("Player 1: Enter 1,2,3, or 4 to pick a move, or enter 5 to switch: "))
                if (p1_move_chosen < 1 or p1_move_chosen > 5):
                    raise ValueError
                break
            except ValueError:
                print('Pick a valid choice')
        else:
            try:
                p1_move_chosen=int(input("Player 1: Enter 1,2,3, or 4 to pick a move: "))
                if (p1_move_chosen < 1 or p1_move_chosen > 4):
                    raise ValueError
                break
            except ValueError:
                print('Pick a valid choice')
    #PICK MOVE, player 2
    while True:
        if len(team_2) > 1:
            try:
                p2_move_chosen=int(input("Player 2: Enter 1,2,3, or 4 to pick a move, or enter 5 to switch: "))
                if (p2_move_chosen < 1 or p2_move_chosen > 5):
                    raise ValueError
                break
            except ValueError:
                print('Pick a valid choice')
        else:
            try:
                p2_move_chosen=int(input("Player 2: Enter 1,2,3, or 4 to pick a move: "))
                if (p2_move_chosen < 1 or p2_move_chosen > 4):
                    raise ValueError
                break
            except ValueError:
                print('Pick a valid choice')
            
    if p1_move_chosen == 5:
        p1_switched = True
        print(f'Player 1 switches out {mon_1}!\n')
        sleep(.5)
        mon_1=list(team_1)[switch(team_1,mon_1,1)]
        p1_moveset=team_1[mon_1][2]
        p1_hp=team_1[mon_1][0]
        P1_FULL_HP=team_1[mon_1][1]
    
    if p2_move_chosen == 5:
        p2_switched = True
        print(f'Player 2 switches out {mon_2}!\n')
        sleep(.5)
        mon_2=list(team_2)[switch(team_2,mon_2,2)]
        p2_moveset=team_2[mon_2][2]
        p2_hp=team_2[mon_2][0]
        P2_FULL_HP=team_2[mon_2][1]
    
    if faster == "tie":
        if random.random() >= .5:
            faster=1
        else:
            faster=2
    p1_move_chosen-=1
    p2_move_chosen-=1 #lines up user choice with index of data (user with moves 1-4 is indexes 0-3, done for easier user interaction)
    if (p1_move_chosen == 4 and p2_move_chosen ==4): #double switch
        main_loop(team_1,mon_1,team_2,mon_2,turn_count,KO)
    else:
        if faster == 1:
            if p1_switched == False: #mon1 goes first, checks to see if KO'd mon2, if it didn't, display mon2's HP. mon2 goes next, checks to see if KO'd mon1, if it didn't, display mon1's HP
                remaining_hp_p2=move_used(mon_1,p1_moveset[p1_move_chosen],move_data[p1_moveset[p1_move_chosen]][0],move_data[p1_moveset[p1_move_chosen]][1],move_data[p1_moveset[p1_move_chosen]][2],move_data[p1_moveset[p1_move_chosen]][3],mon_2,p2_hp,P2_FULL_HP)
                if remaining_hp_p2==0: 
                    #if mon1 KO's mon2, mon2 does not attack
                    KO = True #OUTCOME 2
                    team_2[mon_2][0]=0
                else: 
                    print(f"{mon_2}'s current HP: {round((remaining_hp_p2/P2_FULL_HP)*100,1)}%") #OUTCOME 1A
                    if p2_switched == False:
                        remaining_hp_p1=move_used(mon_2,p2_moveset[p2_move_chosen],move_data[p2_moveset[p2_move_chosen]][0],move_data[p2_moveset[p2_move_chosen]][1],move_data[p2_moveset[p2_move_chosen]][2],move_data[p2_moveset[p2_move_chosen]][3],mon_1,p1_hp,P1_FULL_HP)
                        #OUTCOME 3A ^
                        if remaining_hp_p1==0:
                            KO = True #OUTCOME 3B
                            team_1[mon_1][0]=0
                            team_2[mon_2][0]=remaining_hp_p2
                        else:
                            print(f"{mon_1}'s current HP: {round((remaining_hp_p1/P1_FULL_HP)*100,1)}%") #OUTCOME 1B
                    else:
                        remaining_hp_p1=p1_hp
            else:
                remaining_hp_p2=p2_hp
                remaining_hp_p1=move_used(mon_2,p2_moveset[p2_move_chosen],move_data[p2_moveset[p2_move_chosen]][0],move_data[p2_moveset[p2_move_chosen]][1],move_data[p2_moveset[p2_move_chosen]][2],move_data[p2_moveset[p2_move_chosen]][3],mon_1,p1_hp,P1_FULL_HP)
                if remaining_hp_p1==0:
                    KO = True
                    team_1[mon_1][0]=0

        if faster == 2:
            if p2_switched == False:
                remaining_hp_p1=move_used(mon_2,p2_moveset[p2_move_chosen],move_data[p2_moveset[p2_move_chosen]][0],move_data[p2_moveset[p2_move_chosen]][1],move_data[p2_moveset[p2_move_chosen]][2],move_data[p2_moveset[p2_move_chosen]][3],mon_1,p1_hp,P1_FULL_HP)
                if remaining_hp_p1==0:
                    KO = True #OUTCOME 5
                    team_1[mon_1][0]=0
                    #if mon2 KO's mon1, mon1 does not attack
                else:
                    print(f"{mon_1}'s current HP: {round((remaining_hp_p1/P1_FULL_HP)*100,1)}%") #OUTCOME 4A
                    if p1_switched == False:
                        remaining_hp_p2=move_used(mon_1,p1_moveset[p1_move_chosen],move_data[p1_moveset[p1_move_chosen]][0],move_data[p1_moveset[p1_move_chosen]][1],move_data[p1_moveset[p1_move_chosen]][2],move_data[p1_moveset[p1_move_chosen]][3],mon_2,p2_hp,P2_FULL_HP)
                        #OUTCOME 6A ^
                        if remaining_hp_p2==0:
                            KO = True #OUTCOME 6B
                            team_2[mon_2][0]=0
                            team_1[mon_1][0]=remaining_hp_p1
                        else:
                            print(f"{mon_2}'s current HP: {round((remaining_hp_p2/P2_FULL_HP)*100,1)}%") #OUTCOME 4B
                    else:
                        remaining_hp_p2=p2_hp
            else:
                remaining_hp_p1=p1_hp
                remaining_hp_p2=move_used(mon_1,p1_moveset[p1_move_chosen],move_data[p1_moveset[p1_move_chosen]][0],move_data[p1_moveset[p1_move_chosen]][1],move_data[p1_moveset[p1_move_chosen]][2],move_data[p1_moveset[p1_move_chosen]][3],mon_2,p2_hp,P2_FULL_HP)
                if remaining_hp_p2==0:
                    KO = True
                    team_2[mon_2][0]=0


        if KO == False:
            team_1[mon_1][0]=remaining_hp_p1
            team_2[mon_2][0]=remaining_hp_p2
    main_loop(team_1,mon_1,team_2,mon_2,turn_count,KO)
'''    
#called every turn of the battle, extracts moveset, dynamic HP, and max HP from the dictionary
#prompts the players to make a choice, will only continue when the player makes a valid choice
#after determining move order, move is used, damage is done, then next mon makes a move if it hasn't fainted
#SIX possible outcomes every turn, listed below

#POSSIBLE OUTCOMES OF A SINGLE TURN (assuming no switching):
     mon1 moves first: 
1a) mon1 (move first) damages mon2, 
1b) then mon2 (move second) damages mon1. TURN ENDS
2) mon1 (move first) KO's mon2. TURN ENDS
3a) mon1 (move first) damages mon2, 
3b) then mon2 (move second) KO's mon1. TURN ENDS

     mon2 moves first
4a) mon2 (move first) damages mon1, 
4b) then mon1 (move second) damages mon2. TURN ENDS
5) mon2 (move first) KO's mon1. TURN ENDS
6a) mon2 (move first) damages mon1, 
6b) then mon1 (move second) KO's mon2. TURN ENDS

Displaying current HP doesn't seem necessary, but in the absence of a GUI, it must be displayed. Also not calling move_used through remaining_hp seems to break things for some reason
'''


###################################################################################################################################################################



#INITIALIZE DATA
import pandas as pd
import numpy as np
import random
import json
import math
from time import sleep

pokemon_types = ["Normal", "Fire", "Water", "Grass", "Electric", "Ice",
                 "Fighting", "Poison", "Ground", "Flying", "Psychic",
                 "Bug", "Rock", "Ghost", "Dragon", "Dark", "Steel", "Fairy"]

damage_array = np.array([[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1/2, 0, 1, 1, 1/2, 1],
                    [1, 1/2, 1/2, 2, 1, 2, 1, 1, 1, 1, 1, 2, 1/2, 1, 1/2, 1, 2, 1],
                    [1, 2, 1/2, 1/2, 1, 1, 1, 1, 2, 1, 1, 1, 2, 1, 1/2, 1, 1, 1],
                    [1, 1/2, 2, 1/2, 1, 1, 1, 1/2, 2, 1/2, 1, 1/2, 2, 1, 1/2, 1, 1/2, 1],
                    [1, 1, 2, 1/2, 1/2, 1, 1, 1, 0, 2, 1, 1, 1, 1, 1/2, 1, 1, 1],
                    [1, 1/2, 1/2, 2, 1, 1/2, 1, 1, 2, 2, 1, 1, 1, 1, 2, 1, 1/2, 1],
                    [2, 1, 1, 1, 1, 2, 1, 1/2, 1, 1/2, 1/2, 1/2, 2, 0, 1, 2, 2, 1/2],
                    [1, 1, 1, 2, 1, 1, 1, 1/2, 1/2, 1, 1, 1, 1/2, 1/2, 1, 1, 0, 2],
                    [1, 2, 1, 1/2, 2, 1, 1, 2, 1, 0, 1, 1/2, 2, 1, 1, 1, 2, 1],
                    [1, 1, 1, 2, 1/2, 1, 2, 1, 1, 1, 1, 2, 1/2, 1, 1, 1, 1/2, 1],
                    [1, 1, 1, 1, 1, 1, 2, 2, 1, 1, 1/2, 1, 1, 1, 1, 0, 1/2, 1],
                    [1, 1/2, 1, 2, 1, 1, 1/2, 1/2, 1, 1/2, 2, 1, 1, 1/2, 1, 2, 1/2, 1/2],
                    [1, 2, 1, 1, 1, 2, 1/2, 1, 1/2, 2, 1, 2, 1, 1, 1, 1, 1/2, 1],
                    [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 2, 1, 1/2, 1, 1],
                    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1/2, 0],
                    [1, 1, 1, 1, 1, 1, 1/2, 1, 1, 1, 2, 1, 1, 2, 1, 1/2, 1, 1/2],
                    [1, 1/2, 1/2, 1, 1/2, 2, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1/2, 2],
                    [1, 1/2, 1, 1, 1, 1, 2, 1/2, 1, 1, 1, 1, 1, 1, 2, 2, 1/2, 1]])

testchart = pd.read_csv('updatedpokemon.csv')
moveschart = pd.read_csv('moves.csv')
name=getdata('Name')
type1=getdata('Type 1')
type2=getdata('Type 2')
bst=getdata('Total')
hp=getdata('HP')
attack=getdata('Attack')
defense=getdata('Defense')
SpA=getdata('Sp. Atk')
SpD=getdata('Sp. Def')
spe=getdata('Speed')
single=getdata('Single Stage')
finalevo=getdata('Final Evolution')
move_name = getmove_data('move')
move_type = getmove_data('type')
move_category = getmove_data('category')
base_power = getmove_data('power')
accuracy = getmove_data('accuracy')
raw_hp=[]
for i in hp:
    raw_hp.append((2*i)+110) #get raw HP number from base HP 
attack=raw_stat(attack)
defense=raw_stat(defense)
SpA=raw_stat(SpA)
SpD=raw_stat(SpD)
spe=raw_stat(spe) #get raw stats from base stats, uses a different formula
raw_accuracy=[]
for i in range(len(accuracy)): 
    if accuracy[i] == "—":
        accuracy[i]="100%" #changes all self-status and guaranteed hit moves to be 100% accurate
for i in range(len(accuracy)):
    raw_accuracy.append(int(accuracy[i].rstrip("%"))) #converts list of strings with accuracy % to list of integers to use for random accuracy calculations
    
viablemons=[]
for i in range(len(name)):
    if single[name.index(name[i])]==True or finalevo[name.index(name[i])]==True:
        viablemons.append(name[i]) #extracts only fully evolved or nonevolving pokemon to a new list

with open('movesets.txt') as file:
    sets = file.read()
    mondata = json.loads(sets) #reads file text as a dictionary, as the sets are already in dictionary/json format
moves=[]
for i in range(len(mondata)):
    moves.append(list(list(mondata.values())[i].values())[3])
names=list(mondata.keys())
pokemon_moves=dict(zip(names,moves))
'''
Extract only pokemon name and moveset from dictionary, 
create a new dictionary with pokemon name as keys, and moveset list as values
'''
#create a new dictionary with move names as keys, and traits list as values
move_traits=list(zip(move_type,move_category,base_power,raw_accuracy))
m_traits_list=[list(element) for element in move_traits] #convert list of tuples to list of lists using comprehension
move_data=dict(zip(move_name,m_traits_list))
'''
#initializes everything, puts data from spreadsheets into lists, converts to raw values
#extracts ONLY mon name and movepool from given dictionaries, the rest is unnecessary
#once all data is formatted correctly, it is organized into dictionaries to iterate and comprehend
'''

#START BATTLE
player1_team=[]
player1_team=random.sample(viablemons,k=6)
player2_team=[]
player2_team=random.sample(viablemons,k=6) #creates teams for both players
print(f"Player 1's team: {player1_team}\n")
print(f"Player 2's team: {player2_team}\n")
player1_hp=[]
P1_MAX_HP=[]
player2_hp=[]
P2_MAX_HP=[]
for i in range(6):
    player1_hp.append(raw_hp[name.index(player1_team[i])])
    player2_hp.append(raw_hp[name.index(player2_team[i])])
p1_movesets=[]
p2_movesets=[]
P1_MAX_HP=player1_hp.copy()
P2_MAX_HP=player2_hp.copy()
for i in range(6):
    p1_movesets.append(random.sample(pokemon_moves[player1_team[i]],k=4))
    p2_movesets.append(random.sample(pokemon_moves[player2_team[i]],k=4))
p1_data=list(zip(player1_hp,P1_MAX_HP,p1_movesets))
p1_data=[list(element) for element in p1_data] #convert list of tuples to list of lists using comprehension
p2_data=list(zip(player2_hp,P2_MAX_HP,p2_movesets))
p2_data=[list(element) for element in p2_data] #convert list of tuples to list of lists using comprehension
p1_team=dict(zip(player1_team,p1_data)) #creates dictionaries for both players, where keys are the pokemon, and the values are the list of the 4 chosen moves
p2_team=dict(zip(player2_team,p2_data))
p1_lead=list(p1_team.keys())[0]
p2_lead=list(p2_team.keys())[0] 
'''
battle starts with both players sending the first pokemon on their team
no team preview as of now, so no lead is actually chosen, could be implemented later
'''
print(f'Player 1 sent out {p1_lead}!\n')
sleep(1)
print(f'Player 2 sent out {p2_lead}!')
turn(p1_team,p1_lead,p2_team,p2_lead,0)
#team values is now a list, element 0 is a list of dynamic hp and static max HP, element 1 is list of moves