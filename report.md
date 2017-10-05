# 【面对塞纳河编程】塞纳河第一届人口普查

##Overview

&emsp;&emsp;SNH48九期生招募已经在前不久落下了帷幕，团里的成员越来越多，加上暂休的成员，总数已经在不知不觉中超过了300人。面对这么多成员，总是会不自觉地想，这真是一个做数据分析和可视化的绝佳样本。于是产生了用爬虫获取官网成员资料，进行整理和分析的念头。我叫它“塞纳河人口普查”。

&emsp;&emsp;这篇文章会先讲一些获得数据的技术手段（只有粗浅的一点点），已经对于获得成员资料的一些简单的整理分析和可视化，当然有一些分析的内容可能已经有聚聚在之前做过了。如果对技术不太感冒的聚聚可以跳过下一个part。

## 数据获取

&emsp;&emsp;成员资料全部通过Python爬虫从官网抓取。因为之前只做过一些静态网页的爬取，而SNH48 group的官网均为动态网页。我刚开始想的办法的是通过*Selenium*的*Webdrive*模块实现。对于动态网页的爬取来说这是一个比较省力且傻瓜的方式。*Webdriver*直接控制操作系统的浏览器访问网页，等待网页渲染完毕之后返回相应的内容。与其说是爬虫，不如说是一个自动化工具。

```
from selenium import webdriver

def get_data(team,id):

	member_url = 'http://www.' + team + '.com/member_details.html?sid=' + id

	driver = webdriver.Firefox()

	driver.get(member_url)

	content = driver.page_source

	return content
```

 &emsp;&emsp;相比于其他爬虫工具，*Selenium*只用几行代码就可以实现一个简单的爬取，但是相对而言耗时会久一些，从海外访问丝芭的网站响应速度又十分蛋疼，300多名成员的资料没有两三个小时是完成不了爬取的，这完全违背了爬虫高效的特征。