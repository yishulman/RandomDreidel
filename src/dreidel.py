from lfsr import LFSR32


class Dreidel:

    FACES = ("Nun", "Gimel", "Hey", "Shin")
    
    def __init__(self, seed: int = 1):
        self._lfsr = LFSR32(seed)
    
    def spin(self) -> str:
        random_num = self._lfsr.random_int(0, 3)
        return Dreidel.FACES[random_num]

