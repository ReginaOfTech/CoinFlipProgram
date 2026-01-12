from FlipItObjects.BaseObject import BaseObject

class UserCreated(BaseObject):
    def __init__(self) -> None:
        super().__init__()

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

class ClassicCoin(BaseObject):
    def __init__(self) -> None:
        super().__init__(2)

class IllegalCoin(BaseObject):
    def __init__(self) -> None:
        super().__init__(2, True, 1)

class ClassicDice(BaseObject):
    def __init__(self) -> None:
        super().__init__(6)

class IllegalDice(BaseObject):
    def __init__(self) -> None:
        super().__init__(6, True, 4)