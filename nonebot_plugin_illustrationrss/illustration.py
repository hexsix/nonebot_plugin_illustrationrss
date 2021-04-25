import asyncio
import random

import cv2
import httpx
import numpy as np

from .config import Config


class BaseIllustration(object):
    link: str = None
    filepath: str = None

    def __str__(self):
        return f"Ill(\"{self.link}\",\"{self.filepath}\")"

    __repr__ = __str__

    class IllustrationDownloadError(Exception):
        pass

    async def download(self, config: Config, use_salt: bool = False):
        fail_flag = True
        for _ in range(3):
            try:
                if config.use_proxy:
                    async with httpx.AsyncClient(verify=False, proxies=config.proxies) as client:
                        r = await client.get(self.link)
                else:
                    async with httpx.AsyncClient(verify=False) as client:
                        r = await client.get(self.link)
            except:
                await asyncio.sleep(2)
            else:
                fail_flag = False
        if fail_flag:
            raise self.IllustrationDownloadError()
        else:
            with open(self.filepath, 'wb') as f:
                f.write(r.content)

        if use_salt:
            self.salt()

    @staticmethod
    def _salt(img: np.ndarray, n: int = 6) -> np.ndarray:
        """
        :param img: img mat
        :param n: number of salt
        :return: salty img mat
        """
        assert type(img) == np.ndarray
        for _ in range(n):
            i = random.randint(0, img.shape[1] - 1)
            j = random.randint(0, img.shape[0] - 1)
            if img.ndim == 2:
                img[j, i] = 255
            elif img.ndim == 3:
                img[j, i, 0] = random.randint(0, 255)
                img[j, i, 1] = random.randint(0, 255)
                img[j, i, 2] = random.randint(0, 255)
        return img

    def salt(self):
        image = cv2.imread(self.filepath)
        salt_image = self._salt(image)
        cv2.imwrite(self.filepath, salt_image)


class LocalIllustration(BaseIllustration):
    def __init__(self, filepath):
        self.filepath = filepath
        self.link = ""
