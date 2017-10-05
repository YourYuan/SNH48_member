# 【面对塞纳河编程】SNH48 Group第一届人口普查

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

&emsp;&emsp;幸好，通过对浏览器抓包发现，所有成员的资料都储存在一个json文件中，每次通过成员ID回调获得资料。这就意味着我们只需要爬取一次就可以获得所有成员的资料。从这个方面来说我还是很喜欢丝芭的官网的。

![](file:///Users/thesuguser/Desktop/Personal_project/SNH48_member/report_figure/json.jpg)

![](file:///Users/thesuguser/Desktop/Personal_project/SNH48_member/report_figure/json2.jpg)



&emsp;&emsp;代码实现如下

    import requests
    import urllib
    
    def member_crawler(team_code):
    	headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
      	'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
      	'Accept-Encoding': 'gzip, deflate',
      	'Content-Type': 'application/x-www-form-urlencoded; charset= utf-8',
      	'Connection':"keep-alive",
      	'Referer': 'http://www.snh48.com/member_details.html?sid=10001'
      	}
    
      	url = 'http://h5.snh48.com/resource/jsonp/members.php?gid=' + team_code +'&callback=get_members_success'
    
      	req = urllib.request.Request(url,headers=headers)
    
      	res = urllib.request.urlopen(req)
    
      	content = res.read().decode('utf-8')
    
      	return content
&emsp;&emsp;爬虫返回内容的整理我在这里直接用的正则表达式匹配。对于json文件，其实有更加快速方便的方法，我用了这种傻瓜的方式，也只是因为我觉得正则用的比较顺手（捂脸）。

&emsp;&emsp;有兴趣的朋友也可以没事去爬爬丝芭的网站，比如爬一下最新生写头像什么的。

## 数据分析

&emsp;&emsp;数据爬取于2017年10月1日。截止当日，官网名单（包括暂休）共有**312**名成员，其中SNH48拥有成员**116**名，GNZ48拥有成员**77**名，BEJ48拥有成员**72**名，SHY48拥有成员**47**名。在进行数据分析的过程中NII又有新成员马凡加入。因为个人倦怠，就没有加上马凡的资料，所有数据还是基于**312**名成员的资料进行展示。

### 身高###

&emsp;&emsp;首先，我们从**身高**这个刺激的话题开始。在爬的过程中，我就猜想过那个分团的平均身高会是最高的，初步猜想可能SHY48会有一些优势，毕竟是在模特学校招过成员的分团，但是数据的结果却和我猜想的有一些不同。

&emsp;&emsp;SNH48 group 312名成员的平均身高是**164.1**cm。

​	SNH48成员的平均身高为**165.0**cm。

​	GNZ48成员的平均身高为**163.5**cm。	

​	BEJ48成员的平均身高为**163.1**cm。

​	SHY48成员的平均身高为**164.7**cm。

​	万万没想到，本部居然是平均身高最高的。BEJ48全group平均最矮。emmmm，对于这个，我就不发表什么评论了。

​	通过计算方差，成员之间身高**差距最小**的是**SNH48**，身高**差距最大**的是**SHY48**。

​	接着我们来看看王国里的最高之人和最矮之人。来自SNH48 Team HII的**姜涵**以**176**cm的身高夺得**最高**之人的桂冠，全Group**最矮**的称号则被来自GNZ48 Team NIII的闹闹**卢静**和来自BEJ48 Team E的**李烨**以**155cm**的身高共同获得。

​	对于这两项数据，大家也知道水分有多大，络络的官网身高还是刚入团时的**172**cm，这显然是不科学的。以及某位**DDD**同学（我就不指名道姓说了）在官网的身高是**159**cm，你的良心不会痛吗？

### 血型###

​	中国是以**OB**血型为主体的国家。我军全group血型分布如下

![](file:///Users/thesuguser/Desktop/Personal_project/SNH48_member/report_figure/blood_type.png)

​	对于血型，没有什么太多能发表的看法。有这么多成员不知道自己的血型也是比较有趣的一件事。以及我们总是说塞纳河是一个小社会，从血型分布上来说，也确实是这样的，完美符合中国社会的血型分布。所以说，林子大了，什么小可爱都有，这么想来，河内发生什么事都不足为奇了，这就是一个社会的缩影嘛~

### 星座&出生时间###

​	星座和出生时间就放在一起讨论了。

​	全Group星座御三家如下：

&emsp;&emsp;1. **处女座** 33人

&emsp;&emsp;2. **双子座** 32人

&emsp;&emsp;3. **射手座** 28人

&emsp;&emsp;3. **天秤座** 28人

​	其中处女座以微弱优势获得领先，而摩羯座是成员数量最少的星座。你的推的星座是否榜上有名呢。因为我对星座实在是没有什么认识，所以发表不了太多看法。剩下星座的人数都在下面的柱状图里了。

![](file:///Users/thesuguser/Desktop/Personal_project/SNH48_member/report_figure/star.png)

​	另一件有意思的事是，一年中哪一天有最多数量的成员过生日呢？

​	答案是**3月23日**。

​	徐真，梁可，邓恩惠，苏杉杉，乔钰珂，杨晔六名成员在3月23日过生日。其中3位来自BEJ48。话说我女朋友的生日也是这一天，可能这一天出生的女孩子会可爱一点吧！



### 特长&爱好

​	成员的特长和爱好多种多样，做数量统计未免不够直观。所以我在这里把特长和爱好收集在了一起，做完分词之后将它们做成了词云。词云中字体越大则说明拥有这个特长或爱好的成员越多。

​	首先我们来看成员特长的词云：

![](file:///Users/thesuguser/Desktop/Personal_project/SNH48_member/report_figure/skill.png)

​	不出所料的是，**跳舞**和**唱歌**占据了最大的两个字体，钢琴，画画，表演紧随其后。妹子选择入团，必然是对歌舞表演充满兴趣的。不过特长其中也混进了一些奇怪的，emmm，东西。比如：**反射弧特长，腿特长，一秒变马云，把天聊死…**我只能说，姑娘们，我敬你们是条好汉。

​	接着我们来看看关于爱好的词云：

![](file:///Users/thesuguser/Desktop/Personal_project/SNH48_member/report_figure/hobby.png)

​	不出所料的跳舞唱歌，接着比较多人喜欢的是**看电影，旅游，动漫，宅舞**。比较惊奇的是，有**24**名在个人爱好这里选择了**宅舞**，比我想象中多不少，希望接下来能看到更多成员的宅舞表演吧。

​	当然爱好中也有一些奇奇怪怪的存在，比如**躺着吃外卖打王者荣耀，思考人生，看and模仿鬼畜视频**这些的。



### 家乡###

​	好像之前已经有聚聚统计过了成员的籍贯信息。不过最近又加入了一批新成员，信息也需要更新。

​	诞生成员最多的省份的御三家分别是：**四川**（35人），**广东**（28人），**辽宁**（27人）。**上海**以25人位居第四。

​	不得不说，川渝地区真是扛起了SNH48 Group的半边天。将成员家乡省份的分布做成热点图如下

![](file:///Users/thesuguser/Desktop/Personal_project/SNH48_member/report_figure/home.png)

看看这个分布，什么叫做天下布妹，这就是天下布妹。除了没有来自**西藏**，**宁夏**，**澳门**这三个自治区、特别行政区的成员，别的省市自治区都有妹子加入了SNH48 Group。接下来很期待这是那个地区的女生入团了，等着这张图被蓝色填满的那一天。



## 写在最后

​	从起念做这个project到最后完成花了正好整整24个小时。其实也只是做了一些很粗浅的东西。如果大家还有什么想要从这些数据里挖掘的也可以在评论里留言。我也还有很多想法没有实践，如果接下来有时间还会继续完善。

​	成员的资料我已经整理成了Excel文件和Python的代码一起放在Github上。[Github请戳这里](https://github.com/TheSuguser/SNH48_member) 如果觉得喜欢或者有帮到你，也可以给一个Star哦。如果对于爬虫，数据分析，机器学习想要一起交流的聚聚请大力私联我！

​	最后夹带一个私货，欢迎大家关注SNH48-谢天依，以及谢天依应援会（414680601）

​		