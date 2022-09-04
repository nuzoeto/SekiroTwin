from megumin import megux
from megumin.utils import get_collection

async def add_user_count(chat_id, user_id):
    add_groups = get_collection(f"TOTAL_GROUPS")
    try:
        if not await add_groups.find_one({"user_id": user_id, "chat_id": chat_id}):
            await add_groups.insert_one({"user_id": user_id, "chat_id": chat_id})
    except Exception as e:
        await send_log(e)
        pass

async def count_groups_user(user_id):
    count_groups = get_collection(f"TOTAL_GROUPS")
    num = 0
    async for count in count_groups.find({"user_id": user_id}):
        num += 1

async def del_user_count(chat_id, user_id):
    add_groups = get_collection(f"TOTAL_GROUPS")
    try:
        if await add_groups.find_one({"user_id": user_id, "chat_id": chat_id}):
            await add_groups.delete_one({"user_id": user_id, "chat_id": chat_id})
    except Exception as e:
        await send_log(e)
        pass
