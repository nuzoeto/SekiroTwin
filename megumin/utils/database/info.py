from megumin.utils import get_collection

async def add_user_count(chat_id, user_id):
    count_groups = get_collection(f"TOTAL_GROUPS {user_id}")
    if not await count_groups.find_one({"chat_id": chat_id}):
        await count_groups.find_one({"chat_id": chat_id})
