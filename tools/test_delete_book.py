import sys
from pathlib import Path
project_root = str(Path(__file__).resolve().parents[1])
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from fastapi.testclient import TestClient
from src import app

client = TestClient(app)
# replace this UID with a valid one from your DB if needed
uid = '79b28380-40aa-4af4-8917-ef93c17b4718'
resp = client.delete(f'/api/0.1.0/books/{uid}')
print('STATUS', resp.status_code)
print(resp.text)
