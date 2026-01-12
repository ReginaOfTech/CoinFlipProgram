from enum import Enum

from FlipItObjects.BaseObject import BaseObject
from FlipItObjects.DefaultObjects import ClassicDice, ClassicCoin, UserCreated, IllegalCoin, IllegalDice
from Input_Helpers import _set_restart, _check_restart_statements, _check_exit_statements, _check_invalid_input_count, \
    _get_restart, yes_statements, no_statements, _text2int

def get_user_object():
    fails = 0
    object_roll = None
    while True:
        l_user_choice = input("Would you like to use a default item? (C)oin, (D)ice, IllegalCoin(IC), IllegalDice(ID), or (N)one\n").lower()
        _check_exit_statements(l_user_choice)
        if _check_restart_statements(l_user_choice):
            return object_roll
        if l_user_choice == "c" or l_user_choice == "coin":
            object_roll = ClassicCoin()
            break
        elif l_user_choice == "d" or l_user_choice == "dice":
            object_roll = ClassicDice()
            break
        elif l_user_choice == "ic" or l_user_choice == "illegalcoin":
            object_roll = IllegalCoin()
            break
        elif l_user_choice == "id" or l_user_choice == "illegaldice":
            object_roll = IllegalDice()
            break
        elif l_user_choice == "n" or l_user_choice == "none":
            break
        fails += 1
        _check_invalid_input_count(fails)
        print("Invalid input.")
        continue
    return object_roll

def get_user_sides() -> int:
    fails = 0
    while True:
        sides_input = input("How many sides (1-1000000000000) are on the dice?\n").replace(",", "")
        l_sides_input = sides_input.lower()
        _check_exit_statements(l_sides_input)
        if _check_restart_statements(l_sides_input):
            return 0
        if l_sides_input.isdigit():
            sides_num = int(l_sides_input)
        else:
            sides_num = _text2int(l_sides_input)
        if sides_num <= 0 or sides_num%1 != 0:
            fails += 1
            _check_invalid_input_count(fails)
            print("Invalid input. Please input a valid positive whole number.")
            continue
        return sides_num

def get_user_is_weighted() -> bool:
    fails = 0
    while True:
        is_weighted_input = input("Is this a weighted dice?\n")
        l_is_weighted_input = is_weighted_input.lower()
        _check_exit_statements(l_is_weighted_input)
        if _check_restart_statements(l_is_weighted_input):
            return False
        if l_is_weighted_input in yes_statements:
            return True
        if l_is_weighted_input in no_statements:
            return False
        fails += 1
        _check_invalid_input_count(fails)
        print("Invalid input. Please input (Y)es or (N)o.")

def get_user_weighted_side(sides:int):
    fails = 0
    while True:
        weighted_input = input(f"What is the number of the weighted side? Expecting 1-{sides}\n").replace(",", "")
        l_weighted_input = weighted_input.lower()
        _check_exit_statements(l_weighted_input)
        if _check_restart_statements(l_weighted_input):
            return -1
        if l_weighted_input.isdigit():
            side_num = int(l_weighted_input)
        else:
            side_num = _text2int(l_weighted_input)
        if side_num <= 0 or side_num > sides or side_num%1 != 0:
            fails += 1
            _check_invalid_input_count(fails)
            print(f"Invalid input. Please input a valid positive whole number between 1 and {sides}")
            continue
        return side_num

def roll_object(object_to_roll) -> list:
    fails = 0
    roll_num = 1
    while True:
        l_user_rolls = input("How many rolls would you like to perform?\n").lower().replace(",", "")
        _check_exit_statements(l_user_rolls)
        if _check_restart_statements(l_user_rolls):
            return
        if l_user_rolls.isdigit():
            roll_num = int(l_user_rolls)
        else:
            roll_num = _text2int(l_user_rolls)
        if roll_num <= 0 or roll_num%1 != 0:
            fails += 1
            _check_invalid_input_count(fails)
            print(f"Invalid input. Please input a valid positive whole number starting at 1")
            continue
        break
    print("Rolling...")
    return object_to_roll.roll(roll_num)

def analyze_results(results:list):
    print("Here are the results:")
    print(results)
    return

class Questionnaire:
    class States(Enum):
        GREET = 1
        DEFAULT_OBJ = 2
        SIDES = 3
        IS_WEIGHTED = 4
        WEIGHTED_SIDE = 5
        ROLL = 6
        ANALYZE = 7
        ASK_RESTART = 8
        RESTART = 9

    def __init__(self):
        self.state = self.States.GREET.value
        self.object_to_roll = None
        self.roll_results = []
        self.state_count = {}

    def set_state(self, state:States):
        self.state = state.value

    def check_restart(self):
        if _get_restart():
            _set_restart(False)
            self.set_state(self.States.RESTART)
            return True
        return False

    def state_machine(self):
        #-------------GREET----------------------------------
        if self.state == self.States.GREET.value:
            print("Welcome to the Coin Flip Program.")
            print("At any point during the questions use 'exit()' to quit and 'restart' to restart the program.")
            print("--------------------------------------------------------------------------------------------")
            self.set_state(self.States.DEFAULT_OBJ)
        #-------------DEFAULT_OBJ-----------------------------
        elif self.state == self.States.DEFAULT_OBJ.value:
            self.object_to_roll = get_user_object()
            if not self.check_restart():
                if self.object_to_roll is not None:
                    self.set_state(self.States.ROLL)
                else:
                    self.object_to_roll = UserCreated()
                    self.set_state(self.States.SIDES)
        #-----------SIDES------------------------------------
        elif self.state == self.States.SIDES.value:
            self.object_to_roll.sides = get_user_sides()
            if not self.check_restart():
                self.set_state(self.States.IS_WEIGHTED)
        #--------------IS_WEIGHTED--------------------------
        elif self.state == self.States.IS_WEIGHTED.value:
            self.object_to_roll.is_weighted = get_user_is_weighted()
            if not self.check_restart():
                if self.object_to_roll.is_weighted:
                    self.set_state(self.States.WEIGHTED_SIDE)
                else:
                    self.set_state(self.States.ROLL)
        #--------------WEIGHTED_SIDE--------------------------
        elif self.state == self.States.WEIGHTED_SIDE.value:
            self.object_to_roll.weighted_side = get_user_weighted_side(self.object_to_roll.sides)
            if not self.check_restart():
                self.set_state(self.States.ROLL)
        #--------------ROLL----------------------------------
        elif self.state == self.States.ROLL.value:
            self.roll_results = roll_object(self.object_to_roll)
            if not self.check_restart():
                self.state = self.States.ANALYZE.value
        #--------------ANALYZE-------------------------------
        elif self.state == self.States.ANALYZE.value:
            analyze_results(self.roll_results)
            self.set_state(self.States.ASK_RESTART)
        #--------------ASK_RESTART------------------------
        elif self.state == self.States.ASK_RESTART.value:
            user_input = input("Would you like to restart the program? (Y)es (N)o\n").lower()
            if user_input in yes_statements:
                self.set_state(self.States.RESTART)
            else:
                print("Thank you for using Coin Flip Program.")
                _check_exit_statements("exit")
        #----------------RESTART-----------------------
        elif self.state == self.States.RESTART.value:
            print("Prepping for new roll....")
            print("----------------------------------------------------------------------------------------")
            self.set_state(self.States.DEFAULT_OBJ)
            self.object_to_roll = None
            self.roll_results = []
            self.state_count = {}

if __name__ == "__main__":
    questions = Questionnaire()
    while True:
        questions.state_machine()