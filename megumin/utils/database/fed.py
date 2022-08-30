from megumin import megux
from megumin.utils import get_collection
from pyrogram.types import Message

feds = get_collection("FEDERATION")

async def new_fed(m: Message, fed_name, fed_id, owner_id):
    GETFED = await feds.find_one({"owner_id": owner_id})
    if GETFED:
        await m.reply("Ei você já tem uma federação. Não é possivel criar outra renomeie a federação ou exclua a atual para criar outra.")
        return
    await feds.insert_one({"fed_name": fed_name, "fed_id": fed_id, "owner_id": owner_id})
    await m.reply(
        "*You have successfully created a new federation!*"
        "\nName: `{}`"
        "\nID: `{}`"
        "\n\nUse the command below to join the federation:"
        "\n`/joinfed {}`".format(fed_name, fed_id, fed_id)
        )
    await megux.send_log(f"Federation <b>{}</b> has been created with ID: <pre>{}</pre>".format(
                    fed_name, fed_id
        ),
    )
