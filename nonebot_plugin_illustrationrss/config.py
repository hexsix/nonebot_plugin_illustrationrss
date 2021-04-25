import os.path
from typing import Any, List

from pydantic import BaseSettings


class Config(BaseSettings):

    plugin_setting: str = "default"
    bot_id: str = ""
    # admins: List[str] = []
    use_proxy: bool = False
    proxies: dict = {}
    cachepath: str = None
    use_mirai: bool = True
    mirai_images_path: str = None
    target_members: List[str] = []
    target_groups: List[str] = []

    class Config:
        extra = "ignore"

    class ConfigError(Exception):
        pass

    def __init__(self, **values: Any):
        super().__init__(**values)
        self.bot_id = self._set(str(values.get("illrssbotid")), "")
        self.use_proxy = self._set(values.get("illrssuseproxy"), False)
        self.proxies = self._set(values.get("illrssproxies"), {})
        self.cachepath = self._set(values.get("illrsscachedir"), "")
        self.use_mirai = self._set(values.get("illrssusemirai"), False)
        self.mirai_images_path = self._set(values.get("illrssmiraiimagespath"), "")
        try:
            assert type(self.bot_id) == str
            assert type(self.use_proxy) == bool
            assert type(self.proxies) == dict
            assert type(self.cachepath) == str
            assert type(self.use_mirai) == bool
            assert type(self.mirai_images_path) == str
        except AssertionError as e:
            raise self.ConfigError(e)
        if not self.bot_id:
            raise self.ConfigError("Bot ID 未设置")
        if self.use_mirai and not self.mirai_images_path:
            raise self.ConfigError("mirai_images 目录未设置, 通常在 /path/to/mcl/data/net.mamoe.mirai-api-http/images")
        if not os.path.exists(self.cachepath):
            raise self.ConfigError("Cache 目录配置有误")
        if not os.path.exists(self.mirai_images_path):
            raise self.ConfigError("mirai_images 目录配置有误")

    @staticmethod
    def _set(value: Any, default: Any):
        if not value:
            return default
        return value
