from fastapi import Depends, HTTPException

from apps.token.services import authenticate
from apps.user.services import get_user


async def get_current_active_user(pk: int, user: dict = Depends(authenticate)) -> dict or None:
    """ Get current active user"""

    current_user = await get_user(pk=pk)
    if current_user is not None:
        if current_user['is_active']:
            if user is not None and user.get('id') == current_user['id']:
                return current_user
            raise HTTPException(status_code=403, detail='You have not permissions')
        raise HTTPException(status_code=403, detail='User didnt active. Check your email')
    raise HTTPException(status_code=404, detail='User not found')
