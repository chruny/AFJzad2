import sys
import numpy as np
import os

from classes.automat import Automat
from classes.state import State
from classes.transition import Transition


def export_to_file(automat,output_path):
    # output_path = 'output.txt'
    with open(output_path, 'w') as file:
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
                if line2[1] == "":
                    transition = Transition("E")
                    transition.is_epsilon = True
                else:
                    transition = Transition(line2[1])
                transition.set_start(line2[0])
                transition.set_end(line2[2])
                automat.transitions.append(transition)
    return automat


def convert_tuple_to_string(tup_names):
    names = ""
    if isinstance(tup_names, tuple):
        for name in tup_names:
            names += name
        return names
    else:
        return tup_names


def process_nka_to_dka3(nka_auto):
    arr_trans = nka_auto.get_unique_list_of_transitions()
    arr_symbols = [nka_auto.get_start_with_epsilon()]
    arr_states = nka_auto.get_unique_list_of_states()
    arr_process = []

    for i in range(0, 100000):
        tmp_states2 = [None] * len(arr_trans)

        for j in range(0, len(arr_trans)):
            try:
                states = nka_auto.closure(arr_symbols[i], arr_trans[j], i)
                if len(states) > 1:
                    tmp_states2[j] = tuple(states)  # prerobenie na nove
                    if not tuple(states) in arr_symbols:
                        arr_symbols.append(tuple(states))
                elif len(states) == 1:
                    tmp_states2[j] = tuple(states)  # prerobenie na nove
                    if not states[0] in arr_symbols:
                        arr_symbols.append(states[0])
            except IndexError as e:
                # arr_process.append(tmp_states2)
                dka_auto = create_dka_automat_from_tables2(arr_process, arr_symbols, arr_trans, nka_auto)
                return dka_auto

        arr_process.append(tmp_states2)
        # arr_process.append(tmp_states)


def create_dka_automat_from_tables2(process, symbols, transitions, nka_auto):
    dka_auto = Automat()
    dka_auto.num_of_states = len(symbols)
    dka_auto.num_of_transitions = len(transitions)

    for it, symbol in enumerate(symbols):
        state = State(convert_tuple_to_string(symbol))
        if isinstance(symbol, tuple):
            for sym in symbol:
                if nka_auto.check_if_state_is_final(sym):
                    state.set_final()
        else:

            if nka_auto.check_if_state_is_final(symbol):
                state.set_final()
        if it == 0:
            state.set_start()
        dka_auto.states.append(state)
    for it, tmp_trans in enumerate(transitions):
        for j in range(len(symbols)):
            transition = Transition(convert_tuple_to_string(tmp_trans))
            transition.set_start(convert_tuple_to_string(symbols[j]))
            transition.set_end(convert_tuple_to_string(process[j][it]))
            if transition.end is not None:
                dka_auto.transitions.append(transition)
    return dka_auto


def acceptance_of_word(dka_auto):
    txt = input("Write a word with:")
    state = dka_auto.get_start_state()
    for i in range(0, len(txt)):
        status = False
        transitions = dka_auto.get_transition_for_state(state)
        for transition in transitions:
            if transition.name == txt[i]:
                status = True
                state = transition.end
                pass
        if status == False:
            print("NonAccepted")
            return
    if status == True:
        print("Accepted")


def main(path, path2):
    if os.path.exists(path):
        nka_automat = load_file(path)
        dka_auto = process_nka_to_dka3(nka_automat)
        export_to_file(dka_auto, path2)
        acceptance_of_word(dka_auto)


if __name__ == '__main__':
    # if sys.argv[1] is not None and sys.argv[2] is not None:
    #     path1 = sys.argv[1]
    #     path2 = sys.argv[2]
    # else:
    #     sys.stdout.write("You forgot to add argument")

    main('nka5.txt','output.txt')
    # main(path1, path2)
