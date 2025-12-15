# RandomDreidel

A programming assignment to implement a pseudo-random dreidel spinner using a Linear Feedback Shift Register (LFSR).

## Overview

In this assignment, you will implement a 32-bit LFSR to generate pseudo-random numbers and use it to simulate spinning a dreidel.

## Background

### What is an LFSR?

A Linear Feedback Shift Register (LFSR) is a shift register whose input bit is a linear function (XOR) of its previous state. LFSRs can produce sequences of pseudo-random numbers with a very long period.

### The Dreidel

A dreidel is a four-sided spinning top with Hebrew letters on each face:
- **Nun (נ)** - "Nisht" (nothing happens)
- **Gimel (ג)** - "Gantz" (take all)
- **Hey (ה)** - "Halb" (take half)
- **Shin (ש)** - "Shtel" (put in)

## Your Task

You need to implement three functions:

### 1. `LFSR32._lfsr32(state)` in `src/lfsr.py`

Implement a single step of a 32-bit LFSR using the polynomial: **x³² + x²² + x² + x¹ + 1**

This means you need to:
1. Calculate the feedback bit by XORing bits at positions 32, 22, 2, and 1 (1-indexed)
2. Shift the register right by 1
3. Insert the feedback bit at the most significant bit (MSB)

**Hints:**
- Use bit positions 31, 21, 1, 0 (0-indexed) for the XOR taps
- Use bitwise operations: `>>`, `<<`, `^`, `&`, `|`
- Mask the result to 32 bits using `& 0xFFFFFFFF`

### 2. `LFSR32.random_int(min_val, max_val)` in `src/lfsr.py`

Generate a random integer in the range [min_val, max_val] (inclusive).

**Hints:**
- Use `self._next()` to get the next random 32-bit value
- Use modulo to constrain the range

### 3. `Dreidel.spin()` in `src/dreidel.py`

Return a random dreidel face using the LFSR.

**Hints:**
- Use `self._lfsr.random_int()` to generate a random index
- Return the corresponding face from `self.FACES`

## Project Structure

```
RandomDreidel/
├── src/
│   ├── lfsr.py      # LFSR32 class (implement _lfsr32, random_int)
│   └── dreidel.py   # Dreidel class (implement spin)
├── tests/
│   ├── test_lfsr.py     # Tests for LFSR implementation
│   └── test_dreidel.py  # Tests for Dreidel implementation
└── README.md
```

## Running Tests

To verify your implementation, run the tests using pytest:

```bash
# Run all tests
pytest tests/ -v

# Run only LFSR tests
pytest tests/test_lfsr.py -v

# Run only Dreidel tests
pytest tests/test_dreidel.py -v
```

All tests should pass when your implementation is correct.

Good luck and happy spinning! 🎲
