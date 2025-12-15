"""
Pytest tests for the Dreidel class - testing spin functionality and fair distribution.
"""
import sys
import os

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

import pytest
from dreidel import Dreidel


class TestDreidelBasic:
    """Basic tests for the Dreidel class."""
    
    def test_zero_seed_raises_error(self):
        """Test that zero seed raises ValueError."""
        with pytest.raises(ValueError, match="Seed must be non-zero"):
            Dreidel(seed=0)
    
    def test_spin_returns_valid_face(self):
        """Test that spin returns one of the four valid faces."""
        dreidel = Dreidel(seed=42)
        
        for _ in range(100):
            face = dreidel.spin()
            assert face in ("Nun", "Gimel", "Hey", "Shin")
    
    def test_deterministic_with_same_seed(self):
        """Test that same seed produces same sequence of spins."""
        dreidel1 = Dreidel(seed=12345)
        dreidel2 = Dreidel(seed=12345)
        
        for _ in range(100):
            assert dreidel1.spin() == dreidel2.spin()
    
    def test_different_seeds_different_sequences(self):
        """Test that different seeds produce different sequences."""
        dreidel1 = Dreidel(seed=1)
        dreidel2 = Dreidel(seed=2)
        
        seq1 = [dreidel1.spin() for _ in range(20)]
        seq2 = [dreidel2.spin() for _ in range(20)]
        
        assert seq1 != seq2


class TestDreidelFairDistribution:
    """Tests for fair distribution of dreidel faces."""
    
    def test_all_faces_appear(self):
        """Test that all four faces appear in a reasonable number of spins."""
        dreidel = Dreidel(seed=42)
        faces_seen = set()
        
        for _ in range(100):
            faces_seen.add(dreidel.spin())
        
        assert faces_seen == {"Nun", "Gimel", "Hey", "Shin"}
    
    def test_uniform_distribution(self):
        """Test that each face appears with roughly equal probability (25%)."""
        dreidel = Dreidel(seed=12345)
        num_spins = 10000
        
        counts = {"Nun": 0, "Gimel": 0, "Hey": 0, "Shin": 0}
        for _ in range(num_spins):
            counts[dreidel.spin()] += 1
        
        expected = num_spins / 4  # 2500 each
        
        # Each face should be within 10% of expected
        for face, count in counts.items():
            assert expected * 0.9 <= count <= expected * 1.1, \
                f"{face} count {count} is outside expected range [{expected * 0.9}, {expected * 1.1}]"
    
    def test_chi_squared_fairness(self):
        """Chi-squared test for uniform distribution of faces."""
        dreidel = Dreidel(seed=98765)
        num_spins = 10000
        
        counts = {"Nun": 0, "Gimel": 0, "Hey": 0, "Shin": 0}
        for _ in range(num_spins):
            counts[dreidel.spin()] += 1
        
        expected = num_spins / 4
        
        # Calculate chi-squared statistic
        chi_squared = sum((count - expected) ** 2 / expected for count in counts.values())
        
        # For 3 degrees of freedom, critical value at p=0.05 is ~7.81
        # Using lenient threshold for pseudo-random generator
        assert chi_squared < 10, f"Chi-squared {chi_squared} exceeds threshold"
    
    def test_no_face_dominates(self):
        """Test that no single face appears more than 35% of the time."""
        dreidel = Dreidel(seed=54321)
        num_spins = 5000
        
        counts = {"Nun": 0, "Gimel": 0, "Hey": 0, "Shin": 0}
        for _ in range(num_spins):
            counts[dreidel.spin()] += 1
        
        max_count = max(counts.values())
        max_percentage = max_count / num_spins
        
        assert max_percentage < 0.35, f"A face appeared {max_percentage * 100:.1f}% of the time"
    
    def test_no_face_underrepresented(self):
        """Test that no single face appears less than 15% of the time."""
        dreidel = Dreidel(seed=11111)
        num_spins = 5000
        
        counts = {"Nun": 0, "Gimel": 0, "Hey": 0, "Shin": 0}
        for _ in range(num_spins):
            counts[dreidel.spin()] += 1
        
        min_count = min(counts.values())
        min_percentage = min_count / num_spins
        
        assert min_percentage > 0.15, f"A face appeared only {min_percentage * 100:.1f}% of the time"
    
    def test_distribution_across_multiple_seeds(self):
        """Test fair distribution holds across different seeds."""
        seeds = [1, 100, 9999, 0xDEAD, 0xBEEF]
        
        for seed in seeds:
            dreidel = Dreidel(seed=seed)
            counts = {"Nun": 0, "Gimel": 0, "Hey": 0, "Shin": 0}
            
            for _ in range(4000):
                counts[dreidel.spin()] += 1
            
            expected = 1000  # 4000 / 4
            
            # Each face should be within 20% of expected
            for face, count in counts.items():
                assert expected * 0.8 <= count <= expected * 1.2, \
                    f"Seed {seed}: {face} count {count} outside expected range"
