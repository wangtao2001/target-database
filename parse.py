from typing import List
import pandas as pd
import re


class AbstractParser:
    def __init__(self, excel_file):
        self.excel_file = excel_file
        self.data = pd.read_excel(excel_file)

    def parse(self, keywords: List, loci: List = None, optional: List = None):
        # 考虑大小写
        # 添加一列，用于存储匹配结果
        self.data['status'] = 0
        for i in range(self.data.shape[0]):
            abstract = self.data.iloc[i, 2]
            status = [True] * 3
            # 关键词匹配
            for keyword in keywords:
                pattern = re.compile(keyword, re.IGNORECASE)  # 这里正则要重新写
                if not pattern.search(abstract):
                    status[0] = False
                    break
            # 位点匹配
            if loci:
                for lo in loci:
                    pattern = re.compile(lo + '\d[0-4]', re.IGNORECASE)
                    # 只需要匹配到一个就行
                    status[1] = False
                    if pattern.search(abstract):
                        status[1] = True
                        break
            # 可选词匹配
            if optional:
                for op in optional:
                    pattern = re.compile(op, re.IGNORECASE)
                    status[2] = False
                    if pattern.search(abstract):
                        status[2] = True
                        break
            if all(status):
                self.data.iloc[i, 4] = 1
        self.data.to_excel(self.excel_file, index=False)  # 重新写回去
        return self.excel_file
