from dotenv import load_dotenv
from os import environ

load_dotenv()

# gets API key from environment variables
def getKey(nameOfKey):
    return environ[nameOfKey]
