from megumin.utils import get_collection

from typing import Optional


async def csdl(id: int) -> bool:
    CSDL = get_collection(f"CSDL {id}")
    resp = await CSDL.find_one({"status": True})
    if resp:
        row = True
    else:
        row = False
    return row[0]

async def tsdl(id: int, mode: Optional[bool]) -> None:
    CSDL = get_collection(f"CSDL {id}") 
    await CSDL.drop()
    await CSDL.insert_one({"status": mode})
    
    
async def cisdl(id: int) -> bool:
    CISDL = get_collection(f"CISDL {id}")
    row = await CISDL.find_one({"status": True})
    return row[0]

async def tisdl(id: int, mode: Optional[bool]) -> None:
    CISDL = get_collection(f"CISDL {id}")
    await CISDL.drop()
    await CISDL.insert_one({"status": mode})
