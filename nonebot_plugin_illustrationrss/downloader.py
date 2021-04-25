import os
from typing import List

from nonebot import logger

from .config import Config
from .rss import BaseRss
from .illustration import BaseIllustration


class BaseDownloader(object):
    rss: BaseRss
    illustrations: List[BaseIllustration]
    use_salt: bool = False

    async def run(self, config: Config):
        try:
            await self.rss.download(config)
            logger.log("DEBUG", f"Succeeded to download rss \"{self.rss.rss_url}\"")
        except self.rss.RssDownloadError:
            logger.log("WARNING", f"RssDownloadError: \"{self.rss.rss_url}\"")
            return
        self.illustrations = [ill for ill in self.rss.parse() if not os.path.exists(ill.filepath)]
        logger.log("DEBUG", f"Succeeded to parse rss \"{self.illustrations}\"")
        for ill in self.illustrations:
            try:
                await ill.download(config, self.use_salt)
                logger.log("DEBUG", f"Succeeded to download illustration \"{ill.filepath}\" from \"{ill.link}\"")
            except ill.IllustrationDownloadError:
                logger.log("WARNING", f"IllustrationDownloadError \"{ill.link}\"")
                continue
