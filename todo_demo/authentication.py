from fastapi import HTTPException, status, Depends
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from passlib.context import CryptContext


security = HTTPBasic()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str):
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)

#######################################################################################################################
# User moch database will encrypt the passwords in the next steps
user_mock_db = {
    'admin': {'username': 'admin', 'password': ''},
    'username1': {'username': 'username1', 'password': ''},
}

for usr in user_mock_db:
    user_mock_db[usr]['password'] = hash_password('password123')
    print('User Hashed Password: ', user_mock_db[usr]['password'])

#######################################################################################################################

def authenticate(credentials: HTTPBasicCredentials = Depends(security)):
    user = user_mock_db.get(credentials.username)

    if not user or not verify_password(credentials.password, user['password']):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Incorect username or password',
            headers={'WWW-Authenticate': 'Basic'}
        )
    return user
