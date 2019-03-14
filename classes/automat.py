class Automat:
    states = []
    transitions = []
    num_of_transitions = 0
    num_of_states = 0

    def __init__(self):
        pass

    def get_unique_list_of_states(self):
        arr = []
        for state in self.states:
            arr.append(state.name)
        return set(arr)

    def get_unique_list_of_transitions(self):
        arr = []
        for transition in self.transitions:
            arr.append(transition.name)
        return set(arr)

    def get_states_for_nka_processing(self, state_name, transition_name ):
        arr_end_states = []
        for transition in self.transitions:
            if transition.name == transition_name and transition.start == state_name:
                arr_end_states.append(transition.end)

