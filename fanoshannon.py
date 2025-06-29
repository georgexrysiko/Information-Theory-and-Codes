from collections import Counter
from typing import Dict, Tuple

class FanoShannon:
    def __init__(self):
        pass
    
    def _calculate_probabilities(self, data: bytes) -> Dict[int, float]:
        counter = Counter(data)
        total = len(data)
        return {symbol: count / total for symbol, count in counter.items()}

    def _build_fano_codes(self, symbols_freq):
        if not symbols_freq:
            return {}
        if len(symbols_freq) == 1:
            return {list(symbols_freq.keys())[0]: '0'}
        
        sorted_symbols = sorted(symbols_freq.items(), key=lambda x: x[1], reverse=True)
        
        def split_symbols(symbols):
            if len(symbols) == 1:
                return {symbols[0][0]: ''}
            if len(symbols) == 2:
                return {symbols[0][0]: '0', symbols[1][0]: '1'}
            
            total = sum(freq for _, freq in symbols)
            best_split = min(range(1, len(symbols)), 
                            key=lambda i: abs(2 * sum(freq for _, freq in symbols[:i]) - total))
            
            left, right = symbols[:best_split], symbols[best_split:]
        
            codes = {}
            for symbol, code in split_symbols(left).items():
                codes[symbol] = '0' + code
            for symbol, code in split_symbols(right).items():
                codes[symbol] = '1' + code
                
            return codes
        
        return split_symbols(sorted_symbols)
    
    def compress(self, data: bytes) -> Tuple[str, Dict[int, str]]:
        if not data:
            return '', {}
        
        symbols_freq = Counter(data)
        
        self.code_table = self._build_fano_codes(symbols_freq)
        
        if len(self.code_table) == 1:
            symbol = list(self.code_table.keys())[0]
            compressed_bits = '0' * len(data)
        else:
            compressed_bits = ''.join(self.code_table.get(byte, '0') for byte in data)
        
        return compressed_bits, self.code_table
    
    def decompress(self, compressed_bits: str, code_table: Dict) -> bytes:
        if not compressed_bits or not code_table:
            return b''
        
        if isinstance(list(code_table.keys())[0], str):
            code_table = {int(k): v for k, v in code_table.items()}
        
        if len(code_table) == 1:
            symbol = list(code_table.keys())[0]
            return bytes([symbol] * len(compressed_bits))
        
        decode_table = {code: symbol for symbol, code in code_table.items()}
        
        result = []
        current_code = ''
        
        for bit in compressed_bits:
            current_code += bit
            if current_code in decode_table:
                result.append(decode_table[current_code])
                current_code = ''
        
        if current_code:
            print(f"Warning: Incomplete code at end of compressed data: {current_code}")
        
        return bytes(result)