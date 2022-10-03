from megumin import megux
from megumin.utils import get_collection

async def add_user_count(chat_id: int, user_id: int):
    add_groups = get_collection(f"TOTAL_GROUPS")
    try:
        if not await add_groups.find_one({"user_id": user_id, "chat_id": chat_id}):
            await add_groups.insert_one({"user_id": user_id, "chat_id": chat_id})
    except Exception as e:
        await send_log(e)
        pass

async def count_groups_user(user_id: int):
    count_groups = get_collection(f"TOTAL_GROUPS")
    num = await count_groups.count_documents({"user_id": user_id})
    return num

async def del_user_count(chat_id: int, user_id: int):
    add_groups = get_collection(f"TOTAL_GROUPS")
    try:
        if await add_groups.find_one({"user_id": user_id, "chat_id": chat_id}):
            await add_groups.delete_one({"user_id": user_id, "chat_id": chat_id})
    except Exception as e:
        await send_log(e)
        pass

async def drop_info(user_id: int):
    gps = get_collection(f"TOTAL_GROUPS {user_id}")
    dbs = get_collection(f"WARMS {user_id}")
    await gps.drop()
    await dbs.drop()
