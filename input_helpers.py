####################################################################
# input_helpers.py
# Purpose: Functions/Variables that assist in the validation and/or reading of user input
####################################################################
import sys

# Number of times that a user can fail input validation before the system gracefully exits
max_failures = 10
# Global variable that signals the system to do a restart when needed
restart = False
# Global variable that stores user acceptance inputs including typos
yes_statements = ['yes', 'y', 'ye', 'ys', 'es']
# Global variable that stores user decline inputs including typos
no_statements = ['no', 'n', 'o']
# Global variable that stores user exit inputs including typos
exit_statements = ['exit', 'exit()', 'exi', 'ex', 'xit', 'q', 'quit', 'quit()', 'qu', 'qui', 'uit']
# Global variable that stores user restart inputs including typos
restart_statements = ['restart', 'restart()', 'restar', 'resta', 'rest', 're', 'res', 'start', 'tart', 'art', 'retart', 'rstart']

def _text2int(text_num:str) -> int:
    """
    Takes in a natural language string for numbers and converts it to an integer

    one->1, two->3, hundred->100, etc

    Args:
        text_num: String to convert to int

    Returns:
       int >= 0 if the text_num was converted to int, else return -1
    """
    # Store words in the appropriate indexes to calculate their values
    numwords = {}
    units = [
    "zero", "one", "two", "three", "four", "five", "six", "seven", "eight",
    "nine", "ten", "eleven", "twelve", "thirteen", "fourteen", "fifteen",
    "sixteen", "seventeen", "eighteen", "nineteen",
    ]

    tens = ["", "", "twenty", "thirty", "forty", "fifty", "sixty", "seventy", "eighty", "ninety"]

    scales = ["hundred", "thousand", "million", "billion", "trillion"]

    # First include 'and' so that "one hundred and two" can be successfully read
    # each word's value is (scale, increment)
    # scale = increase hundreds or greater places
    # increment = increase ones or tens places
    numwords["and"] = (1, 0)
    # Go through each of the lists converting the words into their numerical values
    # for 1, one in enumerate(units): numwords['one'] = (1, 1)
    for idx, word in enumerate(units):    numwords[word] = (1, idx)
    # for 2, twenty in enumerate(tens): numwords['twenty'] = (1, 2*10) ie (1,20)
    for idx, word in enumerate(tens):     numwords[word] = (1, idx * 10)
    # for 0, hundred in enumerate(scales): numwords['hundred'] = (10^(2),0) ie (100,0)
    # for 1, thousand in enumerate(scales): numwords['thousand'] = (10^(1*3), 0) ie (1000, 0)
    # if idx*3 is 0 (falsy) then it will default to 2 else idx*3 is used as long as non-zero(truthy) is calculated
    for idx, word in enumerate(scales):   numwords[word] = (10 ** (idx * 3 or 2), 0)

    # Time to start the actual conversion
    current = result = 0
    # Split the text_num string into words separated by spaces and hyphens
    # "one hundred and thirty-one"->['one', 'hundred', 'and', 'thirty', 'one']
    for hyp_word in text_num.split():
        for word in hyp_word.split("-"):
            # If word is not included (ie typo, half values, ect) gracefully handle by returning an invalid value
            if word not in numwords:
              return -1

            scale, increment = numwords[word]
            # update the current value with the new words 'value'
            # 'one': 1 = 0 * 1 + 1
            # 'hundred: 100 = 1 * 100 + 0
            # 'and': 100 = 100 * 1 + 0
            # 'thirty': 130 = 100 * 1 + 30
            # 'three': 133 = 130 * 1 + 3
            current = current * scale + increment
            # A large scale will result in math errors
            # Reset current so that math errors do not occur
            # one million two thousand three hundred and forty-four
            # 'one': 1 = 0 * 1 + 1
            # 'million': 1000000 = 1 * 1000000 + 0
            # current = 0; result = 1000000
            # 'two': 2 = 0 * 1 + 2
            # 'thousand': 2000 = 2 * 1000 + 0
            # current = 0; result = 1002000;
            # 'three': 3 = 0 * 1 + 3
            # 'hundred': 300 = 3 * 100 + 0
            # 'and': 300 = 300 * 1 + 0
            # 'forty': 340 = 300 * 1 + 40
            # 'four': 344 = 340 * 1 + 4
            if scale > 100:
                result += current
                current = 0
    # Since current and result are in different states, add both together to get the correct value
    # 1002000 + 344
    return result + current

def _get_restart() -> bool:
    return restart

def _set_restart(set_to: bool) -> None:
    global restart
    restart = set_to

def _check_exit_statements(user_input: str):
    """
    Checks the provided string if it is an exit statement or not then gracefully exit

    This does not check if the string contains the keywords, but if it is entirely the keyword.

    examples:
        "exit()"->triggers sys.exit(0)

        "I want to exit()"->will not trigger

    Args:
        user_input: String to check exit statements for

    Returns:
       Nothing
    """
    l_input = user_input.lower()
    if l_input in exit_statements:
        print("Goodbye!")
        sys.exit(0)

def _check_restart_statements(user_input: str) -> bool:
    """
    Checks the provided string if it is a restart statement or not. The global 'restart' boolean is set to 'True' so
    that state_machine() is aware of the trigger.

    This does not check if the string contains the keywords, but if it is entirely the keyword.

    Args:
        user_input: String to check restart statements for

    Returns:
       boolean if the restart statement was found
    """
    l_input = user_input.lower()
    if l_input in restart_statements:
        _set_restart(True)
        return True
    return False

def _check_invalid_input_count(invalid_count: int):
    """
    Checks invalid_counts value against max_failures to prevent the program for infinite loops.

    If invalid_count >= max_failures the program will gracefully terminate.

    Args:
        invalid_count: int to check if max retries have been hit

    Returns:
       Nothing
    """
    if invalid_count >= max_failures:
        print("Too many failures, sorry")
        _check_exit_statements("exit")