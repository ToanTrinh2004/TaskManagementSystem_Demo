from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import uuid

from app.core.sercurity import decode_token
from app.db.redis_client import get_redis
from app.db.session import get_db
from app.modules.users.repository import UserRepository


bearer_scheme = HTTPBearer()

async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
    db=Depends(get_db),
    redis_client=Depends(get_redis),
):
    token = credentials.credentials
    try:
        payload = decode_token(token)
    except:
        raise HTTPException(status_code=401, detail="Invalid Token")

    is_blacklist = await redis_client.get(f"blacklist:{token}")
    if is_blacklist:
        raise HTTPException(status_code=401, detail="Token was revoke")

    user_id = payload.get("sub")
    repo = UserRepository(db)
    user = await repo.get_by_id(uuid.UUID(user_id))
    if user is None:
        raise HTTPException(status_code=401, detail="User Not Found")

    return user