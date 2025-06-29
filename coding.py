import numpy as np
from typing import Tuple
import math

class OrthogonalCoding:
    def __init__(self, n: int = 7):
        self.n = n
        self.code_length = 2 ** n  # 128 bits for n=7
        self.hadamard_matrix = self._generate_hadamard_matrix(self.code_length)
    
    def _generate_hadamard_matrix(self, size: int) -> np.ndarray:
        if size == 1:
            return np.array([[1]])
        
        n = int(math.log2(size))
        
        H = np.array([[1, 1], [1, -1]])
        
        for i in range(2, n + 1):
            H_prev = H
            H = np.zeros((2**i, 2**i), dtype=int)
            H[:2**(i-1), :2**(i-1)] = H_prev
            H[:2**(i-1), 2**(i-1):] = H_prev
            H[2**(i-1):, :2**(i-1)] = H_prev
            H[2**(i-1):, 2**(i-1):] = -H_prev
        
        H = (H + 1) // 2
        return H
    
    def encode_block(self, data_bits: str) -> str:
        if len(data_bits) != self.n:
            raise ValueError(f"Data block must be {self.n} bits long")
        
        row_index = int(data_bits, 2)
        
        codeword = self.hadamard_matrix[row_index]
        
        return ''.join(map(str, codeword))
    
    def encode(self, data_bits: str) -> Tuple[str, dict]:
        padding_needed = (self.n - len(data_bits) % self.n) % self.n
        padded_data = data_bits + '0' * padding_needed
        
        encoded_bits = ''
        for i in range(0, len(padded_data), self.n):
            block = padded_data[i:i+self.n]
            encoded_block = self.encode_block(block)
            encoded_bits += encoded_block
        
        parameters = {
            'n': self.n,
            'original_length': len(data_bits),
            'padding_added': padding_needed
        }
        
        return encoded_bits, parameters
    
    def decode_block(self, received_bits: str) -> str:
        if len(received_bits) != self.code_length:
            raise ValueError(f"Received block must be {self.code_length} bits long")
        
        received = np.array([int(b) for b in received_bits])
        
        correlations = []
        for i in range(2**self.n):
            codeword = self.hadamard_matrix[i]
            correlation = np.sum(received == codeword)
            correlations.append(correlation)
        
        best_match = np.argmax(correlations)
        
        return format(best_match, f'0{self.n}b')
    
    def decode(self, encoded_bits: str, parameters: dict) -> Tuple[str, int]:
        n = parameters['n']
        original_length = parameters['original_length']
        
        if len(encoded_bits) % self.code_length != 0:
            truncated_length = (len(encoded_bits) // self.code_length) * self.code_length
            print(f"Warning: Truncating encoded data from {len(encoded_bits)} to {truncated_length} bits")
            encoded_bits = encoded_bits[:truncated_length]
        
        if len(encoded_bits) == 0:
            return '', 0
        
        decoded_bits = ''
        total_errors_corrected = 0
        
        for i in range(0, len(encoded_bits), self.code_length):
            block = encoded_bits[i:i+self.code_length]
            if len(block) == self.code_length: 
                decoded_block = self.decode_block(block)
                decoded_bits += decoded_block
                
                re_encoded = self.encode_block(decoded_block)
                errors_in_block = sum(1 for a, b in zip(block, re_encoded) if a != b)
                total_errors_corrected += errors_in_block
        
        decoded_bits = decoded_bits[:original_length]
        
        return decoded_bits, total_errors_corrected