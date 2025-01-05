from smolagents import Tool, CodeAgent, HfApiModel
from typing import Optional

class ShellCommandTool(Tool):
    name = "execute_shell_command"
    description = """
    Executes a shell command and returns its output. This tool should be used carefully.
    IMPORTANT: Always check commands before executing them. Avoid destructive operations like:
    - rm -rf or any recursive deletes
    - Format or partition commands
    - Raw network access
    - Writing to system directories
    
    Preferred commands are read-only operations like:
    - ls, pwd, echo, cat
    - System info commands like uname, whoami
    - Directory navigation (cd, pwd)
    """
    
    inputs = {
        "command": {
            "type": "string",
            "description": "The shell command to execute. Must be safe and non-destructive."
        }
    }
    output_type = "string"

    DANGEROUS_COMMANDS = [
        "rm -rf", "mkfs", "dd", "format", ">", 
        "sudo", "chmod", "chown", "mv"
    ]

    def _validate_command(self, command: str) -> None:
        """Check if command contains dangerous operations"""
        command = command.lower()
        for dangerous in self.DANGEROUS_COMMANDS:
            if dangerous in command:
                raise ValueError(
                    f"Command '{command}' contains dangerous operation '{dangerous}'. "
                    "This command is not allowed for safety reasons."
                )

    def forward(self, command: str) -> str:
        """Execute the shell command safely"""
        # Import here as required for Hub compatibility
        import subprocess
        import os
        
        try:
            # Validate command first
            self._validate_command(command)
            
            print(f"Executing command: {command}")
            
            # Run command with safety measures
            result = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                text=True,
                cwd=os.getcwd(),
                timeout=30  # Prevent infinite running
            )
            
            # Format output
            output = []
            if result.stdout:
                output.append(f"STDOUT:\n{result.stdout.strip()}")
            if result.stderr:
                output.append(f"STDERR:\n{result.stderr.strip()}")
            output.append(f"Exit code: {result.returncode}")
            
            return "\n\n".join(output)
            
        except subprocess.TimeoutExpired:
            return "Error: Command timed out after 30 seconds"
        except Exception as e:
            return f"Error executing command: {str(e)}"

def create_shell_agent(model_name: Optional[str] = "Qwen/Qwen2.5-72B-Instruct") -> CodeAgent:
    """
    Creates an agent that can execute shell commands safely.
    
    Args:
        model_name: The name of the HuggingFace model to use
        
    Returns:
        A CodeAgent configured to run shell commands with safety measures
    """
    # Create tool instance
    shell_tool = ShellCommandTool()
    
    # Create agent with enhanced prompt
    agent = CodeAgent(
        tools=[shell_tool],
        model=HfApiModel(model_name),
        system_prompt="""You are a helpful assistant that can execute shell commands.
        
        IMPORTANT SAFETY RULES:
        1. Always explain what commands you plan to run and why
        2. Start with safe read-only commands like ls, pwd, echo
        3. Never use destructive commands like rm -rf, format, etc
        4. Avoid commands that modify system files or settings
        5. If unsure about a command's safety, ask for clarification
        
        {{tool_descriptions}}
        {{managed_agents_descriptions}}
        {{authorized_imports}}"""
    )
    return agent

if __name__ == "__main__":
    # Example usage
    agent = create_shell_agent()
    
    # Run safe example commands
    print("Testing directory listing...")
    result = agent.run("Show me what files are in the current directory")
    print(result)
    
    print("\nTesting system info...")
    result = agent.run("What operating system am I running?")
    print(result)
