from typing import List
import pandas as pd
import re


class AbstractParser:
    def __init__(self, data: pd.DataFrame):
        self.data = data

    def parse(self, target, keywords: List, loci: List = None, optional: List = None) -> pd.DataFrame:
        keywords.append(target)  # 必选词中加入靶点
        # 列的初始化
        self.data['status'] = 0
        self.data['loci'] = ''
        for i in range(self.data.shape[0]):
            # 遍历每一行文献
            title = self.data.iloc[i, 1]
            abstract = self.data.iloc[i, 2]
            content = title + " " + abstract  # 一起搜索
            status = [True] * 3
            # 关键词匹配 必选词也可能为空
            if keywords:
                for keyword in keywords:
                    pattern = re.compile(keyword, re.IGNORECASE)
                    if not pattern.search(content):  # 标题和摘要都没有匹配到
                        status[0] = False
                        break
            # 位点匹配 位点也先不做要求，只把有的记录下来
            if loci:
                # status[1] = False
                for lo in loci:
                    pattern = re.compile(lo + '\d{1,5}', re.IGNORECASE)  # 我恨正则表达式
                    # 把匹配到的位点记录下来

                    if pattern.search(content):
                        # status[1] = True
                        r = pattern.search(content).group()
                        if r not in self.data.iloc[i, 5]:
                            self.data.iloc[i, 5] += r + ';'
            self.data.iloc[i, 5] = self.data.iloc[i, 5].rstrip(';')  # 去掉最后一个分号
            # 可选词匹配 只要有一个就行
            if optional:
                status[2] = False
                for op in optional:
                    pattern = re.compile(op, re.IGNORECASE)
                    if pattern.search(content):
                        status[2] = True
                        break
            if all(status):  # 可选词和必选词都包含
                self.data.iloc[i, 4] = 1
        return self.data
