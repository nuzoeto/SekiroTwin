from megumin.utils import get_collection


async def is_disabled(gid: int, query: str) -> bool:
    DISABLED = get_collection(f"DISABLED {gid}")
    off = await DISABLED.find_one({"_cmd": query})
    return bool(off)


async def is_disabled_user(gid: int, query: str) -> bool:
    DISABLED = get_collection(f"DISABLED_USER")
    off = await DISABLED.find_one({"user_id": gid, "_cmd": query})
    return bool(off)
