import os
from typing import List

from nonebot import logger

from .rss import RssBase
from .illustration import IllustrationBase


class DownloaderBase(object):
    rss: RssBase
    illustrations: List[IllustrationBase]
    use_salt: bool = False

    async def run(self):
        try:
            await self.rss.download()
            logger.log("DEBUG", f"Succeeded to download rss \"{self.rss.rss_url}\"")
        except self.rss.RssDownloadError:
            logger.log("WARNING", f"RssDownloadError: \"{self.rss.rss_url}\"")
            return
        self.illustrations = self.rss.parse()
        for illustration in self.illustrations:
            if os.path.exists(illustration.filepath):
                continue
            try:
                await illustration.download(self.use_salt)
                logger.log("DEBUG", f"Succeeded to download illustration \"{illustration.filepath}\" from \"{illustration.link}\"")
            except illustration.IllustrationDownloadError:
                logger.log("WARNING", f"IllustrationDownloadError \"{illustration.link}\"")
                continue
