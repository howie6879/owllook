#!/usr/bin/env python
"""
 Created by howie.hu at 2018/5/28.
"""

import os
import sys

import pytest

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from owllook.spiders.qidian_novel_info import QidianNovelInfoItem


def test_qidian_novel_info():
    item_data = QidianNovelInfoItem.get_item(url='http://book.qidian.com/info/1004608738')

    assert item_data['novel_name'] == '圣墟'
