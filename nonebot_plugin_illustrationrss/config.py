import os.path
from typing import Any, List

from pydantic import BaseSettings


class Config(BaseSettings):

    plugin_setting: str = "default"
    superusers: List[str] = []
    use_proxy: bool = False
    proxies: dict = {}
    cache_dir: str = "IllRssCacheDir"

    class Config:
        extra = "ignore"

    class ConfigError(Exception):
        pass

    def __init__(self, **values: Any):
        super().__init__(**values)
        self.use_proxy = self._set(values.get("illrssuseproxy"), False)
        self.proxies = self._set(values.get("illrssproxies"), {})
        self.cache_dir = self._set(values.get("illrsscachedir"), "")
        try:
            assert type(self.use_proxy) == bool
            assert type(self.proxies) == dict
            assert type(self.cachepath) == str
        except AssertionError as e:
            raise self.ConfigError(e)
        if not os.path.exists(self.cache_dir):
            os.makedirs(self.cache_dir)

    @staticmethod
    def _set(value: Any, default: Any):
        if not value:
            return default
        return value
