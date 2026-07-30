from fastapi.testclient import TestClient
from src import app

payload = {
    "email": "\rÄ",
    "first_name": "f4",
    "last_name": "ã\ud98f\udf16%Òç",
    "password": "\ud835\udd4b\ud835\udd59\ud835\udd56 \ud835\udd62\ud835\udd66\ud835\udd5a\ud835\udd54\ud835\udd5c \ud835\udd53\ud835\udd63\ud835\udd60\ud835\udd68\ud835\udd5f \ud835\udd57\ud835\udd60\ud835\udd69 \ud835\udd5b\ud835\udd66\ud835\udd5e\ud835\udd61\ud835\udd64 \ud835\udd60\ud835\udd67\ud835\udd56\ud835\udd63 \ud835\udd65\ud835\udd59\ud835\udd56 \ud835\udd5d\ud835\udd52\ud835\udd6b\ud835\udd6a \ud835\udd55\ud835\udd60\ud835\udd58",
    "username": "",
    "¢x*ÒÚÁÇuè\uda0d\udc6cÉ\u009dô": {"NUL": {"\udba3\udd76D": [[17977868], [True], {}]}},
    "Ä¿û": {"/@\n\x10\u0094H": -12090, "": "ê\ud924\udefb©=Âð\x11\ud8c6\udffa\ud816\ude83\u009f\u0090;\x80Æ$%\ud950\uddf1\ud962\udf67úÀh"},
    "": [],
}

client = TestClient(app)
resp = client.post('/api/v1/auth/signup', json=payload)
print('status', resp.status_code)
print(resp.text)
