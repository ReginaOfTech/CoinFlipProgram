####################################################################
# flipit_objects/default_objects.py
# Purpose: Contains the object classes that are created by default or custom objects
####################################################################
from flipit_objects.base_object import BaseObject, IllegalBaseObject

class UserCreated(BaseObject):
    def __init__(self) -> None:
        super().__init__()

    # Overrides of BaseObject attributes
    @property
    def sides(self)->int:
        return self._sides

    @sides.setter
    def sides(self, sides:int) -> None:
        self._sides = sides

    @property
    def is_weighted(self)->bool:
        return self._is_weighted

    @is_weighted.setter
    def is_weighted(self, is_weighted:bool) -> None:
        self._is_weighted = is_weighted

    @property
    def weighted_side(self):
        return self._weighted_side

    @weighted_side.setter
    def weighted_side(self, weighted_side:int) -> None:
        self._weighted_side = weighted_side

#----------------COINS------------------
class ClassicCoin(BaseObject):
    def __init__(self) -> None:
        super().__init__(2)

class IllegalCoin(IllegalBaseObject):
    def __init__(self) -> None:
        super().__init__(2, 2)

#--------------CLASSIC DICE-----------------
class ClassicDice(BaseObject):
    def __init__(self) -> None:
        super().__init__(6)

class IllegalDice(IllegalBaseObject):
    def __init__(self) -> None:
        super().__init__(6, 4)
