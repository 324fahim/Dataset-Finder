import os, pathlib

files = {
"requirements.txt": """streamlit==1.39.0
pandas==2.2.3
httpx==0.27.2
pydantic==2.9.2
pydantic-settings==2.5.0
python-dotenv==1.0.1
PyYAML==6.0.2
""",
".env.example": """ANTHROPIC_API_KEY=
OPENAI_API_KEY=
GITHUB_TOKEN=
HF_TOKEN=
KAGGLE_USERNAME=
KAGGLE_KEY=
MAX_DOWNLOAD_MB=500
ALLOWED_DOWNLOAD_HOSTS=huggingface.co,zenodo.org,api.openml.org,github.com,raw.githubusercontent.com,dataverse.harvard.edu,api.worldbank.org
""",
".gitignore": """venv/
.env
__pycache__/
*.db
downloads/
.streamlit/
""",
"config.yaml": """ranking_weights:
  semantic_relevance: 0.40
  documentation_quality: 0.15
  accessibility: 0.15
  format_size_match: 0.15
  recency: 0.10
  license: 0.05
cache_ttl_seconds: 600
"""
}

# Add all other files - for space I will create them via engine
for path, content in files.items():
    pathlib.Path(path).write_text(content, encoding="utf-8")
    print(f"Created {path}")

print("Now run: pip install -r requirements.txt")