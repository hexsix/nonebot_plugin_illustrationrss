<p align="center">
  <a href="https://v2.nonebot.dev/"><img src="https://raw.githubusercontent.com/nonebot/nonebot2/master/docs/.vuepress/public/logo.png" width="200" height="200" alt="nonebot"></a>
</p>

<div align="center">

# NoneBot Plugin IllustrationRSS（Under Construction）

✨ NoneBot 插画订阅插件（开发中） ✨

</div>

## 支持的图源（正在进行）

- [ ] yande.re popular_recent ([https://rsshub.app/yande.re/post/popular_recent](https://rsshub.app/yande.re/post/popular_recent))
- [ ] pixiv.net daily ranking ([https://rsshub.app/pixiv/ranking/day](https://rsshub.app/pixiv/ranking/day))

## 食用方法

### 安装本插件和相关依赖

- nonebot_plugin_apscheduler
- nonebot_plugin_illustrationrss（还未发布，如需体验请手动）

```requirements
opencv_python>=4.2.0.32
numpy>=1.16.1
feedparser>=5.2.1
httpx>=0.11.1
```

ps. 注意 sheduler 插件的加载时间要在本插件之前

### .env 配置

#### 基础配置

TODO

```env
IllustrationRssUseProxy=true
IllustrationRssProxies=http://127.0.0.1:8889
IllustrationRssCacheDir=~/.Temp/illustrationrss
```

apscheduler 的计划配置请参阅：[https://apscheduler.readthedocs.io/en/latest/userguide.html](https://apscheduler.readthedocs.io/en/latest/userguide.html)

httpx 的代理配置请参阅：[https://www.python-httpx.org/advanced/#example](https://www.python-httpx.org/advanced/#example)

#### yande.re popular

TODO

```env
IllustrationRssYandeRePopularRecentEnable=true
IllustrationRssYandeRePopularRecentScoreThreshold=50
IllustrationRssYandeRePopularRecentDownloaderScheduler={type: "cron", hour: "*", minute: "30"}
IllustrationRssYandeRePopularRecentSenderScheduler={type: "cron", hour: "*", minute: "30"}
IllustrationRssYandeRePopularRecentTargetGroup=[""]
IllustrationRssYandeRePopularRecentTargetMember=[""]
```

## 计划中的事

- [ ] 每个图源都有自己的代理规则
- [ ] 支持诸如 SOCKS5 等代理方法
- [ ] 可以在群内或者私聊动态地管理本插件
- [ ] 多帐号支持

## 欢迎 PRPRPRPR

### 扩展基类就好了

### 如何写配置

Check https://pydantic-docs.helpmanual.io/usage/types/
