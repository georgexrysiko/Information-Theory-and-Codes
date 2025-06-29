import requests
from fanoshannon import FanoShannon
from coding import OrthogonalCoding
from utils import (
    check_mime_type, calculate_entropy, calculate_sha256,
    bytes_to_bits, add_errors, transform_to_base64,
    bits_to_bytes_with_padding
)

class CompressionClient:
    def __init__(self, server_url="http://localhost:5000"):
        self.server_url = server_url
        self.fano_shannon = FanoShannon()
        self.walsh_hadamard = OrthogonalCoding(n=7)  # 128-bit blocks
    
    def process_image(self, file_path: str, error_percentage: float = 0.0):
        if not check_mime_type(file_path):
            raise ValueError("File is not an image based on MIME type")
        
        try:
            with open(file_path, 'rb') as f:
                image_data = f.read()
        except FileNotFoundError:
            raise FileNotFoundError(f"File {file_path} not found")
        
        print(f"Original file size: {len(image_data)} bytes")
        
        original_sha256 = calculate_sha256(image_data)
        original_entropy = calculate_entropy(image_data)
        
        print(f"Original SHA256: {original_sha256}")
        print(f"Original entropy: {original_entropy:.4f}")
        
        compressed_bits, code_table = self.fano_shannon.compress(image_data)
        print(f"Compressed to {len(compressed_bits)} bits")
        
        padded_bytes = bits_to_bytes_with_padding(compressed_bits, block_size=16)
        
        padded_bits = bytes_to_bits(padded_bytes)
        
        encoded_bits, encoding_params = self.walsh_hadamard.encode(padded_bits)
        print(f"Padded bits length: {len(padded_bits)}")
        print(f"Encoded to {len(encoded_bits)} bits")
        print(f"Encoded length should be multiple of 128: {len(encoded_bits) % 128 == 0}")
        
        error_bits, num_errors = add_errors(encoded_bits, error_percentage)
        
        if num_errors > 0:
            print(f"Added {num_errors} errors ({error_percentage}%)")
        
        while len(error_bits) % 8 != 0:
            error_bits += '0'
        
        error_bytes = []
        for i in range(0, len(error_bits), 8):
            byte_bits = error_bits[i:i+8]
            error_bytes.append(int(byte_bits, 2))
        
        error_bytes = bytes(error_bytes)
        encoded_message = transform_to_base64(error_bytes)
        
        parameters = {
            'code_table': code_table,
            'encoding_params': encoding_params,
            'compressed_length': len(compressed_bits)
        }
        
        message = {
            "encoded_message": encoded_message,
            "compression_algorithm": "fano-shannon",
            "encoding": "orthogonal",
            "parameters": parameters,
            "errors": num_errors,
            "SHA256": original_sha256,
            "entropy": original_entropy
        }
        
        return message
    
    def send_to_server(self, message: dict):
        try:
            headers = {'Content-Type': 'application/json'}
            response = requests.post(
                f"{self.server_url}/decode",
                json=message,
                headers=headers,
                timeout=30
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                print(f"Server error: {response.status_code}")
                print(response.text)
                return None
                
        except requests.exceptions.RequestException as e:
            print(f"Connection error: {e}")
            return None
    
    def run(self, file_path: str, error_percentage: float = 0.0):
        try:
            print("\n---CLIENT PROCESSING---")
            
            message = self.process_image(file_path, error_percentage)
            
            print("\n---SENDING TO SERVER---")
            
            response = self.send_to_server(message)
            
            if response:
                print("\n---SERVER RESPONSE---")
                print(f"Decoding successful: {response.get('success', False)}")
                print(f"Errors corrected: {response.get('errors_corrected', 0)}")
                print(f"Original errors sent: {response.get('original_errors', 0)}")
                print(f"SHA256 match: {response.get('sha256_match', False)}")
                print(f"Decoded SHA256: {response.get('decoded_sha256', 'N/A')}")
                print(f"Final entropy: {response.get('final_entropy', 'N/A')}")
                
                if response.get('message'):
                    print(f"Message: {response['message']}")
                    
                return response
            else:
                print("Failed to get response from server")
                return None
                
        except Exception as e:
            print(f"Client error: {e}")
            return None

def main():
    client = CompressionClient()
    
    # Example usage
    file_path = input("Enter image file path: ").strip()
    error_percentage = float(input("Enter error percentage (0-100): ") or "0")
    
    client.run(file_path, error_percentage)

if __name__ == "__main__":
    main()