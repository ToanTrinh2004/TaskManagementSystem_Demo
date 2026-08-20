from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import uuid


from app.core.sercurity import decode_token
from app.db.session import get_db
from app.modules.users.repository import UserRepository


bearer_scheme = HTTPBearer()

async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme), db=Depends(get_db)):
    token = credentials.credentials
    try:
        payload = decode_token(token)
    except:
        raise HTTPException(status_code=401, detail="Invalid Token")

    user_id = payload.get("sub")
    repo = UserRepository(db)
    user = await repo.get_by_id(uuid.UUID(user_id))
    if user is None:
        raise HTTPException(status_code=401, detail="User Not Found")

    return user