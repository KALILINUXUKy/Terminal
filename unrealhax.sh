mkdir -p .devcontainer
cat <<EOL > .devcontainer/devcontainer.json
{
    "name": "My Codespace",
    "image": "mcr.microsoft.com/vscode/devcontainers/python:3.8",
    "postStartCommand": "/bin/bash -c 'chmod +x * && \
        pip install --upgrade python-telegram-bot && \
        pip install telebot && \
        pip install flask && \
        pip install aiogram && \
        pip install aiohttp && \
        python3 unrealhax.py'",
    "customizations": {
        "vscode": {
            "settings": {
                "python.pythonPath": "/usr/local/bin/python"
            },
            "extensions": [
                "ms-python.python"
            ]
        }
    }
}
EOL