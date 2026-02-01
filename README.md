# Documentation Generator Agent

A Python-based tool for automatically generating documentation from source code repositories. It parses code, analyzes dependencies, and produces markdown documentation, with optional web interface support.

## Features
- Parses Python code to extract APIs and dependencies
- Builds dependency graphs
- Generates markdown documentation
- Loads repositories from GitHub
- Integrates with LLMs for advanced documentation
- Web interface for interactive use

## Project Structure
- `main.py`: Entry point for running the agent
- `api_parser.py`: Extracts API information from code
- `ast_analyzer.py`: Analyzes Python AST for code structure
- `dependency_graph.py`: Builds and visualizes dependency graphs
- `github_loader.py`: Loads repositories from GitHub
- `llm_agent.py`: Integrates with language models
- `markdown_writer.py`: Writes documentation in markdown format
- `repo_parser.py`: Parses entire repositories
- `scaledown.py`: (Purpose TBD)
- `webapp.py`: Web interface for the agent
- `templates/index.html`: HTML template for the web UI
- `requirements.txt`: Python dependencies

## Installation
1. Clone the repository:
   ```bash
   git clone <repo-url>
   cd Documentation-Generator-Agent
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage
- **Command Line:**
  ```bash
  python main.py <path-to-repo>
  ```
- **Web Interface:**
  ```bash
  python webapp.py
  ```
  Then open your browser to `http://localhost:5000`.

## Requirements
- Python 3.8+
- See `requirements.txt` for details

## License
MIT License

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## Acknowledgements
- OpenAI for LLM integration
- Python community for libraries and tools
