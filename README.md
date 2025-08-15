
# GitHub Activity Analyzer

A Python tool that analyzes GitHub repository activity using the GitHub REST API.  
It fetches commit, issue, and contributor data for one or more repositories and visualizes trends with Pandas and Matplotlib.

## Features
- Weekly commit trends per repository
- Issues opened vs closed trends
- Contributor statistics
- Handles API pagination and rate limits
- Configurable via `config.yaml`

## Tech Stack
- Python 3
- Requests – GitHub API integration
- Pandas – Data processing
- Matplotlib – Data visualization
- PyYAML – Config file handling
- python-dotenv – Secure token management

## Setup & Installation

1. Clone the repository
   ```bash
   git clone https://github.com/USERNAME/github-activity-analyzer.git
   cd github-activity-analyzer
   ```

2. Create a virtual environment

   ```bash
   python -m venv .venv
   source .venv/bin/activate   # Mac/Linux
   .venv\Scripts\activate      # Windows
   ```

3. Install dependencies

   ```bash
   pip install -r requirements.txt
   ```

   Or install manually:

   ```bash
   pip install requests pandas matplotlib tenacity python-dotenv pyyaml
   ```

4. Create `.env` file (store your GitHub token)

   ```env
   GITHUB_TOKEN=ghp_your_token_here
   ```

5. Edit `config.yaml`

   ```yaml
   repos:
     - psf/requests
     - numpy/numpy
   since: "2024-01-01T00:00:00Z"
   ```

6. Run the analyzer

   ```bash
   python main.py
   ```

## Example Output

### Weekly Commits Chart

![Commits Chart](docs/example_commits.png)

### Issues Opened vs Closed

![Issues Chart](docs/example_issues.png)

## Roadmap

* [ ] Add Pull Request analytics
* [ ] Export results to CSV/Excel
* [ ] Build an interactive dashboard (Streamlit/Dash)
* [ ] Support GitHub GraphQL API

## License

This project is open source and available under the MIT License.
