# Don't Remove Credit @VJ_Botz
# Subscribe YouTube Channel For Amazing Bot @Tech_VJ
# Ask Doubt on telegram @KingVJ01

import logging
from pyrogram import Client, filters
from info import CHANNELS, REQUEST_TO_JOIN_MODE, AUTH_CHANNEL, AUTH_CHANNEL_2
from database.ia_filterdb import save_file
from database.join_reqs import JoinReqs

logger = logging.getLogger(__name__)
media_filter = filters.document | filters.video

@Client.on_message(filters.chat(CHANNELS) & media_filter)
async def media(bot, message):
    media = getattr(message, message.media.value, None)
    media.caption = message.caption
    await save_file(media)

@Client.on_chat_join_request()
async def save_join_req(client, request):
    """
    Catches when a user clicks 'Request to Join' on your channels
    and saves them directly into your database.
    """
    if REQUEST_TO_JOIN_MODE:
        try:
            join_db = JoinReqs()
            user_id = request.from_user.id
            first_name = request.from_user.first_name
            username = request.from_user.username
            date = request.date
            chat_id = request.chat.id

            # Only track if it belongs to your FSub channels
            if chat_id in [AUTH_CHANNEL, AUTH_CHANNEL_2]:
                await join_db.add_user(
                    user_id=user_id,
                    first_name=first_name,
                    username=username,
                    date=date
                )
                logger.info(f"Saved Join Request for user {user_id} in channel {chat_id}")
        except Exception as e:
            logger.error(f"Error saving chat join request: {e}")
