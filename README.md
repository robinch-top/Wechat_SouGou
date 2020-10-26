---
title: 搜狗微信文章的抓取
date: 2020-10-26 10:05:18
permalink: /pages/f239fd/
categories:
  - Python
tags:
  - Python
  - 爬虫
  - 公众号文章
---
需要对某个关键字的微信公众号文章进行抓取，按时间排序。

首先就想到了用搜狗微信的Api，但是查询资料后发现，在19年的时候，就已经禁止了。

目前搜狗做的处理是：封ip，封cookie。

又从网上找了一下具体实现的过程。

想要完成的功能：

[√]时间

[√]标题

[×]文章链接（目前只实现了临时链接。）

具体的代码放到了[github](https://github.com/robinch-top/Wechat_SouGou)

如果不需要访问搜狗微信的后十页Cookie中只需要包含SNUID 、SUID即可

如果需要访问，则需加上ppinf和ppmdig，这两个是需要登录后获取的。

临时链接转永久链接目前找到的有两种办法

一是使用微信公众号文章素材的api（过多容易被封）

二是使用模拟器，具体的也没有了解。

主要是我对永久链接的需求不大，所以没有继续弄下去。有需求的小伙伴可以继续研究一下。

当然也可以付费找一些中间商帮你完成。

目前可加深完善的功能：

1.使用代理池，获取ip来抓取，记得刷新cookie。

2.获取永久链接。

本文参考借鉴（复制😁）了以下链接的文章：

https://blog.csdn.net/qq_35193302/article/details/84559660

https://www.cnblogs.com/triangle959/p/10662892.html

https://segmentfault.com/a/1190000023622107

https://www.pythonf.cn/read/129313
