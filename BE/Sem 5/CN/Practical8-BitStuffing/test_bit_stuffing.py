"""
Test script for Bit Stuffing methods
===================================

This script provides unit tests for the Bit Stuffing implementations.
"""

import unittest
from bit_stuffing import BitStuffing, BitStuffingAnalyzer, BitStuffingProtocols


class TestBitStuffing(unittest.TestCase):
    """Test cases for Bit Stuffing."""
    
    def test_initialization(self):
        """Test BitStuffing initialization."""
        bit_stuffing = BitStuffing()
        info = bit_stuffing.get_info()
        
        self.assertEqual(info['flag_pattern'], "01111110")
        self.assertEqual(info['stuffing_pattern'], "11111")
        self.assertEqual(info['stuffing_threshold'], 5)
    
    def test_custom_initialization(self):
        """Test BitStuffing with custom patterns."""
        bit_stuffing = BitStuffing(flag_pattern="01111110", stuffing_pattern="1111")
        info = bit_stuffing.get_info()
        
        self.assertEqual(info['flag_pattern'], "01111110")
        self.assertEqual(info['stuffing_pattern'], "1111")
        self.assertEqual(info['stuffing_threshold'], 4)
    
    def test_invalid_patterns(self):
        """Test initialization with invalid patterns."""
        with self.assertRaises(ValueError):
            BitStuffing(flag_pattern="01111112")  # Invalid binary
        
        with self.assertRaises(ValueError):
            BitStuffing(stuffing_pattern="11112")  # Invalid binary
    
    def test_basic_stuffing(self):
        """Test basic bit stuffing functionality."""
        bit_stuffing = BitStuffing()
        
        # Test data with 5 consecutive 1s
        data = "111110"
        stuffed = bit_stuffing.stuff_data(data)
        expected = "1111100"  # 0 inserted after 5th 1
        
        self.assertEqual(stuffed, expected)
    
    def test_basic_unstuffing(self):
        """Test basic bit unstuffing functionality."""
        bit_stuffing = BitStuffing()
        
        # Test stuffed data
        stuffed_data = "1111100"
        unstuffed = bit_stuffing.unstuff_data(stuffed_data)
        expected = "111110"
        
        self.assertEqual(unstuffed, expected)
    
    def test_stuffing_unstuffing_roundtrip(self):
        """Test that stuffing followed by unstuffing returns original data."""
        bit_stuffing = BitStuffing()
        
        test_cases = [
            "111110",           # Single stuffing opportunity
            "1111111111",       # Multiple stuffing opportunities
            "1010101010",       # No stuffing needed
            "111110111110",     # Multiple sequences
            "01111110111110",   # Mixed pattern
        ]
        
        for data in test_cases:
            stuffed = bit_stuffing.stuff_data(data)
            unstuffed = bit_stuffing.unstuff_data(stuffed)
            self.assertEqual(data, unstuffed, f"Failed for data: {data}")
    
    def test_frame_creation(self):
        """Test frame creation with flags."""
        bit_stuffing = BitStuffing()
        
        data = "111110"
        frame = bit_stuffing.create_frame(data)
        
        # Frame should start and end with flag pattern
        self.assertTrue(frame.startswith("01111110"))
        self.assertTrue(frame.endswith("01111110"))
        
        # Frame should contain stuffed data
        stuffed_data = bit_stuffing.stuff_data(data)
        self.assertIn(stuffed_data, frame)
    
    def test_frame_extraction(self):
        """Test frame extraction."""
        bit_stuffing = BitStuffing()
        
        data = "111110"
        frame = bit_stuffing.create_frame(data)
        extracted = bit_stuffing.extract_frame_data(frame)
        
        self.assertEqual(extracted, data)
    
    def test_frame_creation_extraction_roundtrip(self):
        """Test that frame creation followed by extraction returns original data."""
        bit_stuffing = BitStuffing()
        
        test_cases = [
            "111110",
            "1010101010",
            "1111111111",
            "01111110111110",
        ]
        
        for data in test_cases:
            frame = bit_stuffing.create_frame(data)
            extracted = bit_stuffing.extract_frame_data(frame)
            self.assertEqual(data, extracted, f"Failed for data: {data}")
    
    def test_invalid_frame_extraction(self):
        """Test frame extraction with invalid frames."""
        bit_stuffing = BitStuffing()
        
        # Frame without proper flags
        with self.assertRaises(ValueError):
            bit_stuffing.extract_frame_data("111110")
        
        # Frame with only start flag
        with self.assertRaises(ValueError):
            bit_stuffing.extract_frame_data("01111110111110")
    
    def test_multiple_frames(self):
        """Test finding multiple frames in a bit stream."""
        bit_stuffing = BitStuffing()
        
        # Create multiple frames
        data1 = "111110"
        data2 = "101010"
        data3 = "111111"
        
        frame1 = bit_stuffing.create_frame(data1)
        frame2 = bit_stuffing.create_frame(data2)
        frame3 = bit_stuffing.create_frame(data3)
        
        bit_stream = frame1 + frame2 + frame3
        
        # Find frames
        frames = bit_stuffing.find_frames(bit_stream)
        
        self.assertEqual(len(frames), 3)
        self.assertEqual(frames[0][0], data1)
        self.assertEqual(frames[1][0], data2)
        self.assertEqual(frames[2][0], data3)
    
    def test_invalid_input_stuffing(self):
        """Test stuffing with invalid input."""
        bit_stuffing = BitStuffing()
        
        with self.assertRaises(ValueError):
            bit_stuffing.stuff_data("111112")  # Invalid binary
    
    def test_invalid_input_unstuffing(self):
        """Test unstuffing with invalid input."""
        bit_stuffing = BitStuffing()
        
        with self.assertRaises(ValueError):
            bit_stuffing.unstuff_data("111112")  # Invalid binary
    
    def test_different_stuffing_thresholds(self):
        """Test different stuffing thresholds."""
        # Test with threshold 4
        bit_stuffing_4 = BitStuffing(stuffing_pattern="1111")
        
        data = "11110"
        stuffed = bit_stuffing_4.stuff_data(data)
        expected = "111100"  # 0 inserted after 4th 1
        
        self.assertEqual(stuffed, expected)
        
        # Test with threshold 3
        bit_stuffing_3 = BitStuffing(stuffing_pattern="111")
        
        data = "1110"
        stuffed = bit_stuffing_3.stuff_data(data)
        expected = "11100"  # 0 inserted after 3rd 1
        
        self.assertEqual(stuffed, expected)


class TestBitStuffingAnalyzer(unittest.TestCase):
    """Test cases for Bit Stuffing Analyzer."""
    
    def test_overhead_calculation_no_stuffing(self):
        """Test overhead calculation when no stuffing is needed."""
        data = "1010101010"
        overhead = BitStuffingAnalyzer.calculate_stuffing_overhead(data)
        
        self.assertEqual(overhead['original_length'], 10)
        self.assertEqual(overhead['stuffed_length'], 10)
        self.assertEqual(overhead['overhead_bits'], 0)
        self.assertEqual(overhead['overhead_percentage'], 0.0)
        self.assertEqual(overhead['efficiency'], 1.0)
    
    def test_overhead_calculation_with_stuffing(self):
        """Test overhead calculation when stuffing is needed."""
        data = "111110"  # 5 consecutive 1s
        overhead = BitStuffingAnalyzer.calculate_stuffing_overhead(data, 5)
        
        self.assertEqual(overhead['original_length'], 6)
        self.assertEqual(overhead['stuffed_length'], 7)
        self.assertEqual(overhead['overhead_bits'], 1)
        self.assertAlmostEqual(overhead['overhead_percentage'], 16.67, places=1)
        self.assertAlmostEqual(overhead['efficiency'], 0.857, places=3)
    
    def test_overhead_calculation_multiple_stuffing(self):
        """Test overhead calculation with multiple stuffing opportunities."""
        data = "111110111110"  # Two sequences of 5 consecutive 1s
        overhead = BitStuffingAnalyzer.calculate_stuffing_overhead(data, 5)
        
        self.assertEqual(overhead['original_length'], 12)
        self.assertEqual(overhead['stuffed_length'], 14)
        self.assertEqual(overhead['overhead_bits'], 2)
        self.assertAlmostEqual(overhead['overhead_percentage'], 16.67, places=1)
    
    def test_pattern_analysis(self):
        """Test data pattern analysis."""
        data = "1111101111101010"
        patterns = BitStuffingAnalyzer.analyze_data_patterns(data)
        
        self.assertEqual(patterns['total_sequences'], 2)
        self.assertEqual(patterns['max_consecutive_ones'], 5)
        self.assertAlmostEqual(patterns['avg_consecutive_ones'], 5.0, places=1)
        self.assertEqual(patterns['sequences_requiring_stuffing'], 2)
        self.assertEqual(patterns['consecutive_ones_sequences'], [5, 5])
    
    def test_pattern_analysis_no_ones(self):
        """Test pattern analysis with no consecutive 1s."""
        data = "1010101010"
        patterns = BitStuffingAnalyzer.analyze_data_patterns(data)
        
        self.assertEqual(patterns['total_sequences'], 5)
        self.assertEqual(patterns['max_consecutive_ones'], 1)
        self.assertEqual(patterns['avg_consecutive_ones'], 1.0)
        self.assertEqual(patterns['sequences_requiring_stuffing'], 0)
        self.assertEqual(patterns['consecutive_ones_sequences'], [1, 1, 1, 1, 1])
    
    def test_invalid_input_overhead(self):
        """Test overhead calculation with invalid input."""
        with self.assertRaises(ValueError):
            BitStuffingAnalyzer.calculate_stuffing_overhead("111112")
    
    def test_invalid_input_patterns(self):
        """Test pattern analysis with invalid input."""
        with self.assertRaises(ValueError):
            BitStuffingAnalyzer.analyze_data_patterns("111112")


class TestBitStuffingProtocols(unittest.TestCase):
    """Test cases for Bit Stuffing Protocols."""
    
    def test_standard_protocols(self):
        """Test standard protocols information."""
        protocols = BitStuffingProtocols.get_standard_protocols()
        
        self.assertIn('HDLC', protocols)
        self.assertIn('PPP', protocols)
        self.assertIn('SDLC', protocols)
        self.assertIn('LAPB', protocols)
        
        # Check HDLC protocol
        hdlc = protocols['HDLC']
        self.assertEqual(hdlc['flag_pattern'], '01111110')
        self.assertEqual(hdlc['stuffing_pattern'], '11111')
        self.assertEqual(hdlc['description'], 'High-Level Data Link Control')
    
    def test_protocol_instance_creation(self):
        """Test creating protocol instances."""
        hdlc = BitStuffingProtocols.create_protocol_instance('HDLC')
        
        self.assertIsInstance(hdlc, BitStuffing)
        self.assertEqual(hdlc.flag_pattern, '01111110')
        self.assertEqual(hdlc.stuffing_pattern, '11111')
    
    def test_invalid_protocol(self):
        """Test creating instance with invalid protocol."""
        with self.assertRaises(ValueError):
            BitStuffingProtocols.create_protocol_instance('INVALID')


class TestBitStuffingIntegration(unittest.TestCase):
    """Integration tests for Bit Stuffing."""
    
    def test_complete_workflow(self):
        """Test complete stuffing -> framing -> extraction -> unstuffing workflow."""
        bit_stuffing = BitStuffing()
        
        test_cases = [
            "111110",
            "1010101010",
            "1111111111",
            "01111110111110",
            "110111110111110",
        ]
        
        for data in test_cases:
            # Stuff data
            stuffed = bit_stuffing.stuff_data(data)
            
            # Create frame
            frame = bit_stuffing.create_frame(data)
            
            # Extract from frame
            extracted = bit_stuffing.extract_frame_data(frame)
            
            # Verify
            self.assertEqual(extracted, data, f"Failed for data: {data}")
    
    def test_multiple_frames_workflow(self):
        """Test workflow with multiple frames."""
        bit_stuffing = BitStuffing()
        
        # Create multiple frames
        frames_data = ["111110", "101010", "111111"]
        frames = [bit_stuffing.create_frame(data) for data in frames_data]
        bit_stream = ''.join(frames)
        
        # Find and extract frames
        found_frames = bit_stuffing.find_frames(bit_stream)
        
        self.assertEqual(len(found_frames), 3)
        for i, (frame_data, start, end) in enumerate(found_frames):
            self.assertEqual(frame_data, frames_data[i])
    
    def test_different_protocols_workflow(self):
        """Test workflow with different protocols."""
        protocols = ['HDLC', 'PPP', 'SDLC', 'LAPB']
        test_data = "111110"
        
        for protocol in protocols:
            bit_stuffing = BitStuffingProtocols.create_protocol_instance(protocol)
            
            # Test complete workflow
            stuffed = bit_stuffing.stuff_data(test_data)
            frame = bit_stuffing.create_frame(test_data)
            extracted = bit_stuffing.extract_frame_data(frame)
            
            self.assertEqual(extracted, test_data, f"Failed for protocol: {protocol}")


def run_quick_demo():
    """Run a quick demonstration of the Bit Stuffing methods."""
    print("QUICK BIT STUFFING DEMONSTRATION")
    print("===============================")
    
    # Test basic bit stuffing
    print("\n1. Basic Bit Stuffing:")
    bit_stuffing = BitStuffing()
    data = "111110"
    stuffed = bit_stuffing.stuff_data(data)
    unstuffed = bit_stuffing.unstuff_data(stuffed)
    
    print(f"   Original data: {data}")
    print(f"   Stuffed data: {stuffed}")
    print(f"   Unstuffed data: {unstuffed}")
    print(f"   Data matches: {'Yes' if data == unstuffed else 'No'}")
    
    # Test frame creation
    print("\n2. Frame Creation:")
    frame = bit_stuffing.create_frame(data)
    extracted = bit_stuffing.extract_frame_data(frame)
    
    print(f"   Original data: {data}")
    print(f"   Frame: {frame}")
    print(f"   Extracted data: {extracted}")
    print(f"   Data matches: {'Yes' if data == extracted else 'No'}")
    
    # Test overhead analysis
    print("\n3. Overhead Analysis:")
    overhead = BitStuffingAnalyzer.calculate_stuffing_overhead(data)
    print(f"   Original length: {overhead['original_length']} bits")
    print(f"   Stuffed length: {overhead['stuffed_length']} bits")
    print(f"   Overhead: {overhead['overhead_bits']} bits ({overhead['overhead_percentage']:.1f}%)")
    print(f"   Efficiency: {overhead['efficiency']:.3f}")


if __name__ == "__main__":
    # Run quick demo
    run_quick_demo()
    
    # Run unit tests
    print("\n" + "="*60)
    print("RUNNING UNIT TESTS")
    print("="*60)
    unittest.main(argv=[''], exit=False, verbosity=2)
