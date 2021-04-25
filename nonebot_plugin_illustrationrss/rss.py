import asyncio
from typing import Dict, List

import feedparser
import httpx

from .config import Config
from .illustration import BaseIllustration


class BaseRss(object):
    rss_url: str
    rss_json: Dict

    class RssDownloadError(Exception):
        pass

    async def download(self, config: Config):
        fail_flag = True
        for _ in range(3):
            try:
                if config.use_proxy:
                    async with httpx.AsyncClient(verify=False, proxies=config.proxies) as client:
                        r = await client.get(self.rss_url)
                else:
                    async with httpx.AsyncClient(verify=False) as client:
                        r = await client.get(self.rss_url)
                self.rss_json = feedparser.parse(r.text)
            except:
                await asyncio.sleep(2)
            else:
                fail_flag = False
                break
        if fail_flag:
            raise self.RssDownloadError()

    def parse(self) -> List[BaseIllustration]:
        raise NotImplementedError()
