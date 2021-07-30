<p align="center">
  <a href="https://v2.nonebot.dev/"><img src="https://raw.githubusercontent.com/nonebot/nonebot2/master/docs/.vuepress/public/logo.png" width="200" height="200" alt="nonebot"></a>
</p>

<div align="center">

# NoneBot Plugin IllustrationRSS

✨ NoneBot 插画订阅插件 ✨

</div>

## 一、支持的图源

- [x] yande.re popular_recent ([https://rsshub.app/yande.re/post/popular_recent](https://rsshub.app/yande.re/post/popular_recent))

## 二、食用方法

### 2.1 安装本插件和相关依赖

- nonebot_plugin_apscheduler
- nonebot_plugin_rauthman
- nonebot_plugin_illustrationrss（还未发布，如需体验请手动）

```requirements
opencv_python>=4.2.0.32
numpy>=1.16.1
feedparser>=5.2.1
httpx>=0.11.1
```

ps. 注意依赖插件的加载时间要在本插件之前

```python
nonebot.load_plugin("nonebot_plugin_apscheduler")
nonebot.load_plugin("nonebot_plugin_rauthman")
nonebot.load_plugin("nonebot_plugin_illustrationrss")   # plugin
nonebot.load_plugins("src/plugins")                     # 手动
```

### 2.2 配置 .env

#### 2.2.1 nonebot_plugin_rauthman 配置

授权管理信息保存位置（必须）：

`savedata: str` 保存相对路径，示例意为保存至运行目录下的 `Yuni/savedata` 目录

```env
savedata = Yuni/savedata
```

其他 rauthman 配置请到 [nonebot_plugin_rauthman](https://github.com/Lancercmd/nonebot_plugin_rauthman) 查看

#### 2.2.2 基础配置

```env
# （可选）默认为 false
IllRssUseProxy=false
# （可选）默认为空
IllRssProxies={"http": "http://127.0.0.1:8889", "https": "http://127.0.0.1:8889"}
# （可选）默认为 项目路径下 ./IllRss
IllRssCacheDir=/path/to/your/cache/dir
```

httpx 的代理配置请参阅：[https://www.python-httpx.org/advanced/#example](https://www.python-httpx.org/advanced/#example)

#### 2.2.3 yande.re popular

```env
# （可选）默认为 true
IllRssYandeRePopRecentEnable=true
# （可选）默认为 false，如果为 true，请配置基础配置中的代理 IllRssProxies
IllRssYandeRePopRecentUseProxy=true
# （可选）默认为 50
IllRssYandeRePopRecentScoreThreshold=50
```

## 三、计划中的事

- [x] 每个图源都有自己的代理规则
- [x] 支持在群内或者私聊动态地管理本插件（由 nonebot_plugin_rauthman 管理）

## 四、欢迎 PRPRPRPR

### 扩展基类就好了

你需要扩展 Config、BaseDownloader、BaseIllustration、BaseRss、BaseSender

具体参考 yande_re_popular_recent.py

## 五、Q&A

### Illustration RSS 如何工作

对于每个模块都有两个计划任务单独工作

Downloader 监视上游 RSS，定时下载图片

发送 /yrpr 让机器人发送图片

### Illustration RSS 额外存储了哪些东西

对于每个模块，CacheDir 目录下都会存储一个 {id}_already_sent.pkl 文件，这个文件持久化了一个字符串 Set，记录了是否向某人、群发送了某张图片

另外，图片会自动下载到设置好的 CacheDir 内

### Illustration RSS 会支持多机器人吗

应该不会（懒）
