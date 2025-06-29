from collections import Counter
import hashlib
import mimetypes
import math
import base64
import random
from typing import Tuple

def calculate_entropy(data: bytes) -> float:
        if not data:
            return 0
        
        counter = Counter(data)
        total = len(data)
        entropy = 0

        for count in counter.values():
            probability = count/total
            if probability>0:
                entropy -= probability * math.log2(probability)

        return entropy

def calculate_sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()

def check_mime_type(file_path: str) -> bool:
    mime_type, _ = mimetypes.guess_type(file_path)
    return mime_type is not None and mime_type.startswith('image/')

def transform_to_base64(data: bytes) -> str:
    return base64.b64encode(data).decode('utf-8')

def transform_from_base64(base64_string: str) -> bytes:
    return base64.b64decode(base64_string.encode('utf-8'))

def add_errors(data: str, error_percentage: float) -> Tuple[str, int]:
        if not data or error_percentage <= 0:
            return data, 0
        
        data_list = list(data)
        num_errors = int(len(data) * error_percentage / 100)
        error_positions = random.sample(range(len(data)), min(num_errors, len(data)))
        
        for pos in error_positions:
            data_list[pos] = '1' if data_list[pos] == '0' else '0'
        
        return ''.join(data_list), len(error_positions)

def bytes_to_bits(data: bytes) -> str:
        return ''.join(format(byte, '08b') for byte in data)
    
def bits_to_bytes(bits: str) -> bytes:
    while len(bits) % 8 != 0:
        bits += '0'
    
    result = []
    for i in range(0, len(bits), 8):
        byte_bits = bits[i:i+8]
        result.append(int(byte_bits, 2))
    
    return bytes(result)

def pkcs7_pad(data: bytes, block_size: int = 16) -> bytes:
    if block_size <= 0 or block_size > 255:
        raise ValueError("Block size must be between 1 and 255")
    
    padding_length = block_size - (len(data) % block_size)
    
    padding = bytes([padding_length] * padding_length)
    
    return data + padding

def pkcs7_unpad(padded_data: bytes) -> bytes:    
    if not padded_data:
        raise ValueError("Cannot unpad empty data")
    
    padding_length = padded_data[-1]
    
    if padding_length == 0 or padding_length > len(padded_data):
        raise ValueError("Invalid padding length")
    
    padding_bytes = padded_data[-padding_length:]
    if not all(byte == padding_length for byte in padding_bytes):
        raise ValueError("Invalid padding bytes")
    
    return padded_data[:-padding_length]

def bits_to_bytes_with_padding(bits: str, block_size: int = 16) -> bytes:
    byte_data = bits_to_bytes(bits)
    
    return pkcs7_pad(byte_data, block_size)

def bytes_to_bits_with_unpadding(padded_data: bytes) -> str:
    unpadded_data = pkcs7_unpad(padded_data)
    
    return bytes_to_bits(unpadded_data)