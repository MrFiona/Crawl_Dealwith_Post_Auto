import scrapy, pymysql
from .. import items
import json, time, random
from fake_useragent import UserAgent
from ..tools import basic

class toutiaoSpider(scrapy.Spider):
    name = "toutiaoSpider"
    # allowed_domains = ["www.toutiao.com"]
    # ----------------------- 手动获取cookies和signature的方式 -----------------------------------
    # signature = "_02B4Z6wo00901kln9egAAIDB-ZYZIH4SMh5JQ.FAAPNOzVMC8w1TlrAjpWWO0pFQUTkZlrWpkmY8O9.sUKGHxnwVS4rucVAbrsG4q.W6.xwLoT-orRjn8VgBPauK.veP8ROb9ku4YzDnQyzj40"
    # cleaner = basic.cleanCookiesAndHeadersByRow()
    # cookies = cleaner.translateCookies("__ac_signature=_02B4Z6wo00f01BzAvYgAAIDDrDFRQQIuS.gc4LkAAGZcec; ttcid=10b747fe75ea420b8d8957ad04a1b3a921; tt_webid=7018349806059144712; s_v_web_id=verify_kuot5n54_TX4SeoI4_w4hJ_4jFk_90uZ_T3gvqNcLoldZ; csrftoken=bd335ff96f2f9e157094d8ccffb54854; MONITOR_WEB_ID=7018349806059144712; ttwid=1%7CJq2h1aBSC4kUT-kf9dcqoZMMmJ75jz0YRPG97wqPXO0%7C1634089144%7C41bbbb597d14c9388713d1c2f340abd7a140d9965559dce72f0cae622bfd74a9; tt_scid=ZVgesob4VcpKYXsK2Q8Nb3lpLwyn13Nf19jXdjF739dBWtMBWJiKhHQOJZ5m3pmc9773")
    # ------------------------- 自动获取cookies和signature的方式
    toutiao = basic.articleUrl_toutiao()
    toutiaocookiesAndSignature = toutiao.get_cookiesAndSignature()
    cookies = toutiaocookiesAndSignature["cookies"]
    signature = toutiaocookiesAndSignature["signature"]
    if("refresh_count" not in toutiaocookiesAndSignature.keys()):
        refresh_count = '1'
    else:
        refresh_count = toutiaocookiesAndSignature["refresh_count"]

    start_urls = "https://www.toutiao.com/api/pc/list/feed?channel_id=3189399007&min_behot_time=0&refresh_count=" + refresh_count + "&category=pc_profile_channel&_signature=" + signature
    headers = {
        'Host': 'www.toutiao.com',
        'Connection': 'keep-alive',
        'sec-ch-ua': '" Not;A Brand";v="99", "Google Chrome";v="91", "Chromium";v="91"',
        'Accept': 'application/json, text/plain, */*',
        'sec-ch-ua-mobile': '?0',
        'User-Agent': str(UserAgent().random),
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Dest': 'empty',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Referer': 'https://www.toutiao.com/'
        }
    conn = pymysql.connect(
        host='localhost',
        user="root",
        passwd="root",
        db="imgsdatabase",
        autocommit=True
    )
    cursor = conn.cursor()

    def start_requests(self):
        # sleeptime = random.randint(0, 5)
        # # 每次请求前都要通过模拟浏览器获取cookie和signature 随机时间
        # time.sleep(sleeptime)
        # toutiao = basic.articleUrl_toutiao()
        # toutiaocookiesAndSignature = toutiao.get_cookiesAndSignature()
        # toutiaoCookies = toutiaocookiesAndSignature["cookies"]
        # self.signature = toutiaocookiesAndSignature["signature"]

        # toutiaoCookies['User-Agent'] = str(UserAgent().random)
        # yield scrapy.Request(self.start_urls, callback=self.parse_articleInfo, cookies=toutiaoCookies, headers=self.headers, dont_filter=False)
        print("url : ", self.start_urls)
        yield scrapy.Request(self.start_urls, callback=self.parse_articleInfo, cookies=self.cookies, headers=self.headers, dont_filter=False)

    # 随机时间
    def randomSleep(self):
        sleepTime = random.randint(0,15)
        time.sleep(sleepTime)
        pass

    def getNewHeader(self):
        headers = {
            'Connection': 'keep-alive',
            'Accept': 'application/json, text/plain, */*',
            'sec-ch-ua-mobile': '?0',
            'User-Agent': str(UserAgent().random),
            'Sec-Fetch-Site': 'same-origin',
            'Sec-Fetch-Mode': 'cors',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Referer': 'https://www.toutiao.com/'
        }
        return headers

    # 文章信息
    def parse_articleInfo(self, response, **kwargs):
        if(response.status != 200):
            print(" ---------------------\n", response.status, " ---------------------\n")

        data = json.loads(response.text)["data"]    # 文章信息json列表
        max_behot_time = data[-1]["behot_time"]
        # 获取文章链接 打开文章并下载图片
        urlsList = []   # 文章链接
        toutiaoArticleItem = items.toutiaoArticleInfoItem()
        for articleInfo in data:
            toutiaoArticleItem['title'] = articleInfo['title']
            if('article_url' in articleInfo.keys() and 'share_url' in articleInfo.keys()):
                url = articleInfo['article_url']
            elif('share_url' in articleInfo.keys()):
                url = articleInfo['share_url']
            elif('article_url' in articleInfo.keys()):
                url = articleInfo['article_url']
            else:
                url=''
            if (url and url not in urlsList):
                urlsList.append(url)

            # if ('article_url' in articleInfo.keys() and 'share_url' in articleInfo.keys()):
            #     toutiaoArticleItem['article_url'] = articleInfo['article_url']
            #     toutiaoArticleItem['share_url'] = articleInfo['share_url']
            # elif ('share_url' in articleInfo.keys()):
            #     toutiaoArticleItem['article_url'] = "无链接"
            #     toutiaoArticleItem['share_url'] = articleInfo['share_url']
            # elif ('article_url' in articleInfo.keys()):
            #     toutiaoArticleItem['article_url'] = articleInfo['article_url']
            #     toutiaoArticleItem['share_url'] = "无链接"
            # else:
            #     toutiaoArticleItem['article_url'] = "无链接"
            #     toutiaoArticleItem['share_url'] = "无链接"
            # toutiaoArticleItem['behot_time'] = articleInfo['behot_time']
            # if('group_id' in articleInfo.keys()):
            #     toutiaoArticleItem['group_id'] = articleInfo['group_id']
            # else:
            #     toutiaoArticleItem['group_id'] = "无 group_id"
            # if('has_image' in articleInfo.keys()):
            #     toutiaoArticleItem['has_image'] = articleInfo['has_image']
            # else:
            #     toutiaoArticleItem['has_image'] = "无 has_image"
            # if('user_info' in articleInfo.keys()):
            #     toutiaoArticleItem['user_name'] = articleInfo['user_info']['name']
            #     toutiaoArticleItem['user_id'] = articleInfo['user_info']['user_id']
            #     toutiaoArticleItem['user_avatarUrl'] = articleInfo['user_info']['avatar_url']
            # elif('user' in  articleInfo.keys()):
            #     toutiaoArticleItem['user_name'] = articleInfo['user']['name']
            #     toutiaoArticleItem['user_id'] = articleInfo['user']['user_id']
            #     toutiaoArticleItem['user_avatarUrl'] = articleInfo['user']['avatar_url']
            # yield toutiaoArticleItem

        for urlItem in urlsList:
            if(urlItem==''):
                continue
            # 每次请求前都要通过模拟浏览器获取cookie和signature 随机时间
            # cas = self.toutiao.get_cookiesAndSignature()
            # self.cookies = cas['cookies']
            # self.headers = self.getNewHeader()
            self.randomSleep()
            yield scrapy.Request(
               url=urlItem, callback=self.parse_articleContent, cookies=self.cookies, headers=self.headers
            )

        # sleeptime = random.randint(0, 20)
        # # 每次请求前都要通过模拟浏览器获取cookie和signature 随机时间
        # time.sleep(sleeptime)
        # toutiao = basic.articleUrl_toutiao()
        # toutiaocookiesAndSignature = toutiao.get_cookiesAndSignature()
        # self.cookies = toutiaocookiesAndSignature["cookies"]
        # self.signature = toutiaocookiesAndSignature["signature"]
        # nextUrl = "https://www.toutiao.com/api/pc/list/feed?channel_id=3189399007&max_behot_time=" + str(max_behot_time) + "&category=pc_profile_channel&_signature=" + self.signature
        # self.headers = self.getNewHeader()
        # # 递归获取文章列表数据
        # nextUrlList = [].append(nextUrl)
        # yield scrapy.FormRequest(
        #     nextUrl, callback=self.parse, cookies=self.cookies, headers=self.headers, dont_filter=False
        # )

    def parse_articleContent(self, response, **kwargs):
        # 获取图片链接并保存
        imgUrlList = response.xpath("//article//img/@src").extract()
        if(imgUrlList):
            print("处理的urlList如下：")
            print(imgUrlList)
            toutiaoImg = items.toutiaoImgItem()
            for url in imgUrlList:
                sql = "INSERT INTO `imgsdatabase`.`tb_contentimg_toutiao` (`origin_pic_path`) VALUES (\'{}\');".format(url)
                result = self.cursor.execute(sql)
                if (result == 1):
                    print("插入图片url成功:  ", url)
                else:
                    print("插入记录失败： ", sql)
                toutiaoImg["imgUrl"] = url
                yield toutiaoImg
