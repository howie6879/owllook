#!/usr/bin/env python
import logging
import os
import random

from configparser import ConfigParser

_dir = os.path.dirname(__file__)
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s: %(message)s')


def ver_question() -> tuple:
    """
    针对注册问题验证
    问： 小说名
    答： 作者名
    :return: (question,answer)
    """
    cf = ConfigParser()
    file_name = os.path.join(_dir, 'verification.conf')
    try:
        cf.read(file_name, encoding='utf-8')
        index = random.choice(cf.sections())
    except IndexError as e:
        index = "1"
    except Exception as e:
        logging.exception(e)
        return None
    question = cf.get(index, "question")
    return (index, question)


def get_real_answer(index) -> str:
    """
    通过index值获取问题答案
    :param index: 
    :return: bool
    """
    answer = ''
    try:
        cf = ConfigParser()
        file_name = os.path.join(_dir, 'verification.conf')
        cf.read(file_name)
        answer = cf.get(index, "answer")
    except Exception as e:
        logging.exception(e)
    return answer
