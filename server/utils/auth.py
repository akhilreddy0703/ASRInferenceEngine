from fastapi import Header, HTTPException

async def get_api_key(authorization: str = Header(None)):
    if not authorization:
        raise HTTPException(status_code=401, detail="API Key is missing")
    
    scheme, _, token = authorization.partition(" ")
    if scheme.lower() != "bearer":
        raise HTTPException(status_code=401, detail="Invalid authentication scheme")
    
    if not token:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    return token