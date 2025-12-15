"""
Pytest tests for the LFSR32 class - testing public API and random properties.
"""
import sys
import os

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

import pytest
from lfsr import LFSR32


class TestRandomIntBasic:
    """Basic tests for the random_int public method."""
    
    def test_zero_seed_raises_error(self):
        """Test that zero seed raises ValueError."""
        with pytest.raises(ValueError, match="Seed must be non-zero"):
            LFSR32(seed=0)
    
    def test_random_int_within_default_range(self):
        """Test random_int with default range stays within bounds."""
        lfsr = LFSR32(seed=42)
        value = lfsr.random_int()
        assert 0 <= value <= 0xFFFFFFFF
    
    def test_random_int_within_custom_range(self):
        """Test random_int respects custom min/max bounds."""
        lfsr = LFSR32(seed=42)
        
        for _ in range(100):
            value = lfsr.random_int(min_val=1, max_val=100)
            assert 1 <= value <= 100
    
    def test_random_int_single_value_range(self):
        """Test random_int when min equals max."""
        lfsr = LFSR32(seed=42)
        value = lfsr.random_int(min_val=50, max_val=50)
        assert value == 50
    
    def test_random_int_negative_range(self):
        """Test random_int with negative values."""
        lfsr = LFSR32(seed=42)
        
        for _ in range(100):
            value = lfsr.random_int(min_val=-10, max_val=10)
            assert -10 <= value <= 10


class TestRandomProperties:
    """Tests for statistical/random properties of the LFSR."""
    
    def test_deterministic_with_same_seed(self):
        """Test that same seed produces same sequence."""
        lfsr1 = LFSR32(seed=12345)
        lfsr2 = LFSR32(seed=12345)
        
        for _ in range(100):
            assert lfsr1.random_int() == lfsr2.random_int()
    
    def test_different_seeds_different_sequences(self):
        """Test that different seeds produce different sequences."""
        lfsr1 = LFSR32(seed=1)
        lfsr2 = LFSR32(seed=2)
        
        seq1 = [lfsr1.random_int() for _ in range(10)]
        seq2 = [lfsr2.random_int() for _ in range(10)]
        
        assert seq1 != seq2
    
    def test_uniform_distribution(self):
        """Test that output is roughly uniformly distributed."""
        lfsr = LFSR32(seed=12345)
        num_samples = 10000
        num_buckets = 10
        
        values = [lfsr.random_int(0, num_buckets - 1) for _ in range(num_samples)]
        
        # Count occurrences in each bucket
        counts = [values.count(i) for i in range(num_buckets)]
        
        # Each bucket should have roughly num_samples / num_buckets occurrences
        expected = num_samples / num_buckets
        
        # Allow 20% deviation from expected (reasonable for pseudo-random)
        for count in counts:
            assert expected * 0.8 <= count <= expected * 1.2
    
    def test_all_values_in_range_hit(self):
        """Test that all values in a small range are eventually hit."""
        lfsr = LFSR32(seed=42)
        values = set()
        
        # Generate enough samples to hit all values 1-10
        for _ in range(1000):
            values.add(lfsr.random_int(1, 10))
        
        # Should hit all 10 values
        assert values == set(range(1, 11))
    
    def test_no_obvious_patterns(self):
        """Test that consecutive values don't show obvious patterns."""
        lfsr = LFSR32(seed=42)
        values = [lfsr.random_int(0, 100) for _ in range(1000)]
        
        # Check that consecutive values are not always the same
        consecutive_same = sum(1 for i in range(len(values) - 1) if values[i] == values[i + 1])
        
        # With range 0-100, expect ~1% consecutive matches by chance
        # Allow up to 5% as reasonable threshold
        assert consecutive_same < len(values) * 0.05
    
    def test_sequence_varies_over_time(self):
        """Test that the generator doesn't get stuck in short cycles."""
        lfsr = LFSR32(seed=42)
        
        # Generate values and check for variety
        values = [lfsr.random_int() for _ in range(1000)]
        unique_values = set(values)
        
        # Should have high variety (at least 90% unique in 1000 samples)
        assert len(unique_values) >= 900
    
    def test_chi_squared_uniformity(self):
        """Chi-squared test for uniformity of distribution."""
        lfsr = LFSR32(seed=98765)
        num_samples = 10000
        num_categories = 6  # Like a die
        
        observed = [0] * num_categories
        for _ in range(num_samples):
            observed[lfsr.random_int(0, num_categories - 1)] += 1
        
        expected = num_samples / num_categories
        
        # Calculate chi-squared statistic
        chi_squared = sum((obs - expected) ** 2 / expected for obs in observed)
        
        # For 5 degrees of freedom, critical value at p=0.05 is ~11.07
        # We use a more lenient threshold for pseudo-random generators
        assert chi_squared < 15
    
    def test_mean_approximates_midpoint(self):
        """Test that mean of generated values approximates range midpoint."""
        lfsr = LFSR32(seed=54321)
        min_val, max_val = 0, 100
        num_samples = 10000
        
        values = [lfsr.random_int(min_val, max_val) for _ in range(num_samples)]
        mean = sum(values) / len(values)
        
        expected_mean = (min_val + max_val) / 2
        
        # Mean should be within 5% of expected
        assert abs(mean - expected_mean) < expected_mean * 0.05
