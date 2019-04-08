import numpy as np


class Automat:
    states = []
    transitions = []
    num_of_transitions = 0
    num_of_states = 0
    q = []

    def __init__(self):
        self.states = []
        self.transitions = []
        self.num_of_transitions = 0
        self.num_of_states = 0
        self.q = []

    def get_unique_list_of_states(self):
        arr = []
        for state in self.states:
            arr.append(state.name)
        return list(set(arr))

    def get_unique_list_of_transitions(self):
        arr = []
        for transition in self.transitions:
            if not transition.name == "E":
                arr.append(transition.name)
        return sorted(list(set(arr)))

    def get_start_with_epsilon(self):
        arr_end_states = []
        start = self.get_start_state()
        arr_end_states.append(start)
        for state in arr_end_states:
            for transition in self.transitions:
                if transition.start == state and transition.is_epsilon:
                    arr_end_states.append(transition.end)
        if len(arr_end_states) > 0:
            arr_end_states = list(set(arr_end_states))
            return tuple(arr_end_states)
        else:
            return start

    def closure(self, state_name, transition_name, i):
        arr_end_states = []
        arr_end_states.append(state_name)
        if isinstance(state_name, tuple):
            for tmp_state in arr_end_states:
                for state in tmp_state:
                    for transition in self.transitions:
                        if (transition.name == transition_name or (
                                transition.is_epsilon and i != 0)) and transition.start == state:
                            arr_end_states.append(transition.end)
        else:
            for transition in self.transitions:
                if (transition.name == transition_name or transition.is_epsilon) and transition.start == state_name:
                    arr_end_states.append(transition.end)
        arr_end_states = list(set(arr_end_states))
        return sorted(arr_end_states)

    def get_start_state_object(self):
        for state in self.states:
            if state.is_start:
                return state

    def get_end_states(self):
        states = []
        for state in self.states:
            if state.is_final:
                states.append(state.name)
        return states

    def get_start_state(self):
        for state in self.states:
            if state.is_start:
                return state.name

    def get_start_states(self):
        states = []
        for state in self.states:
            if state.is_start:
                states.append(state.name)
        return states

    def get_transition_for_state(self,state_name):
        arr_transition = []
        for transition in self.transitions:
            if transition.start == state_name:
                arr_transition.append(transition)
        return arr_transition

    def check_if_state_is_final(self, name):
        for state in self.states:
            if state.name == name and state.is_final:
                return True
        return False
