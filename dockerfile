FROM python:3.10.12

WORKDIR /SteamTables

COPY . /SteamTables/

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Specify the command to run your application
CMD ["python", "steam_demo.py"]