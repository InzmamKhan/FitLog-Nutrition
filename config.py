import os

def load_env():
    """Manually parses the local .env file into os.environ to keep dependencies light."""
    env_path = os.path.join(os.path.dirname(__file__), '.env')
    if os.path.exists(env_path):
        with open(env_path, 'r') as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith('#') or '=' not in line:
                    continue
                key, val = line.split('=', 1)
                os.environ[key.strip()] = val.strip()

load_env()
DB_HOST = os.environ["DB_HOST"]
DB_USER = os.environ["DB_USER"]
DB_PASSWORD = os.environ["DB_PASSWORD"]
DB_NAME = os.environ["DB_NAME"]

FLASK_SECRET_KEY = os.environ.get("SECRET_KEY", "fitlog_nutrition_local_secret_secure_key_123")
DEFAULT_STEP_GOAL = 10000