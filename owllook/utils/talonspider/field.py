#!/usr/bin/env python

class BaseField(object):
    """
    BaseField class
    """

    def __init__(self, css_select=None, xpath_select=None):
        """
        Init BaseField class
        url: http://lxml.de/index.html
        :param css_select: css select http://lxml.de/cssselect.html
        :param xpath_select: http://www.w3school.com.cn/xpath/index.asp
        :param re_select: use regular expression to extract a field value
        """
        self.css_select = css_select
        self.xpath_select = xpath_select


class TextField(BaseField):
    """
    TextField class for a field
    """

    def __init__(self, css_select=None, xpath_select=None):
        super(TextField, self).__init__(css_select, xpath_select)

    def extract_value(self, html):
        """
        Use css_select or re_select to extract a field value
        :return:
        """
        value = ''
        if self.css_select:
            value = html.cssselect(self.css_select)
            value = value[0].text.strip() if len(value) == 1 else value
        elif self.xpath_select:
            value = html.xpath(self.xpath_select)
            value = value[0].text.strip() if len(value) == 1 else value
        else:
            raise ValueError('%s field: css_select or xpath_select is expected' % self.__class__.__name__)
        return value


class AttrField(BaseField):
    """
    AttrField class for a field
    """

    def __init__(self, attr, css_select=None, xpath_select=None):
        super(AttrField, self).__init__(css_select, xpath_select)
        self.attr = attr

    def extract_value(self, html):
        """
        Use css_select or re_select to extract a field value
        :return:
        """
        value = ''
        if self.css_select:
            value = html.cssselect(self.css_select)
            value = value[0].get(self.attr).strip()
        elif self.xpath_select:
            value = html.xpath(self.xpath_select)
        else:
            raise ValueError('%s field: css_select or xpath_select is expected' % self.__class__.__name__)
        return value
