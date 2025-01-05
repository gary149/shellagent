from shell_command_agent import create_shell_agent

# Create the agent
agent = create_shell_agent()

# Example commands
result = agent.run("Show me the disk usage in human readable format")
print(result)

result = agent.run("Create a new directory called 'test' and list its contents")
print(result)
