from megumin import megux
from megumin.utils import get_collection
from pyrogram.types import Message

feds = get_collection("FEDERATION")
federation = get_collection("FEDERATION_GROUP")

async def new_fed(m: Message, fed_name, fed_id, owner_id):
    GETFED = await feds.find_one({"owner_id": owner_id})
    if GETFED:
        await m.reply("Ei você já tem uma federação. Não é possivel criar outra renomeie a federação ou exclua a atual para criar outra.")
        return
    x = await feds.insert_one({"fed_name": fed_name, "fed_id": fed_id, "owner_id": owner_id})
    if not x:
        await m.reply("Can't federate! Report in @DaviTudo if the problem persists.")
        return
    await m.reply(
        "*You have successfully created a new federation!*"
        "\nName: `{}`"
        "\nID: `{}`"
        "\n\nUse the command below to join the federation:"
        "\n`/joinfed {}`".format(fed_name, fed_id, fed_id)
        )
    await megux.send_log("Federation <b>{}</b> has been created with ID: <pre>{}</pre>".format(
                    fed_name, fed_id
        ),
    )

    
async def join_fed(chat_id, chat_title, fed_id):
    await federation.update_one(
        {
            'fed_id': fed_id
        },
        {
            "$addToSet": {
                'chats': {
                    "$each": [
                        {
                            'chat_id': chat_id,
                            'chat_title': chat_title
                        }
                    ]
                }
            }
        }
    )
    
async def leave_fed(chat_id, chat_title, fed_id):
    await federation.update(
        {
            'fed_id': fed_id
        },
        {
             "$remove": {
                'chats': {
                    "$pull": [
                        {
                            'chat_id': chat_id  ,
                            'chat_title': chat_title
                        }
                    ]
                }
            }
        }
    )
   
async def user_fban(fed_id, user_id, reason):
    await feds.update(
        {
            'fed_id': fed_id
        },
        {
            "$set": {
                'banned_users': [
                    {
                        'user_id': user_id,
                        'reason': reason
                    }
                ]
            }
        }
    )

    
async def is_user_fban(fed_id, user_id) -> bool:
    GetFed = await feds.find_one(
        {
            'fed_id': fed_id
        }
    )

    user_ids_list = []
    if not GetFed == GetFed:
        if 'banned_users' in GetFed:
            for users in GetFed['banned_users']:
                banned_user = users['user_id']
                user_ids_list.append(banned_user)
            if user_id in user_ids_list:
                return True 
            else:
                return False 
        else:
            return False 
    else:
        return False 
    
async def update_reason(fed_id, user_id, new_reason):
    await federation.update_one(
        {
            'fed_id': fed_id,
            'banned_users.user_id': user_id
        },
        {
            "$set": {
                'banned_users.$.reason': new_reason
            }
        },
        False,
        True
    )

    
def get_fed_from_chat(chat_id):
    for fedData in federation.find(
        {
            'chats': {
                "$elemMatch": {
                    'chat_id': chat_id
                }
            }
        }
    ):  
        if 'fed_id' in fedData:
            fed_id = fedData['fed_id']
            return fed_id
        else:
            return None
