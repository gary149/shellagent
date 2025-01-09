from shell_command_agent import create_shell_agent

# Create the agent - requires LM Studio server running locally
agent = create_shell_agent(model_name="lm_studio/qwen2.5-coder-14b-instruct")

# Example commands
print("Organizing project files...")
agent.run(
    "Create a 'src' directory, move all Python files there except example_usage.py, "
    "then create a requirements.txt by finding all import statements in the Python files"
)

print("\nAnalyzing directory structure...")
agent.run(
    "Show me a tree-like structure of the current directory, including file sizes, "
    "but exclude any __pycache__ directories and .pyc files"
)
