#!/usr/bin/env python
"""
 Created by howie.hu at 17-9-22.
"""


class ResponseField():
    """
    Define the response field
    """
    MESSAGE = 'info'
    STATUS = 'state'
    DATA = 'data'
    FINISH_AT = 'finished_at'


class ResponseReply():
    """
    Define field description
    """
    # ERROR
    UNKNOWN_ERR = '未知错误'
    PARAM_ERR = '参数错误!'
    PARAM_PARSE_ERR = "参数解析错误!"
    DB_ERROR = "数据库操作错误"
    # FORBIDDEN
    IP_FORBIDDEN = "ip被禁"
    # NOT AUTHORIZED
    NOT_AUTHORIZED = "验证未通过"
    # SUCCESS
    SUCCESS = 'ok'


class ResponseCode():
    """
    Define the response code
    """
    SUCCESS = 200
    CREATED = 201
    NO_CONTENT = 204
    BAD_REQUEST = 400
    NOT_AUTHORIZED = 401
    FORBIDDEN = 403
    NOT_FOUND = 404
    SERVER_ERR = 500


class UniResponse():
    NOT_AUTHORIZED = {ResponseField.MESSAGE: ResponseReply.NOT_AUTHORIZED,
                      ResponseField.STATUS: ResponseCode.NOT_AUTHORIZED}
    PARAM_PARSE_ERR = {ResponseField.MESSAGE: ResponseReply.PARAM_PARSE_ERR,
                       ResponseField.STATUS: ResponseCode.BAD_REQUEST}
    PARAM_ERR = {ResponseField.MESSAGE: ResponseReply.PARAM_ERR,
                 ResponseField.STATUS: ResponseCode.BAD_REQUEST}
    PARAM_UNKNOWN_ERR = {ResponseField.MESSAGE: ResponseReply.UNKNOWN_ERR,
                         ResponseField.STATUS: ResponseCode.BAD_REQUEST}
    IP_FORBIDDEN = {ResponseField.MESSAGE: ResponseReply.IP_FORBIDDEN,
                    ResponseField.STATUS: ResponseCode.FORBIDDEN}
    SERVER_DB_ERR = {ResponseField.MESSAGE: ResponseReply.DB_ERROR,
                     ResponseField.STATUS: ResponseCode.SERVER_ERR}
    SERVER_UNKNOWN_ERR = {ResponseField.MESSAGE: ResponseReply.UNKNOWN_ERR,
                          ResponseField.STATUS: ResponseCode.SERVER_ERR}
    SUCCESS = {ResponseField.MESSAGE: ResponseReply.SUCCESS,
               ResponseField.STATUS: ResponseCode.SUCCESS}
