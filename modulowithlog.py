from FA_class import DFA, State
# import visualization
import utils
from utils import imageType
import numpy as np
import math
import sys

import hashlib

def hash_2d_array(arr):
    arr_str = "".join("".join(map(str, row)) for row in arr)
    return hashlib.md5(arr_str.encode()).hexdigest()

def binarySearchColumn(arr, l, r, x,limit):
    halvesListColumn=[]
 
    while l <= r:
 
        mid = l + (r - l) // 2
        
        if arr[mid] <= x:
            l = mid + 1
            halvesListColumn.append("SecondColumn")
            if len(halvesListColumn)==limit:
                return halvesListColumn
 
        
        else:
            r = mid - 1
            halvesListColumn.append("FirstColumn")
            if len(halvesListColumn)==limit:
                return halvesListColumn
 
def binarySearchRow(arr, l, r, x,limit):
    halvesListRow=[]
 
    while l <= r:
 
        mid = l + (r - l) // 2
 
        
        if arr[mid] <= x:
            l = mid + 1
            halvesListRow.append("SecondRow")
            if len(halvesListRow)==limit:
                return halvesListRow

        else:
            r = mid - 1
            halvesListRow.append("FirstRow")
            if len(halvesListRow) ==limit:
                return halvesListRow
    
    
 
def Merge(halvesListColumn, halvesListRow):
    address=""

    for i in range(len(halvesListRow)):
        if(halvesListRow[i]=="SecondRow" and halvesListColumn[i]=="SecondColumn"):
            address+="2"
        elif (halvesListRow[i]=="FirstRow" and halvesListColumn[i]=="SecondColumn"):
            address+="3"
        elif (halvesListRow[i]=="SecondRow" and halvesListColumn[i]=="FirstColumn"):
            address+="0"
        else:
            address+="1"
    return address

def get_1_address_dic(image: imageType):
    limit= math.log2(len(image))
    addressDic={}
    listArr=[]
    for i in range (1,len(image)+1):
       listArr.append(i)

    for i in range (len(image)):
       for j in range (len(image)):
          if(image[i][j]==1) :
              listC= binarySearchColumn(listArr,0,len(image)-1,j,limit)
              listR= binarySearchRow(listArr,0,len(image)-1,i,limit)
              addr=Merge(listC, listR)
              
              addressDic[(i,j)]=(addr)
    print(addressDic)
    return addressDic

def get_lr(address , sz):
    lx = 0 
    rx = sz 
    ly = 0 
    ry = sz
    for c in address:
        if c == '0':
            lx = (lx + rx) // 2
            ry = (ly + ry) // 2
        if c == '1':
            rx = (lx + rx) // 2
            ry = (ly + ry) // 2
        if c == '2':
            lx = (lx + rx) // 2
            ly = (ly + ry) // 2
        if c == '3':
            rx = (lx + rx ) // 2
            ly = (ly + ry) // 2
    return {'lx': lx, 'rx': rx , 'ly' : ly , 'ry' : ry}

def solve(image: imageType) -> 'DFA':
    
    
    all_1=get_1_address_dic(image)
    reversed_all_1 = {value: key for key, value in all_1.items()}
    print("all_1\n")
    print(all_1)
    print("REVERSED All 1\n")
    print(reversed_all_1)
    lev = math.log2(len(image))
    dfa = DFA()
    state_id_to_string = {}
    state_id_to_string[0]= ""
            
    new_state = dfa.add_state()
    last_lev_added_states = [dfa.states[0]]     
    
    
    
    
    
    
    
    
    
    
    print(lev)
    for i in range(int(lev)):
        new_added_states = []  
        hsh_map = {}
        for state in last_lev_added_states:  
            for j in range(4):  
                wp = get_lr(state_id_to_string[state.id] + str(j) , len(image)) 
                subpic = []
                for x in range(wp['lx'] , wp['rx']):
                    sub = image[x][wp['ly'] : wp['ry']]
                    subpic.append(sub)
                hsh = hash_2d_array(subpic)
                print(state.id)
                print("address" , state_id_to_string[state.id] + str(j))
                print("X bound and Y bound " , wp['lx'] , wp['rx'] , wp['ly'] , wp['ry'])
                print(subpic)
                print(hsh)
                if hsh in hsh_map:
                    state.add_transition(str(j), hsh_map[hsh])
                    print("tekrari : " , hsh_map[hsh].id)
                else:
                    new_state = dfa.add_state()
                    print("NEW STATE ADDED ID : " , new_state.id)
                    state.add_transition(str(j), new_state)
                    state_id_to_string[new_state.id] = state_id_to_string[state.id] + str(j)
                    new_added_states.append(new_state)
                    hsh_map[hsh] = new_state
        last_lev_added_states = new_added_states  

    for state_id, string_value in state_id_to_string.items():
        if string_value in reversed_all_1:
            id_final_state = state_id
            print("final" , string_value)
            dfa.add_final_state(dfa.states[id_final_state])

    dfa.assign_initial_state(dfa.states[0])
    dfa.alphabet = ['0', '1', '2', '3']    
    return dfa


if __name__ == "__main__":
    print(sys.path)
    
    image = [[1, 1, 1, 1],
             [1, 0, 1, 0],
             [0, 1, 0, 1],
             [1, 1, 1, 1]]
    
    
    
    utils.save_image(image)
    fa = solve(image)

    
