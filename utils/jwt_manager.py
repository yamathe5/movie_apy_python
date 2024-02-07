from jose import jwt, JWTError

def create_token(data: dict) -> str:
    token:str = jwt.encode(data, key="My secret key", algorithm="HS256")
    return token

def validate_token(token: str) -> dict:
    data:dict = jwt.decode(token, key="My secret key", algorithms=["HS256"])
    return data
    