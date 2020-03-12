# -*- coding: utf-8 -*-
import sqlite3
import http.cookiejar
import pdb
import scrapy
from scrapy.utils.project import get_project_settings
from scrapy.crawler import CrawlerProcess
from scrapy_selenium import SeleniumRequest

ff_cookie = '/Users/v/works/scrapy/download_web/dc/c.sqlite'


class CsSpider(scrapy.Spider):
    name = 'cs'
    allowed_domains = ['order.jd.com']

    def start_requests(self):
        headers = {'User-Agent': 'User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:68.0) Gecko/20100101 Firefox/68.0'}
        urls = ["https://joycenter.jd.com/msgCenter/queryMessage.action",
                'https://order.jd.com/center/list.action']
        for url in urls:
            #yield scrapy.Request(url=url, callback=self.parse_page, headers=headers, cookies=get_cookies(ff_cookie))
            yield SeleniumRequest(url=url, callback=self.parse_page, cookies={ k:v for k, v in get_cookies(ff_cookie) })

    def parse_page(self, response):
        print(response.request.meta['driver'].title)

        from scrapy.shell import inspect_response
        inspect_response(response, self)

        filename = "test.html"
        with open(filename, "wb") as f:
            f.write(response.body)

        self.log('Saved files {}'.format(filename))

        return


def get_cookies(ff_cookies):
    con = sqlite3.connect(ff_cookies)
    cur = con.cursor()
    cur.execute("SELECT host, path, isSecure, expiry, name, value FROM moz_cookies where baseDomain='jd.com'")

    cookies = list()
    count = 0
    to_add = ['shshshfpa',
              '__jda',
              'shshshfpb',
              'shshshfp',
              'TrackID',
              'pinId',
              'qd_uid',
              'qd_fs',
              'qd_ls',
              'qd_ts',
              'qd_sq',
              'ipLoc-djd',
              '__jdv',
              'pin',
              'unick',
              '_tp',
              '_pst',
              '3AB9D23F7A4B3C9B',
              '__jdc',
              'areaId',
              'wq_logid',
              'retina',
              'cid',
              'webp',
              '__wga',
              'sc_width',
              'sk_history',
              'visitkey',
              'wlfstk_smdl',
              'ceshi3.com',
              'user-key',
              'cn',
              'ipLocation',
              '__tak',
              'qd_ad',
              'thor',
              'qd_sid',
              '__jdb']

    for item in cur.fetchall():
        '''
        c = http.cookiejar.Cookie(0, item[4], item[5], # 4 and 5 are name and value
                                  None, False,
                                  item[0], item[0].startswith('.'), item[0].startswith('.'),
                                  item[1], False,
                                  item[2],
                                  item[3], item[3] == "",
                                  None, None, {})
        '''
        if not item[4] in to_add:
            print(item[4])
            continue
        c = {'name': item[4], 'value': item[5]}

        #print(c)
        cookies.append(c)  # same structure, should be able to use ... it is the same...
        count += 1
    print(count, "cookies got")

    return cookies

if __name__ == '__main__':
    settings = get_project_settings()

    settings['SELENIUM_DRIVER_NAME'] = 'chrome'
    settings['SELENIUM_COMMAND_EXECUTOR'] = 'http://localhost:4444/wd/hub'
    settings['SELENIUM_DRIVER_ARGUMENTS'] =['-headless']
    settings['DOWNLOADER_MIDDLEWARES'] = {'scrapy_selenium.SeleniumMiddleware':800}

    c = CrawlerProcess(settings)
    pdb.set_trace()
    c.crawl(CsSpider)
    c.start()
