from typing import List, Tuple, Union
import re


class BitStuffing:
    """
    Bit Stuffing implementation for data link layer protocols.
    
    Provides methods for bit stuffing and unstuffing to ensure proper
    frame synchronization and data transparency.
    """
    
    def __init__(self, flag_pattern: str = "01111110", stuffing_pattern: str = "11111"):
        """
        Initialize Bit Stuffing with specified patterns.
        
        Args:
            flag_pattern (str): Flag pattern used for frame delimiters (default: "01111110")
            stuffing_pattern (str): Pattern that triggers stuffing (default: "11111")
        """
        self.flag_pattern = flag_pattern
        self.stuffing_pattern = stuffing_pattern
        
        # Validate patterns
        if not self._is_valid_binary_pattern(flag_pattern):
            raise ValueError("Flag pattern must contain only binary digits (0 and 1)")
        if not self._is_valid_binary_pattern(stuffing_pattern):
            raise ValueError("Stuffing pattern must contain only binary digits (0 and 1)")
        
        # Calculate stuffing threshold (number of consecutive 1s that trigger stuffing)
        self.stuffing_threshold = len(stuffing_pattern)
    
    def _is_valid_binary_pattern(self, pattern: str) -> bool:
        """Check if pattern contains only binary digits."""
        return all(bit in '01' for bit in pattern)
    
    def stuff_data(self, data: str) -> str:
        """
        Perform bit stuffing on the data.
        
        Args:
            data (str): Binary string data to be stuffed
            
        Returns:
            str: Data with bit stuffing applied
        """
        if not self._is_valid_binary_pattern(data):
            raise ValueError("Data must contain only binary digits (0 and 1)")
        
        stuffed_data = ""
        consecutive_ones = 0
        
        for bit in data:
            stuffed_data += bit
            
            if bit == '1':
                consecutive_ones += 1
                # If we have reached the stuffing threshold, add a 0
                if consecutive_ones == self.stuffing_threshold:
                    stuffed_data += '0'
                    consecutive_ones = 0
            else:
                consecutive_ones = 0
        
        return stuffed_data
    
    def unstuff_data(self, stuffed_data: str) -> str:
        """
        Remove bit stuffing from the data.
        
        Args:
            stuffed_data (str): Binary string data with bit stuffing
            
        Returns:
            str: Original data with stuffing removed
        """
        if not self._is_valid_binary_pattern(stuffed_data):
            raise ValueError("Stuffed data must contain only binary digits (0 and 1)")
        
        unstuffed_data = ""
        consecutive_ones = 0
        
        for bit in stuffed_data:
            if bit == '1':
                consecutive_ones += 1
                unstuffed_data += bit
            else:
                # If we have exactly stuffing_threshold consecutive 1s followed by 0,
                # this is a stuffed bit, so we skip the 0
                if consecutive_ones == self.stuffing_threshold:
                    consecutive_ones = 0
                    # Skip this 0 (it's a stuffed bit)
                else:
                    unstuffed_data += bit
                    consecutive_ones = 0
        
        return unstuffed_data
    
    def create_frame(self, data: str) -> str:
        """
        Create a complete frame with flags and stuffed data.
        
        Args:
            data (str): Binary string data to be framed
            
        Returns:
            str: Complete frame with flags and stuffed data
        """
        if not self._is_valid_binary_pattern(data):
            raise ValueError("Data must contain only binary digits (0 and 1)")
        
        # Stuff the data
        stuffed_data = self.stuff_data(data)
        
        # Create frame: flag + stuffed_data + flag
        frame = self.flag_pattern + stuffed_data + self.flag_pattern
        
        return frame
    
    def extract_frame_data(self, frame: str) -> str:
        """
        Extract and unstuff data from a complete frame.
        
        Args:
            frame (str): Complete frame with flags and stuffed data
            
        Returns:
            str: Original data extracted from frame
        """
        if not self._is_valid_binary_pattern(frame):
            raise ValueError("Frame must contain only binary digits (0 and 1)")
        
        # Check if frame starts and ends with flag pattern
        if not frame.startswith(self.flag_pattern) or not frame.endswith(self.flag_pattern):
            raise ValueError("Frame must start and end with flag pattern")
        
        # Extract stuffed data (remove flags)
        stuffed_data = frame[len(self.flag_pattern):-len(self.flag_pattern)]
        
        # Unstuff the data
        original_data = self.unstuff_data(stuffed_data)
        
        return original_data
    
    def find_frames(self, bit_stream: str) -> List[Tuple[str, int, int]]:
        """
        Find all frames in a bit stream.
        
        Args:
            bit_stream (str): Binary string containing multiple frames
            
        Returns:
            List[Tuple[str, int, int]]: List of (frame_data, start_pos, end_pos) tuples
        """
        if not self._is_valid_binary_pattern(bit_stream):
            raise ValueError("Bit stream must contain only binary digits (0 and 1)")
        
        frames = []
        flag_len = len(self.flag_pattern)
        
        # Find all occurrences of flag pattern
        flag_positions = []
        for i in range(len(bit_stream) - flag_len + 1):
            if bit_stream[i:i + flag_len] == self.flag_pattern:
                flag_positions.append(i)
        
        # Extract frames between consecutive flags
        for i in range(len(flag_positions) - 1):
            start_pos = flag_positions[i]
            end_pos = flag_positions[i + 1] + flag_len
            
            # Extract frame
            frame = bit_stream[start_pos:end_pos]
            
            # Verify it's a valid frame
            if frame.startswith(self.flag_pattern) and frame.endswith(self.flag_pattern):
                try:
                    frame_data = self.extract_frame_data(frame)
                    frames.append((frame_data, start_pos, end_pos))
                except ValueError:
                    # Skip invalid frames
                    continue
        
        return frames
    
    def get_info(self) -> dict:
        """
        Get information about the Bit Stuffing configuration.
        
        Returns:
            dict: Configuration information
        """
        return {
            'flag_pattern': self.flag_pattern,
            'stuffing_pattern': self.stuffing_pattern,
            'stuffing_threshold': self.stuffing_threshold,
            'flag_length': len(self.flag_pattern),
            'stuffing_pattern_length': len(self.stuffing_pattern)
        }


class BitStuffingAnalyzer:
    """
    Utility class for analyzing bit stuffing performance and characteristics.
    """
    
    @staticmethod
    def calculate_stuffing_overhead(data: str, stuffing_threshold: int = 5) -> dict:
        """
        Calculate the overhead introduced by bit stuffing.
        
        Args:
            data (str): Binary string data
            stuffing_threshold (int): Number of consecutive 1s that trigger stuffing
            
        Returns:
            dict: Overhead analysis
        """
        if not all(bit in '01' for bit in data):
            raise ValueError("Data must contain only binary digits (0 and 1)")
        
        # Count consecutive 1s sequences
        consecutive_ones_count = 0
        stuffing_opportunities = 0
        
        current_ones = 0
        for bit in data:
            if bit == '1':
                current_ones += 1
            else:
                if current_ones >= stuffing_threshold:
                    stuffing_opportunities += 1
                current_ones = 0
        
        # Check if sequence ends with consecutive 1s
        if current_ones >= stuffing_threshold:
            stuffing_opportunities += 1
        
        # Calculate overhead
        original_length = len(data)
        stuffed_length = original_length + stuffing_opportunities
        overhead_bits = stuffing_opportunities
        overhead_percentage = (overhead_bits / original_length) * 100 if original_length > 0 else 0
        
        return {
            'original_length': original_length,
            'stuffed_length': stuffed_length,
            'overhead_bits': overhead_bits,
            'overhead_percentage': overhead_percentage,
            'stuffing_opportunities': stuffing_opportunities,
            'efficiency': original_length / stuffed_length if stuffed_length > 0 else 0
        }
    
    @staticmethod
    def analyze_data_patterns(data: str) -> dict:
        """
        Analyze patterns in data that affect bit stuffing.
        
        Args:
            data (str): Binary string data
            
        Returns:
            dict: Pattern analysis
        """
        if not all(bit in '01' for bit in data):
            raise ValueError("Data must contain only binary digits (0 and 1)")
        
        # Count consecutive 1s sequences
        consecutive_ones_sequences = []
        current_ones = 0
        
        for bit in data:
            if bit == '1':
                current_ones += 1
            else:
                if current_ones > 0:
                    consecutive_ones_sequences.append(current_ones)
                current_ones = 0
        
        # Add final sequence if data ends with 1s
        if current_ones > 0:
            consecutive_ones_sequences.append(current_ones)
        
        # Analyze sequences
        if consecutive_ones_sequences:
            max_consecutive = max(consecutive_ones_sequences)
            avg_consecutive = sum(consecutive_ones_sequences) / len(consecutive_ones_sequences)
            sequences_requiring_stuffing = sum(1 for seq in consecutive_ones_sequences if seq >= 5)
        else:
            max_consecutive = 0
            avg_consecutive = 0
            sequences_requiring_stuffing = 0
        
        return {
            'total_sequences': len(consecutive_ones_sequences),
            'max_consecutive_ones': max_consecutive,
            'avg_consecutive_ones': avg_consecutive,
            'sequences_requiring_stuffing': sequences_requiring_stuffing,
            'consecutive_ones_sequences': consecutive_ones_sequences
        }


class BitStuffingProtocols:
    """
    Collection of standard bit stuffing protocols and their configurations.
    """
    
    @staticmethod
    def get_standard_protocols() -> dict:
        """
        Get information about standard bit stuffing protocols.
        
        Returns:
            dict: Standard protocols information
        """
        return {
            'HDLC': {
                'flag_pattern': '01111110',
                'stuffing_pattern': '11111',
                'description': 'High-Level Data Link Control'
            },
            'PPP': {
                'flag_pattern': '01111110',
                'stuffing_pattern': '11111',
                'description': 'Point-to-Point Protocol'
            },
            'SDLC': {
                'flag_pattern': '01111110',
                'stuffing_pattern': '11111',
                'description': 'Synchronous Data Link Control'
            },
            'LAPB': {
                'flag_pattern': '01111110',
                'stuffing_pattern': '11111',
                'description': 'Link Access Procedure Balanced'
            },
            'Custom': {
                'flag_pattern': '01111110',
                'stuffing_pattern': '11111',
                'description': 'Custom configuration'
            }
        }
    
    @staticmethod
    def create_protocol_instance(protocol_name: str) -> BitStuffing:
        """
        Create a BitStuffing instance for a standard protocol.
        
        Args:
            protocol_name (str): Name of the protocol
            
        Returns:
            BitStuffing: Configured BitStuffing instance
        """
        protocols = BitStuffingProtocols.get_standard_protocols()
        
        if protocol_name not in protocols:
            raise ValueError(f"Unknown protocol: {protocol_name}")
        
        protocol_config = protocols[protocol_name]
        return BitStuffing(
            flag_pattern=protocol_config['flag_pattern'],
            stuffing_pattern=protocol_config['stuffing_pattern']
        )


def demonstrate_bit_stuffing():
    """Demonstrate basic bit stuffing functionality."""
    print("=" * 60)
    print("BIT STUFFING DEMONSTRATION")
    print("=" * 60)
    
    # Create BitStuffing instance
    bit_stuffing = BitStuffing()
    info = bit_stuffing.get_info()
    
    print(f"Flag pattern: {info['flag_pattern']}")
    print(f"Stuffing pattern: {info['stuffing_pattern']}")
    print(f"Stuffing threshold: {info['stuffing_threshold']} consecutive 1s")
    
    # Test data with consecutive 1s
    test_data = "110111111011111110"
    print(f"\nOriginal data: {test_data}")
    
    # Perform bit stuffing
    stuffed_data = bit_stuffing.stuff_data(test_data)
    print(f"Stuffed data:  {stuffed_data}")
    
    # Remove bit stuffing
    unstuffed_data = bit_stuffing.unstuff_data(stuffed_data)
    print(f"Unstuffed data: {unstuffed_data}")
    
    # Verify correctness
    print(f"Data matches: {'Yes' if test_data == unstuffed_data else 'No'}")
    
    # Show stuffing positions
    print("\nStuffing analysis:")
    for i, (orig, stuffed) in enumerate(zip(test_data, stuffed_data)):
        if orig != stuffed:
            print(f"  Position {i}: '{orig}' -> '{stuffed}' (stuffed bit)")


def demonstrate_frame_creation():
    """Demonstrate frame creation and extraction."""
    print("\n" + "=" * 60)
    print("FRAME CREATION AND EXTRACTION DEMONSTRATION")
    print("=" * 60)
    
    bit_stuffing = BitStuffing()
    
    # Test data
    test_data = "101111111011111110"
    print(f"Original data: {test_data}")
    
    # Create frame
    frame = bit_stuffing.create_frame(test_data)
    print(f"Complete frame: {frame}")
    
    # Extract data from frame
    extracted_data = bit_stuffing.extract_frame_data(frame)
    print(f"Extracted data: {extracted_data}")
    
    # Verify correctness
    print(f"Data matches: {'Yes' if test_data == extracted_data else 'No'}")
    
    # Show frame structure
    flag_len = len(bit_stuffing.flag_pattern)
    print(f"\nFrame structure:")
    print(f"  Start flag: {frame[:flag_len]}")
    print(f"  Stuffed data: {frame[flag_len:-flag_len]}")
    print(f"  End flag: {frame[-flag_len:]}")


def demonstrate_multiple_frames():
    """Demonstrate handling multiple frames in a bit stream."""
    print("\n" + "=" * 60)
    print("MULTIPLE FRAMES DEMONSTRATION")
    print("=" * 60)
    
    bit_stuffing = BitStuffing()
    
    # Create multiple frames
    data1 = "1011111110"
    data2 = "0111111111"
    data3 = "1101111110"
    
    frame1 = bit_stuffing.create_frame(data1)
    frame2 = bit_stuffing.create_frame(data2)
    frame3 = bit_stuffing.create_frame(data3)
    
    # Combine frames
    bit_stream = frame1 + frame2 + frame3
    print(f"Bit stream with 3 frames: {bit_stream}")
    
    # Find and extract frames
    frames = bit_stuffing.find_frames(bit_stream)
    print(f"\nFound {len(frames)} frames:")
    
    for i, (frame_data, start_pos, end_pos) in enumerate(frames):
        print(f"  Frame {i+1}: {frame_data}")
        print(f"    Position: {start_pos}-{end_pos}")
        print(f"    Length: {end_pos - start_pos} bits")


def demonstrate_overhead_analysis():
    """Demonstrate bit stuffing overhead analysis."""
    print("\n" + "=" * 60)
    print("BIT STUFFING OVERHEAD ANALYSIS")
    print("=" * 60)
    
    # Test different data patterns
    test_cases = [
        "101111111011111110",  # High stuffing overhead
        "101010101010101010",  # No stuffing needed
        "111111111111111111",  # Maximum stuffing
        "110111011101110111",  # Medium stuffing
    ]
    
    for i, data in enumerate(test_cases):
        print(f"\nTest case {i+1}: {data}")
        
        # Calculate overhead
        overhead = BitStuffingAnalyzer.calculate_stuffing_overhead(data)
        print(f"  Original length: {overhead['original_length']} bits")
        print(f"  Stuffed length: {overhead['stuffed_length']} bits")
        print(f"  Overhead: {overhead['overhead_bits']} bits ({overhead['overhead_percentage']:.1f}%)")
        print(f"  Efficiency: {overhead['efficiency']:.3f}")
        
        # Analyze patterns
        patterns = BitStuffingAnalyzer.analyze_data_patterns(data)
        print(f"  Max consecutive 1s: {patterns['max_consecutive_ones']}")
        print(f"  Sequences requiring stuffing: {patterns['sequences_requiring_stuffing']}")


def demonstrate_protocols():
    """Demonstrate different bit stuffing protocols."""
    print("\n" + "=" * 60)
    print("BIT STUFFING PROTOCOLS DEMONSTRATION")
    print("=" * 60)
    
    protocols = BitStuffingProtocols.get_standard_protocols()
    
    print("Standard Bit Stuffing Protocols:")
    print("-" * 40)
    
    for protocol_name, config in protocols.items():
        print(f"{protocol_name}:")
        print(f"  Flag pattern: {config['flag_pattern']}")
        print(f"  Stuffing pattern: {config['stuffing_pattern']}")
        print(f"  Description: {config['description']}")
        print()
    
    # Test with HDLC protocol
    print("Testing with HDLC protocol:")
    hdlc = BitStuffingProtocols.create_protocol_instance('HDLC')
    
    test_data = "101111111011111110"
    stuffed_data = hdlc.stuff_data(test_data)
    frame = hdlc.create_frame(test_data)
    
    print(f"Original data: {test_data}")
    print(f"Stuffed data: {stuffed_data}")
    print(f"HDLC frame: {frame}")


def main():
    """Main function to demonstrate bit stuffing methods."""
    print("BIT STUFFING METHODS IMPLEMENTATION")
    print("===================================")
    
    # Demonstrate basic bit stuffing
    demonstrate_bit_stuffing()
    
    # Demonstrate frame creation
    demonstrate_frame_creation()
    
    # Demonstrate multiple frames
    demonstrate_multiple_frames()
    
    # Demonstrate overhead analysis
    demonstrate_overhead_analysis()
    
    # Demonstrate protocols
    demonstrate_protocols()
    
    print("\n" + "=" * 60)
    print("INTERACTIVE TESTING")
    print("=" * 60)
    
    # Interactive testing
    while True:
        print("\nChoose an option:")
        print("1. Test bit stuffing/unstuffing")
        print("2. Test frame creation/extraction")
        print("3. Test multiple frames")
        print("4. Analyze overhead")
        print("5. Test different protocols")
        print("6. Exit")
        
        choice = input("Enter your choice (1-6): ").strip()
        
        if choice == '1':
            data = input("Enter binary data: ").strip()
            stuffing_threshold = int(input("Enter stuffing threshold (default 5): ") or "5")
            
            try:
                bit_stuffing = BitStuffing(stuffing_pattern="1" * stuffing_threshold)
                stuffed = bit_stuffing.stuff_data(data)
                unstuffed = bit_stuffing.unstuff_data(stuffed)
                
                print(f"Original data: {data}")
                print(f"Stuffed data: {stuffed}")
                print(f"Unstuffed data: {unstuffed}")
                print(f"Data matches: {'Yes' if data == unstuffed else 'No'}")
            except ValueError as e:
                print(f"Error: {e}")
        
        elif choice == '2':
            data = input("Enter binary data: ").strip()
            
            try:
                bit_stuffing = BitStuffing()
                frame = bit_stuffing.create_frame(data)
                extracted = bit_stuffing.extract_frame_data(frame)
                
                print(f"Original data: {data}")
                print(f"Frame: {frame}")
                print(f"Extracted data: {extracted}")
                print(f"Data matches: {'Yes' if data == extracted else 'No'}")
            except ValueError as e:
                print(f"Error: {e}")
        
        elif choice == '3':
            num_frames = int(input("Enter number of frames: "))
            frames_data = []
            
            for i in range(num_frames):
                data = input(f"Enter data for frame {i+1}: ").strip()
                frames_data.append(data)
            
            try:
                bit_stuffing = BitStuffing()
                
                # Create frames
                frames = [bit_stuffing.create_frame(data) for data in frames_data]
                bit_stream = ''.join(frames)
                
                print(f"Bit stream: {bit_stream}")
                
                # Find frames
                found_frames = bit_stuffing.find_frames(bit_stream)
                print(f"Found {len(found_frames)} frames:")
                
                for i, (frame_data, start, end) in enumerate(found_frames):
                    print(f"  Frame {i+1}: {frame_data}")
            except ValueError as e:
                print(f"Error: {e}")
        
        elif choice == '4':
            data = input("Enter binary data: ").strip()
            threshold = int(input("Enter stuffing threshold (default 5): ") or "5")
            
            try:
                overhead = BitStuffingAnalyzer.calculate_stuffing_overhead(data, threshold)
                patterns = BitStuffingAnalyzer.analyze_data_patterns(data)
                
                print(f"Data: {data}")
                print(f"Overhead analysis:")
                print(f"  Original length: {overhead['original_length']} bits")
                print(f"  Stuffed length: {overhead['stuffed_length']} bits")
                print(f"  Overhead: {overhead['overhead_bits']} bits ({overhead['overhead_percentage']:.1f}%)")
                print(f"  Efficiency: {overhead['efficiency']:.3f}")
                print(f"Pattern analysis:")
                print(f"  Max consecutive 1s: {patterns['max_consecutive_ones']}")
                print(f"  Sequences requiring stuffing: {patterns['sequences_requiring_stuffing']}")
            except ValueError as e:
                print(f"Error: {e}")
        
        elif choice == '5':
            protocols = BitStuffingProtocols.get_standard_protocols()
            print("Available protocols:")
            for i, protocol in enumerate(protocols.keys(), 1):
                print(f"  {i}. {protocol}")
            
            protocol_choice = input("Enter protocol name: ").strip()
            data = input("Enter binary data: ").strip()
            
            try:
                bit_stuffing = BitStuffingProtocols.create_protocol_instance(protocol_choice)
                stuffed = bit_stuffing.stuff_data(data)
                frame = bit_stuffing.create_frame(data)
                
                print(f"Protocol: {protocol_choice}")
                print(f"Original data: {data}")
                print(f"Stuffed data: {stuffed}")
                print(f"Frame: {frame}")
            except ValueError as e:
                print(f"Error: {e}")
        
        elif choice == '6':
            print("Exiting...")
            break
        
        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()
