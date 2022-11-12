import asyncio
import json

import socks
from loguru import logger
from telethon.errors import FloodWaitError, UsernameInvalidError
from telethon.errors.rpcerrorlist import (ChannelInvalidError,
                                          ChannelPrivateError,
                                          ChannelsTooMuchError)
from telethon.sessions import StringSession
from telethon.sync import TelegramClient, functions
from telethon.tl.functions.channels import JoinChannelRequest
from telethon.tl.functions.messages import SendReactionRequest
from telethon.tl.types import Updates


class TelegramTasks:
    def __init__(self, session_data: dict, group_url: str, post_id: int = 0, gender: str = "any",
                 count_last_posts: int = 0, count_per_post: int = 1
                 ) -> None:
        self.gender = gender
        self.session_data = session_data
        self.group_url = group_url
        self.post_id = post_id
        self.count_last_posts = count_last_posts
        self.count_per_post = count_per_post

    def create_session_instance(self):
        """Проверяем и возвращаем инстанс сессии, иначе ничего."""
        client = TelegramClient(
            StringSession(str(self.session_data["auth_string"])),
            self.session_data["app_id"],
            self.session_data["app_hash"]
            #proxy=(socks.HTTP, "212.81.37.87", 9826, True, "KvT99V", "9dBtwZ"),
        )

        try:
            is_connect = client.connect()
        except ConnectionError:
            logger.debug("CANT REACH PROXY server")
            return
        if not client.is_user_authorized():
            return

        return client


class ViewTaskObject(TelegramTasks):
    def increase_post_views_count(self):
        """Накручиваем просмотры на объявление"""
        client = self.create_session_instance()
        if client:
            try:
                status =  client(
                    functions.messages.GetMessagesViewsRequest(
                        peer=self.group_url, id=[self.post_id], increment=True
                    )
                )

                if int(status.views[0].views) >= 1:
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
            except Exception as e:
                return False 


class SubscribeTaskObject(TelegramTasks):
    def subscribe_to_channel(self):
        client = self.create_session_instance()
        if client:
            try:
                status =  client(JoinChannelRequest(channel=self.group_url))
                logger.debug(status)
                if isinstance(status, Updates):
                    return True
            except (
                ChannelsTooMuchError,
                ValueError,
                FloodWaitError,
                ChannelInvalidError,
                UsernameInvalidError,
                ChannelPrivateError,
            ):
                return False
            except Exception as e:
                return False
                
            return True
        else:
            return False