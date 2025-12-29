"""
Dreidel spinner using LFSR-based random number generation.
"""
from lfsr import LFSR32


class Dreidel:
    """
    A dreidel spinner that generates random faces using LFSR.
    
    The four faces are:
    - Nun (נ) - "Nisht" (nothing)
    - Gimel (ג) - "Gantz" (all)
    - Hey (ה) - "Halb" (half)
    - Shin (ש) - "Shtel" (put in)
    """
    
    FACES = ("Nun", "Gimel", "Hey", "Shin")
    
    def __init__(self, seed: int = 1):
        """
        Initialize the dreidel with a seed for the random generator.
        
        Args:
            seed: Seed value for the LFSR (must be non-zero).
        """
        self._lfsr = LFSR32(seed)
    
    def spin(self) -> str:
        """
        Spin the dreidel and return the face it lands on.
        
        Returns:
            One of: "Nun", "Gimel", "Hey", "Shin"
        """
        # TODO: Implement spin using self._lfsr.random_int()

        index = self._lfsr.random_int(0, 3)
        return self.FACES[index]