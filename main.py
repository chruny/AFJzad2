import sys
import numpy as np

from classes.automat import Automat
from classes.state import State
from classes.transition import Transition


def export_to_file(automat):
    output_path = 'output/DKA.fsa'
    with open(output_path, 'x') as file:
        file.write(str(automat.num_of_states) + '\n')
        file.write(str(automat.num_of_transitions) + '\n')
        for state in automat.states:
            if state.is_start and state.is_final:
                file.write(str(state.name) + ' IF\n')
            elif state.is_start and not state.is_final:
                file.write(str(state.name) + ' I\n')
            elif not state.is_start and state.is_final:
                file.write(str(state.name) + ' F\n')
            else:
                file.write(str(state.name) + '\n')
        for transition in automat.get_unique_list_of_transitions():
            file.write(str(transition) + '\n')
        for transition in automat.transitions:
            if transition.is_epsilon:
                file.write(str(transition.start) + ', ,' + str(transition.end) + '\n')
            else:
                file.write(str(transition.start) + ',' + str(transition.name) + ',' + str(transition.end) + '\n')


def load_file(filename):
    with open(filename) as file:
        automat = Automat()
        lines = file.readlines()
        for i in range(0, len(lines)):
            line = lines[i].split()
            if "," in line[0]:
                line2 = line[0].split(',')
            if i == 0:
                automat.num_of_states = int(line[0])
            elif i == 1:
                automat.num_of_transitions = int(line[0])
            elif 2 <= i < automat.num_of_states + 2:
                state = State(line[0])
                if len(line) > 1:
                    if line[1] == "IF":
                        state.set_start()
                        state.set_final()
                    elif line[1] == "F":
                        state.set_final()
                    elif line[1] == "I":
                        state.set_start()
                automat.states.append(state)
            elif 2 + automat.num_of_states <= i < 2 + automat.num_of_states + automat.num_of_transitions:
                transition = Transition(line[0])
                # automat.transitions.append(transition)
            elif 2 + automat.num_of_states + automat.num_of_transitions <= i:
                if line2[1] == " ":
                    transition = Transition("E")
                    transition.is_epsilon = True
                else:
                    transition = Transition(line2[1])
                transition.set_start(line2[0])
                transition.set_end(line2[2])
                automat.transitions.append(transition)
    return automat


def process_nka_to_dka(nka_automat):
    # TODO
    print()
    dka_automat = Automat()
    arr_process = []
    arr_transitions = nka_automat.get_get_unique_list_of_transitions()
    arr_tmp = ['states/transitions']
    arr_tmp.extend(arr_transitions)
    arr_tmp_states  = []
    arr_process.append(arr_tmp)
    for i in range(0, np.inf):
        # TODO funkcia ktorej das stav a transition a ona zisti kam sa vies dostat
        for j in range(0, len(arr_transitions)):
            arr_tmp.append(nka_automat.get_states_for_nka_processing())
            arr_tmp.append([nka_automat])
        print()


def main():
    # path = input("Write path to file: ")
    path = "input/nka1.fsa"
    automat = load_file(path)
    export_to_file(automat)
    print()
    # file.write(str() + '\n')


if __name__ == '__main__':
    main()
