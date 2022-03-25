import requests
from bs4 import BeautifulSoup
import m3u8_To_MP4

session = requests.session()
head = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.82 Safari/537.36',
    # 'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9'
    # 'accept-encoding': 'gzip, deflate, br',
    # 'accept-language': 'zh-CN,zh;q=0.9'
}
pony = r"https://91porny.com/video/category/latest"


def get_proxy():
    socks5_add = "socks5://localhost:10808"
    return {
        'http': socks5_add,
        'https': socks5_add
    }


def get(url):
    return session.get(url, timeout=11, headers=head, verify=False, proxies=get_proxy())


def video_download():
    pass


def test():
    resp = get('https://91porny.com/video/view/539784935')
    bs = BeautifulSoup(resp.text, 'html5lib')
    video = bs.select_one("#videoShowPage video")
    data_src = video.attrs["data-src"]
    print(data_src)
    m3u8_To_MP4.multithread_download(data_src, customized_http_header=head, mp4_file_name="yes.mkv", tmpdir=".")


if __name__ == '__main__':
    test()
