from fastapi import Depends, HTTPException, Query
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import Optional

from security import verify_access_token

security_scheme = HTTPBearer(auto_error=False)

def get_current_user(

    credentials: Optional[HTTPAuthorizationCredentials] = Depends(security_scheme),

    token: Optional[str] = Query(None)

):

    if credentials:

        jwt_token = credentials.credentials

    elif token:

        jwt_token = token

    else:

        raise HTTPException(
            status_code=401,
            detail="Not authenticated"
        )

    payload = verify_access_token(jwt_token)

    if payload is None:

        raise HTTPException(
            status_code=401,
            detail="Invalid token"
        )

    return payload