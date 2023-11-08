import os
import pandas as pd
import json

related_list = []

filenames = os.listdir('data')
filenames.sort()
for f in os.listdir('data'):
    li = f.split("-")
    target_name = "-".join(li[1:-1])
    if '~' in target_name:
        target_name = target_name.replace('~', '-')
    number = int(li[-1].rstrip('.xlsx'))
    data = pd.read_excel(f'data/{f}')

    # 按number排序。只要里面有一个就行
    if target_name in [r['target'] for r in related_list]:
        continue

    if number != 2:  # 只有number在2的情况下不能直接导出
        links = []
        locis = []
        for i in range(data.shape[0]):
            if data.iloc[i, 4] == 2:
                links.append(data.iloc[i, 0])
                lo = data.iloc[i, 5]
                if pd.isna(lo):
                    locis.append("")
                    # 这里可以稍微处理一下
                    # 尝试从结论寻找
                else:
                    locis.append(lo)
                # 只有在number为2的情况下才会写入
        if len(links) != 0:
            related_list.append({
                "target": target_name,
                "number": number,
                "links": links,
                "locis": locis
            })


with open('result/result.json', 'w') as f:
    json.dump(related_list, f)

print(len(related_list))

excel_dict = {
    "靶点": [],
    "流程": [],
    "链接": [],
    "氨基酸": []
}
for target in related_list:
    si = len(target['links'])
    excel_dict['靶点'].extend([target['target']] * si)
    excel_dict['流程'].extend([target['number']] * si)
    excel_dict['链接'].extend(target['links'])
    excel_dict['氨基酸'].extend(target['locis'])
data = pd.DataFrame(excel_dict)
data.to_excel(f'result/result.xlsx', index=False)


