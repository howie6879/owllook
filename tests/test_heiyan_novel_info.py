#!/usr/bin/env python
"""
 Created by howie.hu at 2018/5/28.
"""
import os
import sys

import pytest

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from owllook.spiders.heiyan_novel_info import HYNovelInfoItem


def test_heiyan_novel_info():
    url = 'http://www.heiyan.com/book/62599'
    item_data = HYNovelInfoItem.get_item(url=url)

    assert item_data['novel_name'] == '神仙微信群'
