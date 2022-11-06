import asyncio
import json

import socks
from loguru import logger
from telethon.errors import FloodWaitError, UsernameInvalidError
from telethon.errors.rpcerrorlist import (
    ChannelInvalidError,
    ChannelPrivateError,
    ChannelsTooMuchError,
)
from telethon.sessions import StringSession
from telethon.sync import TelegramClient
from telethon.tl.functions.messages import SendReactionRequest
from telethon.tl.types import Updates


class TelegramTasks:
    def __init__(self, session_data: dict, gender: str = "any") -> None:
        self.gender = gender
        self.session_data = session_data

    def create_session_instance(self):
        """Проверяем и возвращаем инстанс сессии, иначе ничего."""
        client = TelegramClient(
            StringSession(self.session_data["string"]),
            self.session_data["app_id"],
            self.session_data["app_hash"],
            proxy=(socks.HTTP, "212.81.37.87", 9826, True, "KvT99V", "9dBtwZ"),
        )

        try:
            is_connect = client.connect()
        except ConnectionError:
            logger.debug("CANT REACH PROXY server")
            return
        if not client.is_user_authorized():
            return

        return client


""" class TasksList(TelegramTasks):
    async def send_reaction(
        session_data: dict,
        group_url: str,
        post_id: int,
        reaction: str,
        gender: str = "female",
    ) -> bool:
        # Отправляем реакцию
        client = await create_session_instance(session_data)
        if client:
            try:
                status = await client(
                    SendReactionRequest(
                        peer=group_url, msg_id=post_id, reaction=reaction
                    )
                )
                if isinstance(status, Updates):
                    return True
                else:
                    return False
            except (
                ChannelsTooMuchError,
                ValueError,
                FloodWaitError,
                ChannelInvalidError,
                UsernameInvalidError,
                ChannelPrivateError,
            ):
                return False
        else:
            return False """
