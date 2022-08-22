from megumin.utils import get_collection

feds = get_collection("FEDERATION")

async def new_fed_db(new_fed, fed_id, created_time, owner_id):
    GETFED = await feds.find_one({"owner_id": owner_id})
