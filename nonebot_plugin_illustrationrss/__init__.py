import asyncio
import os
import glob
import pickle
import platform
from pathlib import Path

import nonebot
from nonebot import on_command
from nonebot.rule import to_me
from nonebot.adapters.cqhttp import Bot, Message, Event
from nonebot.adapters.cqhttp.message import MessageSegment
from nonebot.log import logger

from .yande_re_pop_recent import yande_re_popular_recent_config as yrpr_config


super_user = nonebot.get_driver().config.superusers
scheduler = nonebot.require("nonebot_plugin_apscheduler").scheduler

if platform.system() == "Windows":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())


""" Yande.re Popular Recent Section Start """

if yrpr_config.enable:
    """ 1. Download Section """
    from .yande_re_pop_recent import YandeRePopularRecentDownloader

    @scheduler.scheduled_job("cron", hour="*", minute="*/7", id="yande_re_popular_recent_downloader")
    async def yande_re_popular_recent_downloader():
        await YandeRePopularRecentDownloader().run(yrpr_config)

    """ 2. Send Section """
    from .yande_re_pop_recent import YandeRePopularRecentSender
    from nonebot_plugin_rauthman import isInService
    yande_re_pop_recent = on_command("yrpr", rule=isInService('yande_re_pop_recent', 1))

    @yande_re_pop_recent.handle()
    async def _(bot: Bot, event: Event):
        sender = YandeRePopularRecentSender()
        event_dict = event.normalize_dict()
        if event_dict["type"] == "GroupMessage":
            already_sent = set()
            not_send_list = sender.not_send_list(event_dict["sender"]["group"]["id"])
            if len(not_send_list) == 0:
                await yande_re_pop_recent.send("已经一滴也没有了，下个整点再来吧")
                return
            not_send_list_cut = not_send_list[:6]
            for img_name in not_send_list_cut:
                fail_flag = True
                for __ in range(3):
                    try:
                        await yande_re_pop_recent.send(f"file:///{Path(yrpr_config.cache_dir).resolve().joinpath(img_name)}")
                    except Exception as e:
                        logger.log("DEBUG", f"Failed to send {img_name}: {e}")
                        await asyncio.sleep(2)
                    else:
                        logger.log("DEBUG", f"Succeeded to send {img_name}")
                        already_sent.add(img_name)
                        fail_flag = False
                        break
                if fail_flag:
                    await yande_re_pop_recent.send(f"Failed to send {img_name}")
            await yande_re_pop_recent.send(f"本次发送 {len(not_send_list_cut)} 张图片，"
                                           f"还有 {len(not_send_list) - len(not_send_list_cut)} 张图片")
            sender.save_sent(event_dict["sender"]["group"]["id"], already_sent)
        elif event_dict["type"] == "PrivateMessage":
            await yande_re_pop_recent.send("Private Message Not Support")
            return

    download = on_command("rss")


""" Yande.re Popular Recent Section End """



