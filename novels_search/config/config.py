#!/usr/bin/env python
import logging

# Search engine
# eg:
# https://m.baidu.com/s?word=***+**
# https://www.baidu.com/s?q=&wd=python&ie=utf-8&tn=baidulocal&ct=2097152&si=jianshu.com&cl=3
# https://www.baidu.com/s?wd=%E6%8B%A9%E5%A4%A9%E8%AE%B0+%E5%B0%8F%E8%AF%B4&ie=utf-8&tn=baidulocal
# https://www.baidu.com/s?wd=python&ie=utf-8&tn=baidulocal&ct=2097152&si=cnblogs.com&rn=50
URL_PHONE = 'https://m.baidu.com/s'
URL_PC = 'http://www.baidu.com/s'
USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.95 Safari/537.36'

# logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s: %(message)s')
LOGGER = logging.getLogger('root')
