from typing import Any

import nonebot
from pydantic import BaseSettings


class Config(BaseSettings):

    # plugin custom config
    plugin_setting: str = "default"
    use_proxy: bool = False
    proxies: dict = None
    cachepath: str = None
    # yande.re popular_recent
    yande_re_popular_recent_enable: bool = False
    yande_re_popular_recent_score_threshold: int = 50

    class Config:
        extra = "ignore"

    class ConfigError(Exception):
        pass

    def __init__(self, **values: Any):
        super().__init__(**values)
        try:
            self.use_proxy = bool(values.get("illustrationrssuseproxy"))
            self.proxies = {
                "http": values.get("illustrationrssproxies"),
                "https": values.get("illustrationrssproxies")
            }
            self.cachepath = values.get("illustrationrsscachedir")
            # yande.re popular_recent
            self.yande_re_popular_recent_enable = bool(values.get("illustrationrssyanderepopularrecentenable"))
            self.yande_re_popular_recent_score_threshold = int(values.get("illustrationrssyanderepopularrecentscorethreshold"))
        except ValueError as e:
            raise self.ConfigError(e)


global_config = nonebot.get_driver().config
plugin_config = Config(**global_config.dict())
