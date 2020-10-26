import requests
from lxml import etree
import re
import urllib3
import xlwt
import json
import random
import logging
from logging.handlers import RotatingFileHandler
import time
# 重定向、封ip、封cookie


urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'Cookie': cookie,
        'Host': 'weixin.sogou.com',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-User': '?1',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36',
    }

def get_index(start_url, page):
    params = {
        'query': inputName,
        '_sug_type_': '',
        'sut': '1828',
        'lkt': '1,1597298703444,1597298703444',
        's_from': 'input',
        '_sug_': 'y',
        'type': '2',
        'sst0': '1597298703546',
        'page': page,
        'ie': 'utf8',
        'w': '01019900',
        'dr': '1',
    }
    response = requests.get(url=start_url, params=params,
                            headers=headers, verify=False)

    if response.status_code == 200:
        html = etree.HTML(response.text)
        urls = html.xpath('//ul[@class="news-list"]/li//h3/a/@href')
        for url in urls:
            url = 'https://weixin.sogou.com/' + url
            # print(url)
            yield url
    else:
        print('getting index page fail')


def get_real_url(url):
    response = requests.get(url=url, headers=headers, verify=False)
    pattern = re.compile('\+=.*?\'(.*?)\';', re.S)
    url_list = re.findall(pattern, response.text)
    real_url = ''
    for i in url_list:
        real_url += i
    real_url.replace('@', '')
    return real_url


def get_detail(url):
    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7',
        'cache-control': 'max-age=0',
        'if-modified-since': 'Fri, 14 Aug 2020 12:33:50 +0800',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'cross-site',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36',
    }
    response = requests.get(url, headers=headers, verify=False)

    html = etree.HTML(response.text)
    if html.xpath('//*[@id="activity-name"]/text()'):
        title = html.xpath('//*[@id="activity-name"]/text()')[0].strip()
    else:
        title = ''
    if html.xpath('//*[@id="js_name"]/text()'):
        wechatname = html.xpath('//*[@id="js_name"]/text()')[0].strip()
    else:
        wechatname = ''
    if html.xpath('//*[@id="publish_time"]'):
        timeScriptStr = html.xpath(
            '//*[@id="activity-detail"]/script[12]/text()')[0]
        publishTime = timeScriptStr.split('",s="')[1].split(
            '";\ne(t,n,s,document.getElementById("publish_time"))')[0]
        print(publishTime)
    else:
        publishTime = ''

    result = {
        'title': title,
        'name': wechatname,
        'time': publishTime,
        'link': url
    }
    return result


def random_steep():
    """
    防止封号，随机暂停
    :return:
    """
    a = random.randint(2, 6)
    print("为防止爬取过快，暂停{}秒".format(a))
    time.sleep(a)


if __name__ == '__main__':
    print('-------------------------')
    print('脚本开始运行')
    print('-------------------------')
    runtime=True
    while(runtime):
        print('登录后的cookie可查询十页之后')
        cookie=input('请输入复制的cookie：')
        inputName = input('请输入关键字(不可包含空格):')
        maxPage=10
        maxPageStr=input('请输入查询的最大页数(默认为10):')
        if(int(maxPageStr)):
            maxPage=int(maxPageStr)
        print('开始搜索关键字:“'+inputName+'”，查询页面：'+maxPageStr+'页数')
        checkYN=input("是否正确（y/n），退出输入q：")
        if(checkYN=='y' or checkYN=='Y'):
            runtime=False
        if(checkYN=='q' or checkYN=='Q'):
            exit()
    start_url = 'https://weixin.sogou.com/weixin'
    xls = xlwt.Workbook()  # 创建一个工作簿
    ws = xls.add_sheet(inputName)  # 创建一个工作表
    ws.write(0, 0, '标题')
    ws.write(0, 1, '公众号')
    ws.write(0, 2, '时间')
    ws.write(0, 3, '链接')
    try:
        for page in range(1, maxPage+1):
            print('当前查询的页数:'+str(page))
            urls = get_index(start_url=start_url, page=page)
            ind = (page-1)*10
            for url in urls:
                random_steep()
                real_url = get_real_url(url)
                result = get_detail(real_url)
                ind = ind+1
                print('当前查询的条数:'+str(ind))
                ws.write(ind, 0, result['title'])
                ws.write(ind, 1, result['name'])
                ws.write(ind, 2, result['time'])
                ws.write(ind, 3, result['link'])
                print('标题:'+result['title'])
        # stringname='{inputName}-微信公众号搜索.xls'
        xls.save(inputName+'-微信公众号搜索.xls')
        print('-------------------------')
        print('脚本运行完毕，请在脚本所在目录查看excel。')
        print('-------------------------')
    except Exception as e:
        print(e)
        xls.save('错误-'+inputName+'-微信公众号搜索-未完成.xls')
        print('××××××××××××××××××××××××××')
        print('××××××××脚本异常结束××××××')
        print('×××只保存了一部分数据××××××')
        print('××××××××××××××××××××××××××')
