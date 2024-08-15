# Create a new virtual environment
pyenv virtualenv <YOUR_PYTHON_VERSION> consonance-web

# Make this the default virtual environment for this repository
pyenv local consonance-web

# Install requirements
pip install -r requirements.txt