class LFSR32:

    
    def __init__(self, seed: int = 1):
        if seed == 0:
            raise ValueError("Seed must be non-zero for LFSR to function properly")
        self._state = seed & 0xFFFFFFFF
    
    @staticmethod
    def _lfsr32(state: int) -> int:
        b31 = (state >> 31) & 1
        b21 = (state >> 21) & 1
        b1  = (state >> 1) & 1
        b0  = state & 1
        new_bit = b31 ^ b21 ^ b1 ^ b0
        state = state >> 1
        state = state | (new_bit << 31)

        return state & 0xFFFFFFFF
    
    def _next(self) -> int:

        self._state = self._lfsr32(self._state)
        return self._state
    
    def random_int(self, min_val: int = 0, max_val: int = 0xFFFFFFFF) -> int:
        range = max_val - min_val + 1
        random_num_in_range = self._next() % range

        return min_val + random_num_in_range