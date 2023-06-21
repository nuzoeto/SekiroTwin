from megumin.utils import get_collection

db = get_collection("FLOOD_MSGS")

async def rflood():
    #Deleta as informaçoes anteriores
    await db.drop()
