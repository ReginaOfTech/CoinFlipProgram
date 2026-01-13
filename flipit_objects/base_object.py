####################################################################
# flipit_objects/base_object.py
# Purpose: Contains classes to be inherited that created objects should inherit
####################################################################
import random
import sys

class BaseObject:
    """
    Base class for all objects that the program will 'roll'

    If an error occurs the program will display an error message then gracefully exit. Check all parameters before creating object.

    Args:
        sides: int of sides of the object. Errors out if <=0 or not a whole number.
        weighted: bool of the object is weighted
        weighted_side: int of side that is weighted. Errors out if <=0, > sides, or not a whole number.
    """
    def __init__(self, sides=1, weighted=False, weighted_side=0) -> None:
        # values should be checked before creating object, but just incase lets check the values
        try:
            if sides <= 0:
                raise ValueError("ERROR: BaseObject sides must be greater than 0")
            if sides%1 != 0: # Check that a whole number is provided
                raise ValueError("ERROR: BaseObject sides must be a whole integer")
            if weighted:
                if weighted_side <= 0:
                    raise ValueError("ERROR: BaseObject is weighted, but a weighted_side has not been designated")
                if weighted_side > sides:
                    raise ValueError("ERROR: BaseObject is weighted, but the weighted side is greater than the number of sides.")
                if weighted_side%1 != 0:
                    raise ValueError("ERROR: BaseObject weighted_sides must be a whole positive integer")
            if not weighted and weighted_side > 0:
                print("WARNING: Object is not weighted, but a weighted side has been designated. Setting weighted_side to 0.")
                weighted_side = 0
        except ValueError as e:
            print(e)
            sys.exit(1)
        self._sides = sides  # Store value in internal attribute
        self._is_weighted = weighted
        self._weighted_side = weighted_side

    @property
    def sides(self)->int:
        return self._sides

    @property
    def is_weighted(self)->bool:
        return self._is_weighted

    @property
    def weighted_side(self)->int:
        return self._weighted_side

    def roll(self, num_rolls:int) -> list:
        """
        'Rolls' the created object using the provided internal attributes

        Args:
            num_rolls: int number of times to 'roll' the object

        Returns:
           list[int] of the sides that the object landed on for the roll that is the length of num_rolls
        """
        roll_results = []
        if not self.is_weighted:
            # Roll the object num_rolls times landing on any side since this is an unweighted object
            for _ in range(num_rolls):
                roll = random.randint(1, self._sides)
                # Store the new roll in the return variable
                roll_results.append(roll)
        else:
            # Since this object is weighted another approach is needed
            # The values of the sides is needed to provided for the 'random' selection
            faces = list(range(1, self._sides+1))
            # designates the likelihood that each sides will be 'rolled'
            minimum_weight = 1/self._sides
            # since the total of the weights do not have to equal 1 default to 0.1 if sides > 10
            if len(faces) > 10:
                minimum_weight = 0.1
            weights = [minimum_weight] * len(faces)
            # The weighted side is 5x more likely to be selected
            weights[self._weighted_side - 1] = minimum_weight * 5
            # random.choices will roll the object num_roll times using the provided weights
            roll_results = random.choices(faces, weights=weights, k=num_rolls)
        return roll_results

class IllegalBaseObject(BaseObject):
    """
    Base class for all illegal (ie weighted) objects that the program will 'roll'

    If an error occurs the program will display an error message then gracefully exit. Check all parameters before creating object.

    Args:
        sides: int of sides of the object. Errors out if <=0 or not a whole number.
        weighted_side: int of side that is weighted. Errors out if <=0, > sides, or not a whole number.
    """
    def __init__(self, sides, weighted_side) -> None:
        super().__init__(sides, True, weighted_side)

    @property
    def weighted_side(self) -> int:
        return self._weighted_side

    @weighted_side.setter
    def weighted_side(self, weighted_side:int) -> None:
        try:
            if 0 < weighted_side <= self._sides:
                self._weighted_side = weighted_side
            else:
                raise ValueError(f"ERROR: BaseObject weighted_side must be a whole positive integer less than {self.sides}")
        except ValueError as e:
            print(e)