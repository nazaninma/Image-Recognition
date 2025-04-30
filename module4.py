from math import log2
from utils import imageType
from FA_class import DFA, State
import FA_class
import math
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
            address+="3"
        elif (halvesListRow[i]=="FirstRow" and halvesListColumn[i]=="SecondColumn"):
            address+="1"
        elif (halvesListRow[i]=="SecondRow" and halvesListColumn[i]=="FirstColumn"):
            address+="2"
        else:
            address+="0"
    return address

def get_address_dic(image: imageType):
    limit= math.log2(len(image))
    addressDic={}
    listArr=[]
    for i in range (1,len(image)+1):
       listArr.append(i)

    for i in range (len(image)):
       for j in range (len(image)):
            listR= binarySearchRow(listArr,0,len(image)-1,i,limit)
            listC= binarySearchColumn(listArr,0,len(image)-1,j,limit)
            addr=Merge(listC, listR)  
            addressDic[(i,j)]=(addr)
    return addressDic

def solve(json_str: str, resolution: int) -> imageType:
    dfa = DFA.deserialize_json(json_str)
    res = [[0 for _ in range(resolution)] for _ in range(resolution)]
    addressdic = get_address_dic(res)
    for i in range(resolution):
        for j in range(resolution):
            state = dfa.init_state
            for char in addressdic[(i , j)]:
                state = state.transitions[char]
                
            if dfa.is_final(state):
                
                res[i][j] = 1
            else:
                res[i][j] = 0
    return res

if __name__ == "__main__":
    pic_arr = solve(
            """
            {
                "states": ["q_0", "q_1", "q_2", "q_3", "q_4"],
                "initial_state": "q_0",
                "final_states": ["q_3"],
                "alphabet": ["0", "1", "2", "3"],
                "q_0": {"0": "q_1", "1": "q_1", "2": "q_2", "3": "q_2"},
                "q_1": {"0": "q_3", "1": "q_3", "2": "q_3", "3": "q_4"},
                "q_2": {"0": "q_4", "1": "q_3", "2": "q_3", "3": "q_3"},
                "q_3": {"0": "q_3", "1": "q_3", "2": "q_3", "3": "q_3"},
                "q_4": {"0": "q_4", "1": "q_4", "2": "q_4", "3": "q_4"}
            }
            """,
            4
        )
    print(pic_arr)



















