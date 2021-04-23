import asyncio
import os
import pickle
from typing import List, Set, Tuple

import nonebot
from nonebot import logger, Bot

from .config import plugin_config
from .illustration import IllustrationBase, IllustrationLocal


class SenderBase(object):

    already_sent: Set[Tuple[str, str]]
    illustrations: List[IllustrationLocal]
    tgt_groups: List[str]
    tgt_members: List[str]

    def __init__(self, prefix: str):
        self.already_sent_filepath = os.path.join(plugin_config.cachepath, f".{prefix}already_sent.pkl")
        if os.path.exists(self.already_sent_filepath):
            self.already_sent = pickle.load(open(self.already_sent_filepath, 'rb'))
        else:
            self.already_sent = set()
        self.illustrations = []
        for filepath in os.listdir(plugin_config.cachepath):
            if filepath.startswith(prefix):
                ill_filepath = os.path.join(plugin_config.cachepath, filepath)
                self.illustrations.append(IllustrationLocal(ill_filepath))
        # todo
        # if plugin_config.use_mirai:
        #     # todo: mah 找图的时候默认会在 mcl/data/net.mirai.api.http/images 下找
        #     for filepath in os.listdir(plugin_config.mirai_images_path):
        #         if filepath.startswith(prefix):
        #             self.illustrations.append(IllustrationLocal(filepath))
        # else:
        #     for filepath in os.listdir(plugin_config.cachepath):
        #         if filepath.startswith(prefix):
        #             ill_filepath = os.path.join(plugin_config.cachepath, filepath)
        #             self.illustrations.append(IllustrationLocal(ill_filepath))

    async def _send(self, bot: Bot, type: str, tgt: str, ill: IllustrationBase):
        if (tgt, ill.filepath) in self.already_sent:
            return

        if type == "friend":
            send_msg = bot.send_friend_message
        elif type == "group":
            send_msg = bot.send_group_message
        else:
            return

        fail_flag = True
        for _ in range(3):
            try:
                if plugin_config.use_mirai:
                    from nonebot.adapters.mirai.message import MessageChain, MessageSegment
                    image_id = bot.upload_image(type=type, img=open(ill.filepath, "wb"))
                    await send_msg(tgt, MessageChain(MessageSegment.image(image_id=image_id)))    # mirai-api-http
                else:
                    await send_msg(tgt, f"[CQ:image,file={ill.encode()}]")        # cq-http
            except:
                await asyncio.sleep(2)
            else:
                logger.log("DEBUG", f"Succeeded to send {ill.filepath} to \"{tgt}\"")
                self.already_sent.add((tgt, ill.filepath))
                pickle.dump(self.already_sent, open(self.already_sent_filepath, 'wb'))
                fail_flag = False
                break
        if fail_flag:
            logger.log("DEBUG", f"Failed to send {ill.filepath} to \"{tgt}\"")

    async def run(self):
        bot = nonebot.get_bots()[plugin_config.bot_id]
        for illustration in self.illustrations:
            for group_id in self.tgt_groups:
                await self._send(bot, "group", group_id, illustration)
            for member_id in self.tgt_members:
                await self._send(bot, "friend", member_id, illustration)
