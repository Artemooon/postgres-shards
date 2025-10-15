import hashlib
import base64
from fastapi import APIRouter, Depends, HTTPException

from db_connection import get_db_connector
from shard_hashing import db_hr

urls_router = APIRouter()


@urls_router.get("/{url_id}")
async def get_url(url_id: str, get_connection=Depends(get_db_connector)):

    db_server_port = db_hr.get(url_id)["hostname"]
    conn = await get_connection(db_server_port)

    try:
        url_data = await conn.fetchrow("SELECT URL, URL_ID FROM url_table WHERE URL_ID=$1", url_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"DB insert failed: {str(e)}")
    finally:
        await conn.close()

    if not url_data:
        raise HTTPException(status_code=404, detail=f"Url with id: {url_id} was not found")

    return {
        "url_id": url_data.get("url_id"),
        "url": url_data.get("url"),
        "server": db_hr.get(url_id)
    }

@urls_router.post("")
async def create_url(full_url: str, get_connection=Depends(get_db_connector)):
    hash_bytes = hashlib.sha256(full_url.encode('utf-8')).digest()

    base64_hash = base64.b64encode(hash_bytes).decode('utf-8')
    url_id = base64_hash[0:5]
    db_server_port = db_hr.get(url_id)["hostname"]

    conn = await get_connection(db_server_port)

    try:
        await conn.execute("INSERT INTO url_table (URL, URL_ID) VALUES($1, $2)", full_url, url_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"DB insert failed: {str(e)}")

    return {
        "url_id": url_id,
        "url": full_url,
        "server": db_hr.get(url_id)
    }
