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
        # Extract tap bits (0-indexed): 31, 21, 1, 0
        bit31 = (state >> 31) & 1
        bit21 = (state >> 21) & 1
        bit1  = (state >> 1) & 1
        bit0  = (state >> 0) & 1
        # XOR the tap bits to get the feedback bit
        feedback = bit31 ^ bit21 ^ bit1 ^ bit0
        # Shift state right by 1
        next_state = state >> 1
        # Insert feedback at the MSB (bit 31)
        next_state = (feedback << 31) | next_state
        # Mask to 32 bits
        return next_state & 0xFFFFFFFF
    
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
        # Get the next pseudo-random 32-bit value
        rand_val = self._next()
        # Map it to the desired range using modulo
        range_size = max_val - min_val + 1
        return min_val + (rand_val % range_size)
