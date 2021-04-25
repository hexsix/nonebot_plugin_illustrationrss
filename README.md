<p align="center">
  <a href="https://v2.nonebot.dev/"><img src="https://raw.githubusercontent.com/nonebot/nonebot2/master/docs/.vuepress/public/logo.png" width="200" height="200" alt="nonebot"></a>
</p>

<div align="center">

# NoneBot Plugin IllustrationRSS（Under Construction）

✨ NoneBot 插画订阅插件（开发中） ✨

</div>

## 一、支持的图源（正在进行）

- [x] yande.re popular_recent ([https://rsshub.app/yande.re/post/popular_recent](https://rsshub.app/yande.re/post/popular_recent))
- [ ] pixiv.net daily ranking ([https://rsshub.app/pixiv/ranking/day](https://rsshub.app/pixiv/ranking/day))

## 二、食用方法

### 2.1 安装本插件和相关依赖

- nonebot_plugin_apscheduler
- nonebot_plugin_illustrationrss（还未发布，如需体验请手动）

```requirements
opencv_python>=4.2.0.32
numpy>=1.16.1
feedparser>=5.2.1
httpx>=0.11.1
```

ps. 注意 sheduler 插件的加载时间要在本插件之前

```python
nonebot.load_plugin("nonebot_plugin_apscheduler")
nonebot.load_plugins("nonebot_plugin_illustrationrss")  # plugin
nonebot.load_plugins("src/plugins")                     # 手动
```

### 2.2 配置 .env

#### 2.2.1 基础配置

```env
IllRssBotID=114514
IllRssUseProxy=false
IllRssProxies={"http": "http://127.0.0.1:8889", "https": "http://127.0.0.1:8889"}
IllRssCacheDir=/path/to/your/cache/dir
IllRssUseMirai=false
IllRssMiraiImagesPath=/path/to/mcl/data/net.mamoe.mirai-api-http/images
```

apscheduler 的计划配置请参阅：[https://apscheduler.readthedocs.io/en/latest/userguide.html](https://apscheduler.readthedocs.io/en/latest/userguide.html)

httpx 的代理配置请参阅：[https://www.python-httpx.org/advanced/#example](https://www.python-httpx.org/advanced/#example)

#### 2.2.2 yande.re popular

```env
IllRssYandeRePopRecentEnable=true
IllRssYandeRePopRecentUseProxy=true
IllRssYandeRePopRecentScoreThreshold=50
IllRssYandeRePopRecentTargetGroups=["987654321"]
IllRssYandeRePopRecentTargetMembers=["123456789"]
```

## 三、计划中的事

- [x] 每个图源都有自己的代理规则
- [ ] 支持代理自定义 header （for pixiv）
- [ ] 支持每个目标群或者好友单独设置计划任务
- [ ] 支持在群内或者私聊动态地管理本插件
- [ ] 修正 httpx 的 debug 输出 “returning true from eof_received() has no effect when using ssl”

## 四、欢迎 PRPRPRPR

### 扩展基类就好了

你需要扩展 Config、BaseDownloader、BaseIllustration、BaseRss、BaseSender

具体参考 yande_re_popular_recent.py

## 五、Q&A

### Illustration RSS 如何工作

对于每个模块都有两个计划任务单独工作

Downloader 监视上游 RSS，定时下载图片

Sender 监视图片目录，定时发送没有推送的图片

### Illustration RSS 额外存储了哪些东西

对于每个模块，CacheDir 目录下都会存储一个 *already_sent.pkl 文件，这个文件持久化了一个三元组 Set，记录了是否向某人、群发送了某张图片

对于 mirai 用户，由于 mirai-api-http send_xx_message 的实现问题，只能发送 “/path/to/mcl/data/net.mamoe.mirai-api-http/images” 下的图片，所以图片会下载到这个目录

对于 cqhttp 用户，图片会自动下载到设置好的 CacheDir

### Illustration RSS 会支持多机器人吗

应该不会（懒）

### 如何写配置

Check https://pydantic-docs.helpmanual.io/usage/types/
