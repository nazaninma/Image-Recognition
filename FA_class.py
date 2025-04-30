import json



class State:
    
    __counter = 0

    @classmethod
    def reset_counter(cls):
        cls.__counter=0
    
    def __init__(self, id: None) -> None:
        
        if id is None:
            self.id = State._get_next_id()
        else:
            self.id = id
        
        self.transitions: dict[str, 'State'] = {}

    
    def add_transition(self, symbol: str, state: 'State') -> None:
        self.transitions[symbol] = state

    
    @classmethod
    def _get_next_id(cls) -> int:
        current_id = cls.__counter
        cls.__counter += 1
        return current_id

class DFA:
    
    def __init__(self) -> None:
        
        self.init_state = None
        self.states: list['State'] = []
        self.alphabet: list['str'] = []
        self.final_states: list['State'] = []

    
    @staticmethod
    def deserialize_json(json_str: str) -> 'DFA':
        
        fa = DFA()
        
        json_fa = json.loads(json_str)

        
        fa.alphabet = json_fa["alphabet"]

        
        for state_str in json_fa["states"]:
            fa.add_state(int(state_str[2:]))

        
        fa.init_state = fa.get_state_by_id(int(json_fa["initial_state"][2:]))

        
        for final_str in json_fa["final_states"]:
            fa.add_final_state(fa.get_state_by_id(int(final_str[2:])))

        
        for state_str in json_fa["states"]:
            for symbol in fa.alphabet:
                fa.add_transition(fa.get_state_by_id(int(state_str[2:])), fa.get_state_by_id(int(json_fa[state_str][symbol][2:])),
                                  symbol)

        return fa

    
    def serialize_json(self) -> str:
        
        fa = {
            "states": list(map(lambda s: f"q_{s.id}", self.states)),
            "initial_state": f"q_{self.init_state.id}",
            "final_states": list(map(lambda s: f"q_{s.id}", self.final_states)),
            "alphabet": self.alphabet
        }

        
        for state in self.states:
            fa[f"q_{state.id}"] = {}
            for symbol in self.alphabet:
                fa[f"q_{state.id}"][symbol] = f"q_{state.transitions[symbol].id}"

        
        return json.dumps(fa)

    def add_state(self, id: int | None = None) -> State:
        
        new_state = State(id)
        
        self.states.append(new_state)
        
        return new_state

    def add_transition(self, from_state: State, to_state: State, input_symbol: str) -> None:
        from_state.add_transition(input_symbol,to_state)

    def assign_initial_state(self, state: State) -> None:
        self.init_state=state

    def add_final_state(self, state: State) -> None:
        
        self.final_states.append(state)

    def get_state_by_id(self, id) -> State | None:
        
        for state in self.states:
            
            if state.id == id:
                
                return state
        
        return None

    def is_final(self, state: State) -> bool:
        if self.final_states.count(state)>=1:
            return True
        return False

class NFAState:
    __counter = 0

    def __init__(self, id: None) -> None:
        if id is None:
            self.id = NFAState._get_next_id()
        else:
            self.id = id
        
        self.transitions: list[tuple[str | None, set['NFAState']]] = []

    def add_transition(self, symbol: str | None, state: 'NFAState') -> None:
        
        self.transitions.append((symbol, {state}))  

    @classmethod
    def _get_next_id(cls) -> int:
        current_id = cls.__counter
        cls.__counter += 1
        return current_id


class NFA:
    def __init__(self) -> None:
        self.init_state = None
        self.states: list['NFAState'] = []
        self.alphabet: list['str'] = []
        self.final_states: list['NFAState'] = []

    @staticmethod
    def convert_DFA_instance_to_NFA_instance(dfa_machine: 'DFA') -> 'NFA':
        nfa_machine = NFA()

        
        for dfa_state in dfa_machine.states:
            nfa_state = NFAState(dfa_state.id)
            
            for symbol, state in dfa_state.transitions.items():
                nfa_state.add_transition(symbol, state)
            
            nfa_machine.states.append(nfa_state)
            
            if dfa_machine.init_state == dfa_state:
                nfa_machine.init_state = nfa_state
            
            if dfa_state in dfa_machine.final_states:
                nfa_machine.final_states.append(nfa_state)

        nfa_machine.alphabet = dfa_machine.alphabet
        return nfa_machine

    @staticmethod
    def union(machine1: 'NFA', machine2: 'NFA') -> 'NFA':
        
        union_machine = NFA()
        
        
        union_machine.init_state = NFAState(None)
        
        
        union_machine.init_state.add_transition(None, machine1.init_state)
        union_machine.init_state.add_transition(None, machine2.init_state)
        
        
        union_machine.states.extend(machine1.states)
        union_machine.states.extend(machine2.states)
        
        
        union_machine.final_states.extend(machine1.final_states)
        union_machine.final_states.extend(machine2.final_states)
        
        
        union_machine.final_states = list(set(union_machine.final_states))
        
        
        union_final_state = NFAState(None)
        union_machine.final_states.append(union_final_state)
        
        
        for final_state in union_machine.final_states:
            final_state.add_transition(None, union_final_state)
            if(final_state!=union_final_state):
                union_machine.final_states.remove(final_state)
        
        
        union_machine.alphabet = list(set(machine1.alphabet) | set(machine2.alphabet))
        
        return union_machine

    @staticmethod
    def concat(machine1: 'NFA', machine2: 'NFA') -> 'NFA':
        
        concat_machine = NFA()
        
        concat_machine.init_state=machine1.init_state

        
        concat_machine.states.extend(machine1.states)
        concat_machine.states.extend(machine2.states)
        

        
        for final_state in machine1.final_states:
            final_state.add_transition(None, machine2.init_state)
        
        concat_machine.final_states = machine2.final_states
        
        concat_machine.alphabet = list(set(machine1.alphabet) | set(machine2.alphabet))
        
        
        
        return concat_machine

    @staticmethod
    def star(machine: 'NFA') -> 'NFA':
        
        star_machine = NFA()
        
        
        star_machine.init_state = NFAState(None)
        
        
        star_machine.init_state.add_transition(None, machine.init_state)
        
        
        star_machine.states.extend(machine.states)
        
        
        star_machine.init_state.add_transition(None, machine.init_state)
        for final_state in machine.final_states:
            star_machine.init_state.add_transition(None, final_state)
        for final_state in machine.final_states:
            final_state.add_transition(None, machine.init_state)
        
        
        star_machine.alphabet = machine.alphabet
        
        
        star_machine.final_states = machine.final_states
        
        return star_machine

    def serialize_to_json(self) -> str:
        
        nfa_json = {
            "states": [state.id for state in self.states],
            "initial_state": self.init_state.id,
            "final_states": [state.id for state in self.final_states],
            "alphabet": self.alphabet,
            "transitions": {}
        }
        
        
        for state in self.states:
            state_transitions = {}
            for transition in state.transitions:
                symbol, next_states = transition
                next_state_ids = [next_state.id for next_state in next_states]
                state_transitions[symbol] = next_state_ids
            nfa_json["transitions"][state.id] = state_transitions
        
        return json.dumps(nfa_json)

