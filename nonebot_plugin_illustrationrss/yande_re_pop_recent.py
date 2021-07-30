import os
import pickle
import re
from typing import List, Dict, Any, Set

import nonebot

from .config import Config
from .downloader import BaseDownloader
from .illustration import BaseIllustration
from .rss import BaseRss
from .sender import BaseSender


class YandeRePopularRecentConfig(Config):

    enable: bool = False
    score_threshold: int = 50
    use_proxy: bool = False
    cache_dir: str = os.path.join("IllRssCacheDir", "YandeRePopRecent")
    prefix: str = "yande"

    def __init__(self, **values: Any):
        super().__init__(**values)
        try:
            self.enable = self._set(values.get("illrssyanderepoprecentenable"), False)
            self.use_proxy = self._set(values.get("illrssyanderepoprecentuseproxy"), False)
            self.score_threshold = self._set(values.get("illrssyanderepoprecentscorethreshold"), 50)
        except ValueError as e:
            raise self.ConfigError(e)
        try:
            assert type(self.enable) == bool
            assert type(self.score_threshold) == int
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
        # filename: yande_892137_43_s.jpg
        self.filename = f"{yande_re_popular_recent_config.prefix}_{self.id}_{self.rating}.jpg"
        # filepath
        self.filepath = os.path.join(yande_re_popular_recent_config.cache_dir, self.filename)


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

    @staticmethod
    def not_send_list(uid: int):
        try:
            already_sent = pickle.load(open(os.path.join(yande_re_popular_recent_config.cache_dir, f"{uid}.pkl")))
        except FileNotFoundError:
            already_sent = set()
        ill_filepaths = []
        for ill_filename in os.listdir(yande_re_popular_recent_config.cache_dir):
            if not ill_filename.endswith("jpg"):
                continue
            elif ill_filename in already_sent:
                continue
            else:
                ill_filepaths.append(os.path.join(yande_re_popular_recent_config.cache_dir, ill_filename))
        return ill_filepaths

    @staticmethod
    def save_sent(uid: int, cur: Set[str]):
        try:
            already_sent = pickle.load(open(os.path.join(yande_re_popular_recent_config.cache_dir, f"{uid}.pkl")))
        except FileNotFoundError:
            already_sent = set()
        already_sent.update(cur)
        pickle.dump(already_sent, open(os.path.join(yande_re_popular_recent_config.cache_dir, f"{uid}.pkl")))
