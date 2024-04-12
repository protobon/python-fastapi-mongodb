from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi import Depends, HTTPException, status
from firebase_admin import auth
from app.common.config import Config


def get_user(cred: HTTPAuthorizationCredentials = Depends(HTTPBearer(auto_error=False))) -> dict:
    config = Config()

    # default firebase app
    _app = config.firebase_app

    if cred is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Bearer authentication required",
            headers={'WWW-Authenticate': 'Bearer realm="auth_required"'},
        )
    try:
        _credentials_ = cred.credentials.replace('Bearer ', '')
        decoded_token: dict = auth.verify_id_token(_credentials_, app=_app)
    except Exception as err:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Invalid authentication credentials. {err}",
            headers={'WWW-Authenticate': 'Bearer error="invalid_token"'},
        )

    return decoded_token
