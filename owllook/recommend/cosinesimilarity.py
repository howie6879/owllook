import numpy as np

from functools import reduce
from math import sqrt


class CosineSimilarity(object):
    """
    余弦相似性计算相似度
    """

    def __init__(self, initQuery, userData):
        self.title = initQuery
        self.data = userData

    def create_vector(self):
        """
        创建兴趣向量
        :return: wordVector = {} 目标用户以及各个兴趣对应的向量
        """
        wordVector = {}
        for web, value in self.data.items():
            wordVector[web] = []
            titleVector, valueVector = [], []
            allWord = set(self.title + value)
            for eachWord in allWord:
                titleNum = self.title.count(eachWord)
                valueNum = value.count(eachWord)
                titleVector.append(titleNum)
                valueVector.append(valueNum)
            wordVector[web].append(titleVector)
            wordVector[web].append(valueVector)
        return wordVector

    def calculate(self, wordVector):
        """
        计算余弦相似度
        :param wordVector: wordVector = {} 目标用户以及各个兴趣对应的向量
        :return: 返回各个用户相似度值
        """
        resultDic = {}
        for web, value in wordVector.items():
            valueArr = np.array(value)
            # 余弦相似性
            squares = []
            numerator = reduce(lambda x, y: x + y, valueArr[0] * valueArr[1])
            square_title, square_data = 0.0, 0.0
            for num in range(len(valueArr[0])):
                square_title += pow(valueArr[0][num], 2)
                square_data += pow(valueArr[1][num], 2)
            squares.append(sqrt(square_title))
            squares.append(sqrt(square_data))
            mul_of_squares = reduce(lambda x, y: x * y, squares)
            value = float(('%.5f' % (numerator / mul_of_squares)))
            if value > 0:
                resultDic[web] = value
        resultDic = [{v[0]: v[1]} for v in sorted(resultDic.items(), key=lambda d: d[1], reverse=True)]
        return resultDic
