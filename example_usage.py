from shell_command_agent import create_shell_agent

# Create the agent
agent = create_shell_agent()

# Example commands
print("Checking disk usage...")
result = agent.run("I want to see the disk usage in human readable format. Please use the df -h command.")
print(result)

print("\nCreating and listing directory...")
result = agent.run("First create a directory named 'test' using mkdir, then list its contents with ls")
print(result)
