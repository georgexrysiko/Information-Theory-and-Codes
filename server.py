from flask import Flask, request, jsonify
from fanoshannon import FanoShannon
from coding import OrthogonalCoding
from utils import (
    calculate_entropy, calculate_sha256,
    transform_from_base64, bytes_to_bits,
    bytes_to_bits_with_unpadding
)

app = Flask(__name__)

class CompressionServer:
    def __init__(self):
        self.fano_shannon = FanoShannon()
        self.walsh_hadamard = OrthogonalCoding(n=7)
    
    def decode_message(self, data: dict):
        try:
            encoded_message = data['encoded_message']
            compression_algorithm = data['compression_algorithm']
            encoding_type = data['encoding']
            parameters = data['parameters']
            original_errors = data['errors']
            original_sha256 = data['SHA256']
            original_entropy = data['entropy']
            
            print(f"Received message with {original_errors} errors")
            print(f"Compression: {compression_algorithm}, Encoding: {encoding_type}")
            
            message_bytes = transform_from_base64(encoded_message)
            message_bits = bytes_to_bits(message_bytes)
            
            print(f"Received message bits length: {len(message_bits)}")
            
            expected_length = (len(message_bits) // 128) * 128
            if expected_length != len(message_bits):
                print(f"Truncating from {len(message_bits)} to {expected_length} bits")
                message_bits = message_bits[:expected_length]
            
            if encoding_type == "orthogonal":
                encoding_params = parameters['encoding_params']
                decoded_bits, errors_corrected = self.walsh_hadamard.decode(
                    message_bits, encoding_params
                )
                print(f"Walsh-Hadamard corrected {errors_corrected} errors")
            else:
                raise ValueError(f"Unsupported encoding type: {encoding_type}")
            
            try:
                while len(decoded_bits) % 8 != 0:
                    decoded_bits += '0'
                
                decoded_bytes = []
                for i in range(0, len(decoded_bits), 8):
                    byte_bits = decoded_bits[i:i+8]
                    decoded_bytes.append(int(byte_bits, 2))
                
                decoded_bytes = bytes(decoded_bytes)
                unpadded_bits = bytes_to_bits_with_unpadding(decoded_bytes)
            except Exception as e:
                print(f"Padding error: {e}")
                unpadded_bits = decoded_bits
            
            if compression_algorithm == "fano-shannon":
                code_table = parameters['code_table']
                
                if isinstance(list(code_table.keys())[0], str):
                    code_table = {int(k): v for k, v in code_table.items()}
                
                decompressed_data = self.fano_shannon.decompress(unpadded_bits, code_table)
                print(f"Decompressed to {len(decompressed_data)} bytes")
            else:
                raise ValueError(f"Unsupported compression algorithm: {compression_algorithm}")
            
            decoded_sha256 = calculate_sha256(decompressed_data)
            final_entropy = calculate_entropy(decompressed_data)
            
            sha256_match = decoded_sha256 == original_sha256
            
            print(f"SHA256 match: {sha256_match}")
            print(f"Original SHA256: {original_sha256}")
            print(f"Decoded SHA256:  {decoded_sha256}")
            print(f"Final entropy: {final_entropy:.4f}")
            
            return {
                'success': True,
                'errors_corrected': errors_corrected,
                'original_errors': original_errors,
                'sha256_match': sha256_match,
                'decoded_sha256': decoded_sha256,
                'original_sha256': original_sha256,
                'final_entropy': final_entropy,
                'original_entropy': original_entropy,
                'decompressed_size': len(decompressed_data),
                'message': f"Successfully decoded. Corrected {errors_corrected} errors. SHA256 {'matches' if sha256_match else 'does not match'}."
            }
            
        except Exception as e:
            print(f"Decoding error: {e}")
            import traceback
            traceback.print_exc()
            return {
                'success': False,
                'error': str(e),
                'message': f"Decoding failed: {e}"
            }

server = CompressionServer()

@app.route('/decode', methods=['POST'])
def decode_endpoint():
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No JSON data received'}), 400
        
        print("\n---SERVER PROCESSING---")
        result = server.decode_message(data)
        
        return jsonify(result)
        
    except Exception as e:
        print(f"Server error: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'healthy', 'message': 'Server is running'})

@app.route('/', methods=['GET'])
def root():
    return jsonify({
        'message': 'Compression Server',
        'endpoints': {
            '/decode': 'POST - Decode compressed and encoded messages',
            '/health': 'GET - Health check'
        }
    })

def run_server(host='localhost', port=5000, debug=True):
    print(f"Starting server on {host}:{port}")
    app.run(host=host, port=port, debug=debug)

if __name__ == '__main__':
    run_server()