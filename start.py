# -*- coding:utf-8 -*-
import os

import requests
from bs4 import BeautifulSoup
import m3u8_To_MP4
import logging.config
import yaml

with open("log_conf.yaml", "r") as f:
    dict_conf = yaml.safe_load(f)

logging.config.dictConfig(dict_conf)
logger = logging.getLogger('logger2')

socks5_add = "socks5://localhost:10808"
pony = r"https://91porny.com/video/category/latest"


def get_proxy():
    return {
        'http': socks5_add,
        'https': socks5_add
    }


class WebDriver:
    def __init__(self, is_proxy):
        self.session = requests.session()
        self.isProxy = is_proxy
        self.head = {
            'user-agent':
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.82 Safari/537.36',
            # 'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9'
            # 'accept-encoding': 'gzip, deflate, br',
            # 'accept-language': 'zh-CN,zh;q=0.9'
        }

    def get(self, url):
        return self.session.get(url, timeout=11, headers=self.head, verify=False, proxies=get_proxy())


class VideoDetail:
    def __init__(self, view_id, view_page, author, datetime, title, data_src):
        self.view_id = view_id
        self.view_page = view_page
        self.author = author
        self.datetime = datetime
        self.title = title
        self.data_src = data_src


def download(video: VideoDetail, head):
    try:
        m3u8_To_MP4.multithread_download(video.data_src,
                                         customized_http_header=head,
                                         mp4_file_name=video.view_id,
                                         tmpdir="./")
    except Exception as e:
        logger.warning(e)
    logger.info("clean ------\n")
    os.remove("ts_recipe.txt")
    for root, dirs, files in os.walk('./'):
        for name in files:
            if name.endswith(".ts"):
                os.remove(name)


def test():
    # url = r'https://91porny.com/video/view/539784935'
    url = r'https://91porny.com/video/view/85241f4c1843abf2b914'

    logger.info("into " + url)
    view_id = url.split("/")[-1:][0]
    web = WebDriver(True)
    resp = web.get(url)
    bs = BeautifulSoup(resp.text, 'html5lib')
    video = bs.select_one("#videoShowPage video")
    data_src = video.attrs["data-src"]
    logger.info("data_src " + data_src)


if __name__ == '__main__':
    test()
