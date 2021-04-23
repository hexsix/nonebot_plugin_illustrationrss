import os
import re
from typing import List, Dict

import nonebot
from nonebot import logger

from .config import plugin_config
from .downloader import DownloaderBase
from .illustration import IllustrationBase
from .rss import RssBase
from .sender import SenderBase

scheduler = nonebot.require("nonebot_plugin_apscheduler").scheduler


class YandeRePopularRecentIllustration(IllustrationBase):
    post_url: str
    score: int
    rating: str

    def __init__(self, entry: Dict):
        # https://yande.re/post/show/xxxxxx
        self.post_url = entry['link']
        #
        self.id = self.post_url.split('/')[-1]
        # score
        self.score = int(re.search(r'Score:\d*', entry['description']).group().split(':')[-1])
        # s: safe, q: questionable, e: explicit
        self.rating = re.search(r'Rating:.', entry['description']).group().split(':')[-1]
        # https://files.yande.re/sample/xxxx.../xxxx...
        self.illustration_link = re.search(r'https://files.yande.re/sample/[^"]*', entry['description']).group()
        # filename
        self.filename = f"yande_re_popular_recent_{self.id}.jpg"
        # filepath
        self.filepath = os.path.join(plugin_config.cachepath, self.filename)
        # todo
        # if plugin_config.use_mirai:
        #     self.filepath = os.path.join(plugin_config.mirai_images_path, self.filename)
        # else:
        #     self.filepath = os.path.join(plugin_config.cachepath, self.filename)


class YandeRePopularRecentRss(RssBase):

    def __init__(self):
        self.rss_url = "https://rsshub.app/yande.re/post/popular_recent"

    def parse(self) -> List[YandeRePopularRecentIllustration]:
        illustrations = []
        for entry in self.rss_json["entries"]:
            try:
                illustration = YandeRePopularRecentIllustration(entry)
                if illustration.score < plugin_config.yande_re_popular_recent_score_threshold:
                    continue
                illustrations.append(illustration)
            except:
                continue
        return illustrations


class YandeRePopularRecentDownloader(DownloaderBase):
    rss: YandeRePopularRecentRss
    illustrations: List[YandeRePopularRecentIllustration]
    use_salt: bool = True

    def __init__(self):
        self.rss = YandeRePopularRecentRss()


class YandeRePopularRecentSender(SenderBase):
    def __init__(self):
        super().__init__("yande_re_popular_recent")
        self.tgt_members = plugin_config.yande_re_popular_recent_tgt_members
        self.tgt_groups = plugin_config.yande_re_popular_recent_tgt_groups


if plugin_config.yande_re_popular_recent_enable:
    @scheduler.scheduled_job("cron", hour="10", minute="10", id="yande_re_popular_recent_downloader")
    async def yande_re_popular_recent_downloader():
        yande_re_popular_recent_config = {"use_proxy": plugin_config.use_proxy,
                                          "proxies": plugin_config.proxies,
                                          "score_threshold": plugin_config.yande_re_popular_recent_score_threshold
                                          }
        logger.log("DEBUG", f"Loaded Config: {str(yande_re_popular_recent_config)}")
        await YandeRePopularRecentDownloader().run()

    @scheduler.scheduled_job("cron", hour="*", minute="*", id="yande_re_popular_recent_sender")
    async def yande_re_popular_recent_sender():
        await YandeRePopularRecentSender().run()
