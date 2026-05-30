import sys
from pathlib import Path

# Ensure project root is on sys.path so `src` can be imported
project_root = str(Path(__file__).resolve().parents[1])
if project_root not in sys.path:
	sys.path.insert(0, project_root)

from fastapi.testclient import TestClient
from src import app

client = TestClient(app)
resp = client.get('/api/0.1.0/books/')
print('STATUS', resp.status_code)
print(resp.text)
