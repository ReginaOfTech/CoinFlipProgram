import pytest

import input_helpers as helpers
from flipit_objects import default_objects
from flipit_objects.base_object import BaseObject


# Ensure that natural language to digits functions as expected
def test_text2int():
    tests = {"one hundred and thirty-two": 132, #pass
             "1":-1, #fail due to being a number
             "132":-1, #fail due to being a number
             "one": 1, #pass
             "twenty":20, #pass
             "one million three hundred and four thousand two hundred and thirty":1304230, #pass
             "one trillion 40 thousand":-1} #fail due to 40
    for _ in tests:
        ans = helpers._text2int(_)
        assert ans == tests[_]

# Make sure that the bare minimum to exit the program is still present
def test_exit_statements():
    tests = {"exit()":True,
             "exit":True,
             "Let's leave":False,
             "ex":True}
    for _ in tests:
        present = _ in helpers.exit_statements
        assert present == tests[_]
    #With the proper one sysexit(0) should be hit
    with pytest.raises(SystemExit) as excinfo:
        first_key = list(tests)[0]
        helpers._check_exit_statements(first_key)
    assert excinfo.value.code == 0

#Make sure that the bare minimum to restart the program is still present
def test_restart_statements():
    tests = {"restart()":True,
             "restart": True,
             "Try another":False,
             "rstart":True}
    for _ in tests:
        rest = helpers._check_restart_statements(_)
        assert rest == tests[_]
        #Ensure that input_helpers.restart is being set if True
        assert helpers._get_restart() == tests[_]
        #Reset restart to False for following tests
        helpers._set_restart(False)

#Make sure that the bare minimum for 'yes' and 'no' inputs are present
def test_yes_no_input():
    y_present = "yes" in helpers.yes_statements
    n_present = "no" in helpers.no_statements
    assert y_present == True
    assert n_present == True

#BaseObject rejects improper values
def test_base_object(capsys):
    obj = BaseObject()
    assert obj.sides == 1
    assert obj.is_weighted == False
    assert obj.weighted_side == 0
    sides = {0: "ERROR: BaseObject sides must be greater than 0\n", #sides != 0
             -1:"ERROR: BaseObject sides must be greater than 0\n", #sides > 0
             0.5:"ERROR: BaseObject sides must be a whole integer\n"} #sides%1==0
    for _ in sides:
        with pytest.raises(SystemExit) as excinfo:
            obj = BaseObject(sides=_)
        out, err = capsys.readouterr()
        assert out == sides[_]
    #if weighted == False and weighted_side > 0 then exit
    obj = BaseObject(weighted_side=4)
    out, err = capsys.readouterr()
    assert out == "WARNING: Object is not weighted, but a weighted side has been designated. Setting weighted_side to 0.\n"
    #if weighted then make sure weighted_side is checked properly
    weighted_side = {0:"ERROR: BaseObject is weighted, but a weighted_side has not been designated\n", #weighted_side == 0
                    -1:"ERROR: BaseObject is weighted, but a weighted_side has not been designated\n", #weighted_side < 0
                     2:"ERROR: BaseObject is weighted, but the weighted side is greater than the number of sides.\n", #weighted_side > _sides
                     0.75:"ERROR: BaseObject weighted_sides must be a whole positive integer\n"} #weighted_side%1 != 0
    for _ in weighted_side:
        with pytest.raises(SystemExit) as excinfo:
            obj = BaseObject(weighted=True, weighted_side=_)
        out, err = capsys.readouterr()
        assert out == weighted_side[_]

#Check UserCreated default object
def test_default_objects_user_created():
    obj = default_objects.UserCreated()
    # Expected default values in BaseObject are still set
    assert obj.sides == 1
    assert obj.is_weighted == False
    assert obj.weighted_side == 0
    # Internal attributes are still overwritten
    sides = 546
    is_weighted = True
    weighted_side = 250
    obj.sides = sides
    obj.is_weighted = is_weighted
    obj.weighted_side = weighted_side
    assert obj.sides == sides
    assert obj.weighted_side == weighted_side
    assert obj.is_weighted == is_weighted

#Check that default object values have not been changed from expected
def test_default_objects_coin():
    coin_side = 2
    false_weighted_side = 0
    true_weighted_side = 2
    #-----------Legal-----------------
    obj = default_objects.ClassicCoin()
    assert obj.sides == coin_side
    assert obj.is_weighted == False
    assert obj.weighted_side == false_weighted_side
    #-----------Illegal--------------
    obj = default_objects.IllegalCoin()
    assert obj.sides == coin_side
    assert obj.is_weighted == True
    assert obj.weighted_side == true_weighted_side
    #Weighted side is still overwritten
    obj.weighted_side = 1
    assert obj.weighted_side == 1
    #Fails if weighted_side is greater than sides
    obj.weighted_side = coin_side + 1
    # weighted_side should not have changed due to raising ValueError
    assert obj.weighted_side == 1

def test_default_objects_dice():
    dice_side = 6
    false_weighted_side = 0
    true_weighted_side = 2
    # -----------Legal-----------------
    obj = default_objects.ClassicDice()
    assert obj.sides == dice_side
    assert obj.is_weighted == False
    assert obj.weighted_side == false_weighted_side
    # -----------Illegal--------------
    obj = default_objects.IllegalDice()
    assert obj.sides == dice_side
    assert obj.is_weighted == True
    assert obj.weighted_side == 4
    # Weighted side is still overwritten
    obj.weighted_side = true_weighted_side
    assert obj.weighted_side == true_weighted_side
