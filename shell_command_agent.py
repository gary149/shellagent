from smolagents import CodeAgent, HfApiModel, tool
import subprocess
import os
from typing import Optional

@tool
def execute_shell_command(command: str) -> str:
    """
    Executes a shell command and returns its output.
    
    Args:
        command: The shell command to execute. Be careful with destructive commands!
        
    Returns:
        The command output (stdout and stderr combined)
    """
    try:
        # Run command and capture output
        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
            cwd=os.getcwd()
        )
        
        # Combine stdout and stderr
        output = ""
        if result.stdout:
            output += f"STDOUT:\n{result.stdout}\n"
        if result.stderr:
            output += f"STDERR:\n{result.stderr}\n"
            
        output += f"Exit code: {result.returncode}"
        return output
        
    except Exception as e:
        return f"Error executing command: {str(e)}"

def create_shell_agent(model_name: Optional[str] = "Qwen/Qwen2.5-72B-Instruct") -> CodeAgent:
    """
    Creates an agent that can execute shell commands.
    
    Args:
        model_name: The name of the HuggingFace model to use
        
    Returns:
        A CodeAgent configured to run shell commands
    """
    agent = CodeAgent(
        tools=[execute_shell_command],
        model=HfApiModel(model_name),
        system_prompt="""You are a helpful assistant that can execute shell commands.
        Be very careful with destructive commands that could harm the system.
        Always explain what commands you're going to run and why.
        {{tool_descriptions}}
        {{authorized_imports}}"""
    )
    return agent

if __name__ == "__main__":
    # Example usage
    agent = create_shell_agent()
    
    # Run a simple command
    result = agent.run("List all files in the current directory")
    print(result)
