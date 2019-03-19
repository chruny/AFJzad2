import numpy as np
class Automat:
    states = []
    transitions = []
    num_of_transitions = 0
    num_of_states = 0
    q = []

    def __init__(self):
        pass

    def get_unique_list_of_states(self):
        arr = []
        for state in self.states:
            arr.append(state.name)
        return list(set(arr))

    def get_unique_list_of_transitions(self):
        arr = []
        for transition in self.transitions:
            arr.append(transition.name)
        return list(set(arr))

    def get_states_for_nka_processing(self, state_name, transition_name):
        arr_end_states = []
        if isinstance(state_name, tuple):
            for state in state_name:
                for transition in self.transitions:
                    if transition.name == transition_name and transition.start == state:
                        arr_end_states.append(transition.end)
        else:
            for transition in self.transitions:
                if transition.name == transition_name and transition.start == state_name:
                    arr_end_states.append(transition.end)
        arr_end_states = list(set(arr_end_states))
        return arr_end_states

    def get_start_state(self):
        for state in self.states:
            if state.is_start:
                return state

    def get_end_states(self):
        states = []
        for state in self.states:
            if state.is_final:
                states.append(state.name)
        return states

    def get_start_states(self):
        states = []
        for state in self.states:
            if state.is_start:
                states.append(state.name)
        return states

    def convert_from_nfa(self, nfa):
        self.transitions = nfa.transition
        self.start_state = nfa.get_start_state()

        nka_transition_dict = {}
        dka_transition_dict = {}

        # Combine NFA transitions
        for transition in nfa.transitions:
            starting_state = transition.start
            transition_symbol = transition.name
            ending_state = transition.end

            if (starting_state, transition_symbol) in nka_transition_dict:
                nka_transition_dict[(starting_state, transition_symbol)].append(ending_state)
            else:
                nka_transition_dict[(starting_state, transition_symbol)] = [ending_state]

        self.q.append((0,))

        # Convert NFA transitions to DFA transitions
        for dfa_state in self.q:
            for transition in nfa.transitions:
                if len(dfa_state) == 1 and (dfa_state[0], transition) in nka_transition_dict:
                    dka_transition_dict[(dfa_state, transition)] = nka_transition_dict[(dfa_state[0], transition)]

                    if tuple(dka_transition_dict[(dfa_state, transition)]) not in self.q:
                        self.q.append(tuple(dka_transition_dict[(dfa_state, transition)]))
                else:
                    destinations = []
                    final_destination = []

                    for nfa_state in dfa_state:
                        if (nfa_state, transition) in nka_transition_dict and nka_transition_dict[
                            (nfa_state, transition)] not in destinations:
                            destinations.append(nka_transition_dict[(nfa_state, transition)])

                    if not destinations:
                        final_destination.append(None)
                    else:
                        for destination in destinations:
                            for value in destination:
                                if value not in final_destination:
                                    final_destination.append(value)

                    dka_transition_dict[(dfa_state, transition)] = final_destination

                    if tuple(final_destination) not in self.q:
                        self.q.append(tuple(final_destination))

        # Convert NFA states to DFA states
        for key in dka_transition_dict:
            self.transition_functions.append(
                (self.q.index(tuple(key[0])), key[1], self.q.index(tuple(dka_transition_dict[key]))))

        for q_state in self.q:
            for nfa_accepting_state in nfa.accepting_states:
                if nfa_accepting_state in q_state:
                    self.accepting_states.append(self.q.index(q_state))
                    self.num_accepting_states += 1
