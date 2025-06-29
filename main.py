import sys
import os
from client import CompressionClient
from server import run_server

def run_client_mode():
    client = CompressionClient()
    
    while True:
        print("\n---CLIENT---")
        
        try:
            file_path = input("Enter image file path (or 'quit' to exit): ").strip()
            
            if file_path.lower() == 'quit':                
                break
            
            if not os.path.exists(file_path):
                print(f"Error: File '{file_path}' not found!")
                continue
            
            error_percentage = input("Enter error percentage (0-100, default 0): ").strip()
            if not error_percentage:
                error_percentage = 0
            else:
                try:
                    error_percentage = float(error_percentage)
                    if error_percentage < 0 or error_percentage > 100:
                        print("Error percentage must be between 0 and 100")
                        continue
                except ValueError:
                    print("Invalid error percentage")
                    continue
            
            result = client.run(file_path, error_percentage)
            
            if result and result.get('success'):
                print("\n---PROCESSING COMPLETED SUCCESSFULLY---")
            else:
                print("\n---PROCESSING FAILED---")
                
        except KeyboardInterrupt:
            break
        except Exception as e:
            print(f"Error: {e}")

def run_server_mode():
    print("Starting server mode...")
    print("Server will run on http://localhost:5000")
    
    try:
        run_server(host='localhost', port=5000, debug=True)
    except KeyboardInterrupt:
        print("\nServer stopped.")

def show_usage():
    print("""
Usage: python main.py [mode]

Modes:
  server     - Run only the server
  client     - Run only the client (server must be running separately)
  help       - Show this help message

Examples:
  python main.py server          # Run server only
  python main.py client          # Run client only
  python main.py help            # Show help
""")

def main():
    mode = "help"  # default
    if len(sys.argv) > 1:
        mode = sys.argv[1].lower()
    
    if mode == "help":
        show_usage()
    elif mode == "server":
        run_server_mode()
    elif mode == "client":
        run_client_mode()
    else:
        print(f"Unknown mode: {mode}")
        show_usage()

if __name__ == "__main__":
    main()