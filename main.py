import sys
import numpy as np

from classes.automat import Automat
from classes.state import State
from classes.transition import Transition


def export_to_file(automat):
    output_path = 'output/DKA.txt'
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


def process_nka_to_dka2(nka_automat):
    print()
    dka_automat = Automat()
    dka_automat.convert_from_nfa(nka_automat)


def process_nka_to_dka(nka_automat):
    # TODO
    print()
    dka_automat = Automat()
    arr_process = []
    arr_transitions = nka_automat.get_unique_list_of_transitions()
    arr_tmp = ['states/transitions']
    arr_tmp.extend(arr_transitions)
    dict_tmp_states = {}
    for element in nka_automat.get_unique_list_of_states():
        dict_tmp_states[element] = element
    key = ''.join(nka_automat.get_unique_list_of_states())
    arr_process.append(arr_tmp)
    for i in range(0, 100000):
        keys = list(dict_tmp_states.keys())
        for j in range(0, len(arr_transitions)):
            states = []
            key_tmp = keys[i]
            tran_tmp = arr_transitions[j]
            states = nka_automat.get_states_for_nka_processing(dict_tmp_states[keys[i]], arr_transitions[j])
            if len(states) > 0:
                key = tuple(states)
                # key = ''.join(states)
                if key not in dict_tmp_states:
                    dict_tmp_states[key] = states


def process_nka_to_dka3(nka_auto):
    print()
    arr_trans = nka_auto.get_unique_list_of_transitions()
    arr_symbols = nka_auto.get_unique_list_of_states()
    arr_states = nka_auto.get_unique_list_of_states()
    arr_process = []
    for i in range(0, 100000):
        tmp_states = []
        for j in range(0, len(arr_states)):
            try:
                states = nka_auto.get_states_for_nka_processing(arr_symbols[i], arr_trans[j])
                if len(states) > 1:
                    tmp_states.append(tuple(states))
                    if not tuple(states) in arr_symbols:
                        arr_symbols.append(tuple(states))
                elif len(states) == 1:
                    tmp_states.append(tuple(states))
                    if not states[0] in arr_symbols:
                        arr_symbols.append(states[0])
            except IndexError:
                arr_process.append(tmp_states)
                create_dka_automat_from_tables(arr_process,arr_symbols,arr_trans,nka_auto)

        arr_process.append(tmp_states)


def create_dka_automat_from_tables(process, symbols, transitions, nka_auto):
    dka_auto = Automat()
    arr_end_states = nka_auto.get_end_states()
    arr_start_states = nka_auto.get_start_states()
    dka_auto.num_of_states = len(symbols)
    dka_auto.num_of_transitions = len(transitions)

    for it, symbol in enumerate(symbols):
        for j in range(0, len(transitions)):
            dka_auto.states.append(symbol)
            state = State(symbols[it][j])

            if any(elem in symbols[it] for elem in arr_start_states):
                state.is_start = True
            if any(elem in symbols[it] for elem in arr_end_states):
                state.is_final = True
            if len(process[it][j]) > 1:
                for elem in process[it][j]:
                    trans = Transition(transitions[j])
                    trans.set_start(state.name)
                    trans.set_end(elem)
                    dka_auto.transitions.append(trans)
            elif len(process[it][j]) == 1:
                trans = Transition(transitions[j])
                trans.set_start(state.name)
                trans.set_end(process[it][j][0])
                dka_auto.transitions.append(trans)


def main():
    # path = input("Write path to file: ")
    path = "input/nka1.txt"
    nka_automat = load_file(path)
    # process_nka_to_dka2(nka_automat)
    process_nka_to_dka3(nka_automat)
    # process_nka_to_dka(nka_automat)
    export_to_file(nka_automat)

    print()

    # file.write(str() + '\n')


if __name__ == '__main__':
    main()
