import argparse
import os
from shell_command_agent import create_shell_agent

def main():
    # Create argument parser
    parser = argparse.ArgumentParser(description='Shell Command Agent CLI')
    parser.add_argument('prompt', type=str, help='The prompt to run with the shell agent')
    parser.add_argument('--path', '-p', type=str, default=os.getcwd(),
                       help='The path where to run the command (default: current directory)')
    
    # Parse arguments
    args = parser.parse_args()
    
    # Validate path
    if not os.path.exists(args.path):
        print(f"Error: Path '{args.path}' does not exist")
        return 1
    
    # Change to specified directory
    original_dir = os.getcwd()
    os.chdir(args.path)
    
    try:
        # Create and run agent
        agent = create_shell_agent()
        result = agent.run(args.prompt)
        print(result)
    finally:
        # Always return to original directory
        os.chdir(original_dir)
    
    return 0

if __name__ == '__main__':
    exit(main())
