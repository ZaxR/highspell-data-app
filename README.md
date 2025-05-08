# Run locally
python download_data.py
python load_data.py
python run.py
http://localhost:8080


# Some UV nonsense while using pyenv virtualenvs
uv init --python $(which python)
uv pip install -r pyproject.toml
uv lock --python $(which python)