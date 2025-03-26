import requests
import argparse
import json

class FunctionExecutionCLI:
    def __init__(self, base_url="http://localhost:8000"):
        """
        Initialize CLI with base API URL
        """
        self.base_url = base_url
        self.session_id = None

    def execute_prompt(self, prompt, params=None):
        """
        Send prompt to API and execute function
        """
        try:
            # Prepare request payload
            payload = {
                "prompt": prompt,
                "session_id": self.session_id
            }
            
            # Add parameters if provided
            if params:
                payload["params"] = params
            
            # Send request to API
            response = requests.post(f"{self.base_url}/execute", json=payload)
            
            # Check response
            if response.status_code == 200:
                result = response.json()
                
                # Update session ID
                if result.get('session_id'):
                    self.session_id = result['session_id']
                
                return result
            else:
                print(f"Error: {response.status_code} - {response.text}")
                return None
        
        except requests.exceptions.RequestException as e:
            print(f"Connection error: {e}")
            return None

    def interactive_mode(self):
        """
        Interactive CLI mode
        """
        print("Function Execution CLI")
        print("Type 'exit' to quit")
        
        while True:
            try:
                # Get user prompt
                prompt = input("\nEnter your prompt: ")
                
                # Check for exit
                if prompt.lower() in ['exit', 'quit', 'q']:
                    break
                
                # Check for parameters
                params = None
                if '|' in prompt:
                    prompt, param_str = prompt.split('|', 1)
                    try:
                        params = json.loads(param_str.strip())
                    except json.JSONDecodeError:
                        print("Invalid parameter format. Use JSON.")
                        continue
                
                # Execute prompt
                result = self.execute_prompt(prompt.strip(), params)
                
                # Display result
                if result:
                    print("\n--- Result ---")
                    print(json.dumps(result, indent=2))
            
            except KeyboardInterrupt:
                print("\nOperation cancelled.")
                break
            except Exception as e:
                print(f"An error occurred: {e}")

def main():
    # Create argument parser
    parser = argparse.ArgumentParser(description="Function Execution CLI")
    parser.add_argument('-p', '--prompt', help="Execute a single prompt")
    parser.add_argument('-i', '--interactive', action='store_true', help="Start interactive mode")
    
    args = parser.parse_args()
    
    # Create CLI instance
    cli = FunctionExecutionCLI()
    
    # Execute based on arguments
    if args.prompt:
        # Single prompt execution
        result = cli.execute_prompt(args.prompt)
        if result:
            print(json.dumps(result, indent=2))
    elif args.interactive:
        # Interactive mode
        cli.interactive_mode()
    else:
        # Default to interactive if no arguments
        cli.interactive_mode()

if __name__ == "__main__":
    main()