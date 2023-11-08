import pandas as pd
from download import PubMed
from parse import AbstractParser
from llm import GPT
from settings import flow_setting

target_excel = "assets/41573_2018_BFnrd2018167_MOESM8_ESM.xlsx"
target_list = list(pd.read_excel(target_excel)['Target'].dropna(axis=0, how='any'))
result_target_list = list(pd.read_excel('result/第二次筛选/result.xlsx')['靶点'].dropna(axis=0, how='any'))
# target_list_local = list(set("-".join(f.split("-")[1:-1]) for f in os.listdir('data')))  # 本地文件
key = 'sk-A7woJYWdLmLThlyUWTN2FxeZgniXD8uV9OTszoyJYk67rJ3R'
target_related = []


def related(d: pd.DataFrame) -> bool:
    for i in range(d.shape[0]):
        if d.iloc[i, 4] == 2:  # 经过llm判断, 至少有一篇是相关的
            return True
    return False


def run(target, number: int, term, relate, keywords=None, loci=None, optional=None) -> bool:
    # 这里先做一个转换，因为有的靶点中可能存在/
    print(f'当前靶点：{target} 分支序号：{number}')
    target_file_name = target
    if "~" in target:  # 从本地文件读取
        target = target.replace("~", "/")
    if "/" in target:  # 从靶点库读取
        target_file_name = target.replace("/", "~")

    try:
        data = pd.read_excel(f'data/pubmed-{target_file_name}-{number}.xlsx')
    except FileNotFoundError:
        print(f'重新下载')
        data = PubMed(f'{target} {term}').download()
        if data is None:
            print("无数据")
            return False

    data = AbstractParser(data).parse(target, keywords, loci, optional)
    data = GPT(key, data).run(target, relate)
    data.to_excel(f'data/pubmed-{target_file_name}-{number}.xlsx', index=False)  # 重新保存
    if related(data):
        return True
    return False
    # 这里返回的False可能是无关或者没有下载到文件(没下载到就不会保存实体文件)


related_target = []

if __name__ == '__main__':
    # 流程控制
    for target in result_target_list:
        print(f'当前靶点：{target}')
        if run(target, **flow_setting[0]):  # 1
            related_target.append((target, 1))
        else:
            if run(target, **flow_setting[1]):  # 2
                if run(target, **flow_setting[2]):  # 3
                    related_target.append((target, 3))
                else:
                    continue
            else:
                if run(target, **flow_setting[3]):  # 4
                    related_target.append((target, 4))
                else:
                    continue
    # 最后的处理流程还有获取全文根据结论找到位点 氨基酸
