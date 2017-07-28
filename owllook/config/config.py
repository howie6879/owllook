#!/usr/bin/env python
import os


class Config():
    """
    Basic config for owllook
    """

    # Application config
    DEBUG = True
    HOST = ['127.0.0.1:8001', '0.0.0.0:8001', '127.0.0.1:8002', '0.0.0.0:8002']
    TIMEZONE = 'Asia/Shanghai'
    BASE_DIR = os.path.dirname(os.path.dirname(__file__))
    USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.95 Safari/537.36'
    WEBSITE = dict(
        IS_RUNNING=True,
        TOKEN=''
    )

    # Engine config
    URL_PHONE = 'https://m.baidu.com/s'
    URL_PC = 'http://www.baidu.com/s'
    BAIDU_RN = 15
    SO_URL = "https://www.so.com/s"
