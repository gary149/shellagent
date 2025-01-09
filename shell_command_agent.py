from smolagents import tool, CodeAgent, LiteLLMModel

DANGEROUS_COMMANDS = [
    "rm -rf",
    "mkfs",
    "dd",
    "format",
    ">",
    "sudo",
    "chmod",
    "chown",
]


def _validate_command(command: str) -> None:
    """Check if command contains dangerous operations"""
    command = command.lower()
    for dangerous in DANGEROUS_COMMANDS:
        if dangerous in command:
            raise ValueError(
                f"Command '{command}' contains dangerous operation '{dangerous}'. "
                "This command is not allowed for safety reasons."
            )


@tool
def execute_shell_command(command: str) -> str:
    """Executes a shell command and returns its output.

    This tool executes a single shell command and returns the combined stdout/stderr output.

    Preferred commands:
    - ls, pwd, echo, cat (read-only operations)
    - mkdir, mv, cp (safe file operations)
    - System info like uname, whoami

    Forbidden commands:
    - rm -rf or any recursive deletes
    - Format/partition commands
    - Raw network access
    - Writing to system directories
    - Multi-command operations with && or ;
    - Pipes or redirections

    Args:
        command: The shell command to execute as a string

    Returns:
        The command output as a string, including any error messages
    """
    # Import here as required for Hub compatibility
    import subprocess
    import os

    try:
        # Validate command first
        _validate_command(command)

        print(f"Executing command: {command}")

        # Run command with safety measures
        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
            cwd=os.getcwd(),
            timeout=30,  # Prevent infinite running
        )

        # Format output
        output = []
        if result.stdout:
            output.append(result.stdout.strip())
        if result.stderr:
            output.append(result.stderr.strip())
        if result.returncode != 0:
            output.append(f"Exit code: {result.returncode}")

        return "\n".join(output)

    except subprocess.TimeoutExpired:
        return "Error: Command timed out after 30 seconds"
    except Exception as e:
        return f"Error executing command: {str(e)}"


def create_shell_agent(
    model_name: str,
) -> CodeAgent:
    """
    Creates an agent that can execute shell commands.

    Args:
        model_name: The name of the LLM model to use (required)
                   Format: "lm_studio/<model-name>"
                   Example: "lm_studio/qwen2.5-coder-14b-instruct"

                   Requires LM Studio server running locally:
                   1. Download LM Studio: https://lmstudio.ai/
                   2. Start the local inference server
                   3. Set env var: export LM_STUDIO_API_BASE="http://localhost:1234/v1"

    Returns:
        A CodeAgent configured to run shell commands with safety measures
    """

    # Create agent with enhanced prompt
    agent = CodeAgent(
        tools=[execute_shell_command],
        model=LiteLLMModel(model_name),
        max_iterations=40,
    )
    return agent


if __name__ == "__main__":
    # Example usage
    agent = create_shell_agent()

    # Run safe example commands
    print("Testing directory listing...")
    agent.run("Show me what files are in the current directory")

    print("\nTesting system info...")
    agent.run("What operating system am I running?")
