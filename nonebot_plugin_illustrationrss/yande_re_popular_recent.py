import os
import re
from typing import List, Dict, Any

import nonebot

from .config import Config
from .downloader import BaseDownloader
from .illustration import BaseIllustration
from .rss import BaseRss
from .sender import BaseSender

scheduler = nonebot.require("nonebot_plugin_apscheduler").scheduler


class YandeRePopularRecentConfig(Config):

    enable: bool = False
    score_threshold: int = 50
    target_members: List[str] = []
    target_groups: List[str] = []

    def __init__(self, **values: Any):
        super().__init__(**values)
        try:
            self.enable = self._set(values.get("illrssyanderepoprecentenable"), False)
            self.use_proxy = self._set(values.get("illrssyanderepoprecentuseproxy"), False)
            self.score_threshold = self._set(values.get("illrssyanderepoprecentscorethreshold"), 50)
            self.target_members = self._set(values.get("illrssyanderepoprecenttargetmembers"), [])
            self.target_groups = self._set(values.get("illrssyanderepoprecenttargetgroups"), [])
        except ValueError as e:
            raise self.ConfigError(e)
        try:
            assert type(self.enable) == bool
            assert type(self.score_threshold) == int
            assert type(self.target_members) == list
            assert type(self.target_members) == list
        except AssertionError as e:
            raise self.ConfigError(e)


global_config = nonebot.get_driver().config
yande_re_popular_recent_config = YandeRePopularRecentConfig(**global_config.dict())


class YandeRePopularRecentIllustration(BaseIllustration):

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
        self.link = re.search(r'https://files.yande.re/sample/[^"]*', entry['description']).group()
        # filename
        self.filename = f"yande_re_popular_recent_{self.id}.jpg"
        # filepath
        if yande_re_popular_recent_config.use_mirai:
            self.filepath = os.path.join(yande_re_popular_recent_config.mirai_images_path, self.filename)
        else:
            self.filepath = os.path.join(yande_re_popular_recent_config.cachepath, self.filename)


class YandeRePopularRecentRss(BaseRss):

    def __init__(self):
        self.rss_url = "https://rsshub.app/yande.re/post/popular_recent"

    def parse(self) -> List[YandeRePopularRecentIllustration]:
        illustrations = []
        for entry in self.rss_json["entries"]:
            try:
                illustration = YandeRePopularRecentIllustration(entry)
                if illustration.score < yande_re_popular_recent_config.score_threshold:
                    continue
                illustrations.append(illustration)
            except:
                continue
        return illustrations


class YandeRePopularRecentDownloader(BaseDownloader):

    rss: YandeRePopularRecentRss
    illustrations: List[YandeRePopularRecentIllustration]
    use_salt: bool = True

    def __init__(self):
        self.rss = YandeRePopularRecentRss()


class YandeRePopularRecentSender(BaseSender):
    pass


if yande_re_popular_recent_config.enable:

    @scheduler.scheduled_job("cron", hour="*", minute="*/7", id="yande_re_popular_recent_downloader")
    async def yande_re_popular_recent_downloader():
        await YandeRePopularRecentDownloader().run(yande_re_popular_recent_config)

    @scheduler.scheduled_job("cron", hour="*", minute="*/11", id="yande_re_popular_recent_sender")
    async def yande_re_popular_recent_sender():
        await YandeRePopularRecentSender(yande_re_popular_recent_config, "yande_re_popular_recent").run()
