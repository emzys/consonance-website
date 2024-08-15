# Create a new virtual environment
pyenv virtualenv <YOUR_PYTHON_VERSION> taxifare-web

# Make this the default virtual environment for this repository
pyenv local taxifare-web

# Create a new requirements.txt for our project
touch requirements.txt

# Open our new project in VS Code
code .