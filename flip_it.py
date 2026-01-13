####################################################################
# flip_it.py
# Purpose: This is where if __name__ == "__main__": is located
####################################################################
from enum import Enum

from flipit_objects.default_objects import ClassicDice, ClassicCoin, UserCreated, IllegalCoin, IllegalDice
from input_helpers import _set_restart, _check_restart_statements, _check_exit_statements, _check_invalid_input_count, \
    _get_restart, yes_statements, no_statements, _text2int

def get_user_object():
    """
   Asks the user if they will be using a default object or creating their own custom one.

    Returns:
       if the user wants to use a default object that is returned else None is returned to signal that a custom object is needed.
    """
    fails = 0
    object_roll = None
    while True:
        l_user_choice = input("Would you like to use a default item? (C)oin, (D)ice, IllegalCoin(IC), IllegalDice(ID), or (N)one\n").lower()
        _check_exit_statements(l_user_choice)
        if _check_restart_statements(l_user_choice):
            return object_roll
        # TODO: Clean this up so that it is easier to maintain
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
    """
    Asks the user how many sides they would like to use.

    Returns:
       A whole int greater than 0.
    """
    fails = 0
    while True:
        sides_input = input("How many sides (1-1000000000000) are on the dice?\n").replace(",", "")
        l_sides_input = sides_input.lower()
        _check_exit_statements(l_sides_input)
        if _check_restart_statements(l_sides_input):
            return 0
        # If the input contains digits (0, 1, 2, etc) then use that
        # else call the internal helper to translate the number
        if l_sides_input.isdigit():
            sides_num = int(l_sides_input)
        else:
            sides_num = _text2int(l_sides_input)
        # Make sure that the value is a positive value AND is a whole number
        if sides_num <= 0 or sides_num%1 != 0:
            fails += 1
            _check_invalid_input_count(fails)
            print("Invalid input. Please input a valid positive whole number.")
            continue
        return sides_num

def get_user_is_weighted() -> bool:
    """
    Asks the user if the object has a weighted side that is more likely to be used.

    Returns:
        boolean if the object is weighted
    """
    fails = 0
    while True:
        is_weighted_input = input("Is this a weighted dice? (Y)es or (N)o\n")
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

def get_user_weighted_side(sides:int) -> int:
    """
    Asks the user which side is weighted. This should only be reached if the object is weighted.

    Returns:
       if successful a whole positive int that is less than or equal to sides.
       else a negative value is returned
    """
    fails = 0
    while True:
        weighted_input = input(f"What is the number of the weighted side? Expecting 1-{sides}\n").replace(",", "")
        l_weighted_input = weighted_input.lower()
        _check_exit_statements(l_weighted_input)
        if _check_restart_statements(l_weighted_input):
            return -1
        # If the input contains digits (0, 1, 2, etc) then use that
        # else call the internal helper to translate the number
        if l_weighted_input.isdigit():
            side_num = int(l_weighted_input)
        else:
            side_num = _text2int(l_weighted_input)
        # Make sure that the value is a positive value AND is a whole number
        if side_num <= 0 or side_num > sides or side_num%1 != 0:
            fails += 1
            _check_invalid_input_count(fails)
            print(f"Invalid input. Please input a valid positive whole number between 1 and {sides}")
            continue
        return side_num

def get_user_change_default(default_side:int) -> bool:
    """
    Asks the user if they would like to change the default side for an illegally weighted object.

    Returns:
       bool if user is changing the default side.
    """
    fails = 0
    while True:
        change_default = input(f"Would you like to change the default weighted side of {default_side} for the object? (Y)es or (N)o\n")
        l_change_default = change_default.lower()
        _check_exit_statements(l_change_default)
        if _check_restart_statements(l_change_default):
            return False
        if l_change_default in yes_statements:
            return True
        if l_change_default in no_statements:
            return False
        fails += 1
        _check_invalid_input_count(fails)
        print("Invalid input. Please input (Y)es or (N)o.")

def roll_object(object_to_roll) -> list:
    """
    Asks the user how many times the object should be rolled then proceeds to call BaseObject.roll

    Returns:
       list of results sent back from BaseObject.roll. This is not guaranteed to be not to be empty.
    """
    fails = 0
    roll_num = 1
    while True:
        l_user_rolls = input("How many rolls would you like to perform?\n").lower().replace(",", "")
        _check_exit_statements(l_user_rolls)
        if _check_restart_statements(l_user_rolls):
            return []
        # If the input contains digits (0, 1, 2, etc) then use that
        # else call the internal helper to translate the number
        if l_user_rolls.isdigit():
            roll_num = int(l_user_rolls)
        else:
            roll_num = _text2int(l_user_rolls)
        # Make sure that the value is a positive value AND is a whole number
        if roll_num <= 0 or roll_num%1 != 0:
            fails += 1
            _check_invalid_input_count(fails)
            print(f"Invalid input. Please input a valid positive whole number starting at 1")
            continue
        break
    print("Rolling...")
    return object_to_roll.roll(roll_num)

def analyze_results(results:list):
    # TODO: Check for empty list, do analytics manually, create OpenAI API w/Ollama, Work with LLM to find insights on data
    # TODO: Move to another file to maintain code hygiene
    print("Here are the results:")
    print(results)
    return

class Questionnaire:
    """
    Holds the state machine to handle logic progression in questions as well as the object that is being used/created.
    """
    class States(Enum):
        """
        Logical triggers for questions/actions

        Current lineup:

        GREET = 1 #Triggers the official greeting. Currently only ran once at startup\n
        DEFAULT_OBJ = 2 #Asks the user what object to use\n
        SIDES = 3 #How many sides for the object?\n
        IS_WEIGHTED = 4 #Is the object weighted?\n
        WEIGHTED_SIDE = 5 #Should only be set if IS_WEIGHTED came back as True\n
        ROLL = 6 #Roll the object\n
        ANALYZE = 7 #Analyze the results stored in a list\n
        ASK_RESTART = 8 #Ask user if they would like to RESTART. Exits if 'no'\n
        RESTART = 9 #Resets all internal class attributes\n
        ILLEGAL_DEFAULT_SIDE = 10 #Would you like to change default side of illegal object?\n
        """
        GREET = 1 #Triggers the official greeting. Currently only ran once at startup
        DEFAULT_OBJ = 2 #Asks the user what object to use
        SIDES = 3 #How many sides for the object?
        IS_WEIGHTED = 4 #Is the object weighted?
        WEIGHTED_SIDE = 5 #Should only be set if IS_WEIGHTED came back as True
        ROLL = 6 #Roll the object
        ANALYZE = 7 #Analyze the results stored in a list
        ASK_RESTART = 8 #Ask user if they would like to RESTART. Exits if 'no'
        RESTART = 9 #Resets all internal class attributes
        ILLEGAL_DEFAULT_SIDE = 10 #Would you like to change default side of illegal object?

    def __init__(self):
        self.state = self.States.GREET
        self.object_to_roll = None
        self.roll_results = []
        self.state_count = {}

    def state(self) -> States:
        return self.state

    def set_state(self, state:States) -> None:
        self.state = state

    def check_restart(self):
        if _get_restart():
            _set_restart(False)
            self.set_state(self.States.RESTART)

    def state_machine(self):
        """
        State machine for question logic

        Actual handling of questions (input/validation checks) should be handled in separate methods.
        """
        #Each iteration check to see if Input_Helpers/restart global variable has been set
        self.check_restart()

        match self.state:
        #-------------GREET----------------------------------
            case self.States.GREET:
                print("Welcome to Flip It!!!")
                print("At any point during the questions use 'exit()' to quit and 'restart' to restart the program.")
                print("--------------------------------------------------------------------------------------------")
                self.set_state(self.States.DEFAULT_OBJ)
        #-------------DEFAULT_OBJ-----------------------------
            case self.States.DEFAULT_OBJ:
                self.object_to_roll = get_user_object()
                if self.object_to_roll is not None:
                    if self.object_to_roll.is_weighted:
                        self.set_state(self.States.ILLEGAL_DEFAULT_SIDE)
                    else:
                        self.set_state(self.States.ROLL)
                else:
                    self.object_to_roll = UserCreated()
                    self.set_state(self.States.SIDES)
        #-----------SIDES------------------------------------
            case self.States.SIDES:
                self.object_to_roll.sides = get_user_sides()
                self.set_state(self.States.IS_WEIGHTED)
        #--------------IS_WEIGHTED--------------------------
            case self.States.IS_WEIGHTED:
                self.object_to_roll.is_weighted = get_user_is_weighted()
                if self.object_to_roll.is_weighted:
                    self.set_state(self.States.WEIGHTED_SIDE)
                else:
                    self.set_state(self.States.ROLL)
        #-------------ILLEGAL_DEFAULT_SIDE--------------------
            case self.States.ILLEGAL_DEFAULT_SIDE:
                if get_user_change_default(self.object_to_roll.weighted_side):
                    self.set_state(self.States.WEIGHTED_SIDE)
                else:
                    self.set_state(self.States.ROLL)
        #--------------WEIGHTED_SIDE--------------------------
            case self.States.WEIGHTED_SIDE:
                self.object_to_roll.weighted_side = get_user_weighted_side(self.object_to_roll.sides)
                self.set_state(self.States.ROLL)
        #--------------ROLL----------------------------------
            case self.States.ROLL:
                self.roll_results = roll_object(self.object_to_roll)
                self.set_state(self.States.ANALYZE)
        #--------------ANALYZE-------------------------------
            case self.States.ANALYZE:
                analyze_results(self.roll_results)
                self.set_state(self.States.ASK_RESTART)
        #--------------ASK_RESTART------------------------
            case self.States.ASK_RESTART:
                user_input = input("Would you like to restart the program? (Y)es (N)o\n").lower()
                if user_input in yes_statements:
                    self.set_state(self.States.RESTART)
                else:
                    # Everything else, even if a typo, triggers an exit.
                    print("Thank you for using Coin Flip Program.")
                    _check_exit_statements("exit")
        #----------------RESTART-----------------------
            case self.States.RESTART:
                print("Prepping for new roll....")
                print("----------------------------------------------------------------------------------------")
                self.set_state(self.States.DEFAULT_OBJ)
                self.object_to_roll = None
                self.roll_results = []
                self.state_count = {}

if __name__ == "__main__":
    # Only one instance of the questionnaire is used. Allows for future development of conversation tracking.
    questions = Questionnaire()
    while True:
        questions.state_machine()
