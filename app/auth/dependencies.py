import jwt

from fastapi import HTTPException, status, Depends, Request

from app.auth.utils import SECRET


def get_current_user(
    request: Request,
):
    credentials_exception = HTTPException(
        status.HTTP_401_UNAUTHORIZED, 
        'Required login'
    )  
    token = request.cookies.get('jwt_token')
    if not token:
        raise credentials_exception
    try:     
        token = jwt.decode(token, SECRET, algorithms='HS256')
    except jwt.exceptions.ExpiredSignatureError:
        raise credentials_exception
    else:
        user = token.get('user_id')
    if user:
        return {'user_id': user}
    enter = token.get('enter_id')
    return {'enter_id': enter}


def get_anonym_user(request: Request):
    token = request.cookies.get('jwt_token')
    if token:
        raise HTTPException(
            status.HTTP_400_BAD_REQUEST,
            'You cant register/login while you are logged in',
        )
    

current_user = Depends(get_current_user)
anonym_user = Depends(get_anonym_user)