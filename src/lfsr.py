"""
32-bit Linear Feedback Shift Register (LFSR) implementation.

This module provides a maximal-length 32-bit LFSR using the polynomial:
x^32 + x^22 + x^2 + x^1 + 1

This configuration produces a sequence with period 2^32 - 1.
"""


class LFSR32:
    """
    A 32-bit Linear Feedback Shift Register class.
    
    Provides a pseudo-random number generator using a maximal-length LFSR.
    """
    
    def __init__(self, seed: int = 1):
        """
        Initialize the LFSR with a seed value.
        
        Args:
            seed: Initial state (must be non-zero). Defaults to 1.
        
        Raises:
            ValueError: If seed is zero.
        """
        if seed == 0:
            raise ValueError("Seed must be non-zero for LFSR to function properly")
        self._state = seed & 0xFFFFFFFF
    
    @staticmethod
    def _lfsr32(state: int) -> int:
        """
        Perform one step of a 32-bit LFSR.
        
        Uses taps at positions 32, 22, 2, 1 (1-indexed) for maximal length sequence.
        Polynomial: x^32 + x^22 + x^2 + x^1 + 1
        
        Args:
            state: Current state of the LFSR (32-bit unsigned integer).
                  Must be non-zero for proper operation.
        
        Returns:
            Next state of the LFSR (32-bit unsigned integer).
        """
        # TODO: Implement LFSR step
        fb = ((state >> 31) & 1) ^ ((state >> 21) & 1) ^ ((state >> 1) & 1) ^ ((state >> 0) & 1)  # XOR calculation for the feedback bit
        next_state = state >> 1 | (fb << 31) # shift right and insert feedback bit at MSB
        return next_state & 0xFFFFFFFF # clearing bits upper than 32 bits
        # Hint: XOR taps at positions 32, 22, 2, 1 (0-indexed: 31, 21, 1, 0)
        # Shift right and insert feedback bit at MSB
        raise NotImplementedError("Students must implement _lfsr32")
    
    def _next(self) -> int:
        """
        Advance the LFSR by one step and return the new state.
        
        Returns:
            The next 32-bit pseudo-random value.
        """
        self._state = self._lfsr32(self._state)
        return self._state
    
    def random_int(self, min_val: int = 0, max_val: int = 0xFFFFFFFF) -> int:
        """
        Generate a random integer in the specified range [min_val, max_val].
        
        Args:
            min_val: Minimum value (inclusive). Defaults to 0.
            max_val: Maximum value (inclusive). Defaults to 0xFFFFFFFF.
        
        Returns:
            A pseudo-random integer in the specified range.
        """
        # TODO: Implement random integer generation using _next()
        scale = max_val - min_val + 1 # range size
        random_value = self._next() % scale + min_val # give random number in scale
        return random_value
        raise NotImplementedError("Students must implement random_int")
