from typing import Any, List

import nonebot
from pydantic import BaseSettings


class Config(BaseSettings):

    # plugin custom config
    plugin_setting: str = "default"
    use_proxy: bool = False
    proxies: dict = None
    cachepath: str = None
    bot_id: str = None
    use_mirai: bool = True
    mirai_images_path: str = None

    # yande.re popular_recent
    yande_re_popular_recent_enable: bool = False
    yande_re_popular_recent_score_threshold: int = 50
    yande_re_popular_recent_tgt_members: List[str] = []
    yande_re_popular_recent_tgt_groups: List[str] = []

    class Config:
        extra = "ignore"

    class ConfigError(Exception):
        pass

    def __init__(self, **values: Any):
        super().__init__(**values)
        try:
            self.use_proxy = bool(values.get("illrssuseproxy"))
            self.proxies = {
                "http": values.get("illrssproxies"),
                "https": values.get("illrssproxies")
            }
            self.cachepath = values.get("illrsscachedir")
            self.bot_id = str(values.get("illrssbotid"))
            self.use_mirai = values.get("illrssusemirai")
            self.mirai_images_path = values.get("illrssmiraiimagespath")
            # yande.re popular_recent
            self.yande_re_popular_recent_enable = bool(values.get("illrssyanderepoprecentenable"))
            self.yande_re_popular_recent_score_threshold = int(values.get("illrssyanderepoprecentscorethreshold"))
            self.yande_re_popular_recent_tgt_members = values.get("illrssyanderepoprecenttargetmembers")
            self.yande_re_popular_recent_tgt_groups = values.get("illrssyanderepoprecenttargetgroups")
        except ValueError as e:
            raise self.ConfigError(e)

    @staticmethod
    def _set(value: Any, default: Any):
        if not value:
            return default
        return value


global_config = nonebot.get_driver().config
plugin_config = Config(**global_config.dict())
