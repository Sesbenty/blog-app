import os


base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
database_url = f"sqlite:///{base_dir}/data/db.sqlite3"

SECRET_KEY = os.environ.get("SECRET_KEY", "key")
ALGORITHM = os.environ.get("ALGORITHM", "HS256")
