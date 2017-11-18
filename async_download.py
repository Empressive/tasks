import re
import os
import random
import asyncio
import aiohttp
import urllib.request

from lxml import html
from urllib.parse import urlsplit, quote

urls = [
    'https://aiohttp.readthedocs.io/en/stable/', 'http://www.python.org', 'http://mail.ru', 'https://blog.ostrovok.ru'
]


async def get_images(url):
    session = aiohttp.ClientSession()

    protocol = urlsplit(url)[0]
    resource = urlsplit(url)[1]

    response = await session.get(url)
    data = await response.text()

    print('Download files from {}'.format(url))

    page = html.fromstring(data)

    images = page.xpath('//img/@src')

    make_resource_directory(resource)

    os.chdir(resource)

    for img in images:
        protocol_in_path = re.findall('^http://|https://', img)
        slashes = re.findall('^//', img)

        starts_with_slash = re.findall('^/', img)

        link = img

        if not protocol_in_path and not slashes:
            if not starts_with_slash:
                link = '{}{}'.format(url, img)
            else:
                link = '{}://{}/{}'.format(protocol, resource, img)

        if slashes:
            link = '{}://{}'.format(protocol, img.replace('//', ''))

        try:
            download_file(link)
        except UnicodeEncodeError:
            link = urlsplit(link)

            download_file('{}://{}{}'.format(link[0], link[1], quote(link[2])))

    os.chdir('../')

    session.close()

    return data


def download_file(url):
    urllib.request.urlretrieve(url, '{}'.format(random.randrange(0, 999999999)))


def make_resource_directory(resource):
    if not os.path.exists(resource):
        os.mkdir(resource)


futures = [get_images(url) for url in urls]

loop = asyncio.get_event_loop()
loop.run_until_complete(asyncio.wait(futures))
