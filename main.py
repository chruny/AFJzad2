import sys

from classes.automat import Automat
from classes.state import State
from classes.transition import Transition


def main():
    #path = input("Write path to file: ")
    path = "input/nka4.fsa"
    load_file(path)
    print()


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
                else:
                    transition = Transition(line2[1])
                transition.set_start(line2[0])
                transition.set_end(line2[2])
                automat.transitions.append(transition)
    print()


if __name__ == '__main__':
    main()
