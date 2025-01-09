# Shell Command Agent

> [!CAUTION]  
> DO NOT RUN THIS APPLICATION! This tool automatically executes ANY shell command with your user permissions without confirmation. It can cause irreversible system damage. Use only in isolated test environments.

A Python-based tool that uses [smolagents](https://github.com/huggingface/smolagents) to execute shell commands based on natural language prompts.


## Quick Start

This application uses LiteLLM to support various local LLM providers. For privacy and security, never use cloud-based LLMs as they could expose sensitive system information.

1. Set up your preferred local LLM provider (LM Studio, Ollama, etc.)
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the application with your chosen model:
   ```bash
   python app.py "list files in current directory" --model provider/model-name
   ```

## LM Studio Example

One way to run this tool is with LM Studio's local models:

1. Download and install [LM Studio](https://lmstudio.ai/)
2. Download the recommended [Qwen2.5-Coder-14B-Instruct-GGUF model](https://huggingface.co/Qwen/Qwen2.5-Coder-14B-Instruct-GGUF)
3. Start LM Studio's local inference server (default: http://localhost:1234/v1)
4. Run commands using the lm_studio provider:
   ```bash
   python app.py "your prompt" --model lm_studio/qwen2.5-coder-14b-instruct
   ```

Note: The LM Studio API base URL is automatically set to `http://localhost:1234/v1` but can be overridden:

```bash
export LM_STUDIO_API_BASE="http://localhost:1234/v1"
```

## Usage Examples

### Command Line Interface

```bash
# Organize Python files in a project directory
python app.py "create a 'python_files' directory and move all .py files into it, then show me the contents of both directories" --path ~/projects/my-python-project --model lm_studio/qwen2.5-coder-14b-instruct

# Find and analyze large files in Downloads
python app.py "find files larger than 100MB in the current directory, show their sizes in human readable format, and create a report.txt with this information" --path ~/Downloads --model lm_studio/qwen2.5-coder-14b-instruct

# Organize files by extension in Documents
python app.py "create separate directories for different file types (like images, documents, etc), move files into appropriate directories based on their extensions, then show the new structure" --path ~/Documents --model lm_studio/qwen2.5-coder-14b-instruct
```

## Environment Variables

- `LM_STUDIO_API_BASE`: API base URL for LM Studio (default: "http://localhost:1234/v1")

## Project Structure

- `app.py`: Command-line interface
- `shell_command_agent.py`: Core agent implementation
- `example_usage.py`: Example usage of the Python API

## Dependencies

- [smolagents](https://github.com/huggingface/smolagents)

## Contributing

Feel free to open issues or submit pull requests for improvements or bug fixes.
