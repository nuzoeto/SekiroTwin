from megumin.utils import get_collection

from typing import Optional


async def csdl(gid: int) -> bool:
    CSDL = get_collection(f"MEDIAS")
    resp = await CSDL.find_one({"chat_id": gid, "status": True})
    return bool(resp)

async def tsdl(gid: int, mode: Optional[bool]) -> None:
    CSDL = get_collection(f"MEDIAS") 
    await CSDL.update_one({"chat_id": gid}, {"$set": {"status": mode}}, upsert=True)  
    
async def cisdl(gid: int) -> bool:
    CISDL = get_collection(f"CAPTION_SDL")
    row = await CISDL.find_one({"status": True})
    return bool(row)

async def tisdl(gid: int, mode: Optional[bool]) -> None:
    CISDL = get_collection(f"CAPTION_SDL")
    await CSDL.update_one({"chat_id": gid}, {"$set": {"status": mode}}, upsert=True)
    
