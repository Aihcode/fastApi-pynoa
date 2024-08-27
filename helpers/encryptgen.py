from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_hashed_name(name):
    return str(pwd_context.hash(name)).replace('$', 'img_').replace('/', '').replace('.', 'plus')

def get_hashed_token(token):
    return str(pwd_context.hash(token))