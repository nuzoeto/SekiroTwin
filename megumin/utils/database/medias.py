from megumin.utils import get_collection

from typing import Optional


async def csdl(ugid: int) -> bool:
    CSDL = get_collection(f"MEDIAS")
    resp = await CSDL.find_one({"chat_id": ugid, "status": True})
    return bool(resp)

async def tsdl(ugid: int, mode: Optional[bool]) -> None:
    CSDL = get_collection(f"MEDIAS") 
    await CSDL.update_one({"chat_id": ugid}, {"$set": {"status": mode}}, upsert=True)  
    
async def cisdl(ugid: int) -> bool:
    CISDL = get_collection(f"CAPTION_SDL")
    row = await CISDL.find_one({"chat_id": ugid, "status": True})
    return bool(row)

async def tisdl(ugid: int, mode: Optional[bool]) -> None:
    CISDL = get_collection(f"CAPTION_SDL")
    await CSDL.update_one({"chat_id": ugid}, {"$set": {"status": mode}}, upsert=True)
    
