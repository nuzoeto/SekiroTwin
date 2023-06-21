from megumin.utils import get_collection

DB = get_collection("FLOOD_MSGS")

async def drop_flood():
  # Deletar Todas as Mensagens Guardadas Anteriormente
  await DB.drop()
