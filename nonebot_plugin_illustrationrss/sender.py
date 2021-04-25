import asyncio
import base64
import os
import pickle
from typing import List, Set, Tuple

import nonebot
from nonebot import logger, Bot

from .config import Config


def encode(filepath: str) -> str:
    """ convert image to base64 """
    assert filepath is not None
    with open(filepath, 'rb') as f:
        return "base64://" + base64.b64encode(f.read()).decode('utf-8')


class BaseSender(object):

    config: Config
    already_sent: Set[Tuple[str, str, str]]
    not_sent: Set[Tuple[str, str, str]]
    illustrations_paths: List[str]

    def __init__(self,  config: Config, prefix: str):
        self.config = config
        # read already_sent.pkl
        self.already_sent_filepath = os.path.join(self.config.cachepath, f".{prefix}_already_sent.pkl")
        if os.path.exists(self.already_sent_filepath):
            self.already_sent = pickle.load(open(self.already_sent_filepath, 'rb'))
        else:
            self.already_sent = set()
        # walk illustrations
        self.illustrations_paths = []
        if config.use_mirai:
            # mah 找图的时候默认会在 mcl/data/net.mirai.api.http/images 下找，所以不要完整的路径
            for filename in os.listdir(config.mirai_images_path):
                if filename.startswith(prefix):
                    self.illustrations_paths.append(filename)
        else:
            for filename in os.listdir(config.cachepath):
                if filename.startswith(prefix):
                    filepath = os.path.join(config.cachepath, filename)
                    self.illustrations_paths.append(filepath)
        # filter illustrations
        self.not_sent = set()
        for filepath in self.illustrations_paths:
            for member in self.config.target_members:
                three = ("friend", member, filepath)
                if three not in self.already_sent:
                    self.not_sent.add(three)
            for group in self.config.target_groups:
                three = ("group", group, filepath)
                if three not in self.already_sent:
                    self.not_sent.add(three)

    async def _send(self, bot: Bot, three):
        func_type, target, filepath = three[0], three[1], three[2]
        if func_type == "friend":
            send_msg = bot.send_friend_message
        elif func_type == "group":
            send_msg = bot.send_group_message
        else:
            return

        fail_flag = True
        err_msg = ""
        for _ in range(3):
            try:
                if self.config.use_mirai:
                    from nonebot.adapters.mirai.message import MessageChain, MessageSegment
                    await send_msg(target, MessageChain(MessageSegment.image(path=filepath)))   # mirai-api-http
                else:
                    await send_msg(target, f"[CQ:image,file={encode(filepath)}]")               # cq http
            except Exception as e:
                err_msg = str(e)
                await asyncio.sleep(2)
            else:
                logger.log("DEBUG", f"Succeeded to send {filepath} to \"{target}\"")
                self.already_sent.add(three)
                pickle.dump(self.already_sent, open(self.already_sent_filepath, 'wb'))
                fail_flag = False
                break
        if fail_flag:
            logger.log("DEBUG", f"Failed to send {filepath} to \"{target}\": {err_msg}")

    async def run(self):
        bot = nonebot.get_bots()[self.config.bot_id]
        for three in self.not_sent:
            await self._send(bot, three)
