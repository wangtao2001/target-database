import time

import openai
import pandas as pd


class GPT:
    def __init__(self, key, data: pd.DataFrame):
        openai.api_key = key
        openai.api_base = "https://api.chatanywhere.com.cn/v1"
        self.data = data

    def run(self, target, relate) -> pd.DataFrame:
        count = 0  # 限制访问次数
        for i in range(self.data.shape[0]):
            if self.data.iloc[i, 4] == 1 and count < 4:  # 限制访问次数，调用4篇
                # title = self.data.iloc[i, 1]
                abstract = self.data.iloc[i, 2]
                # loci = self.data.iloc[i, 5]
                print(f"语言模型判断：{target}")
                max_retry = 0
                while max_retry < 3:  # 超时重试
                    try:
                        answer = self._api(target, abstract, relate)
                        print('获取到响应：', answer)
                        count += 1
                        if answer == 'Y':
                            self.data.iloc[i, 4] = 2
                        break
                    except openai.error.APIError as e:
                        print(f'请求超时, 尝试重试：{max_retry}')
                        max_retry += 1
                        time.sleep(300)
        return self.data

    @staticmethod
    def _api(target, abstract, relate):
        resp = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system",
                 "content": f"You are ChatGPT, a large language model trained by OpenAI. Knowledge cutoff: 2021-09. Current date: {time.strftime('%Y-%m-%d', time.localtime())}"},
                {"role": "user",
                 "content": f"Based on the following the abstract of the literature: {abstract}. Determine if phosphorylation of {target} is associated with {relate} by only answering with the word 'Y' or 'N'. Do not have to explain why."}
            ],
            max_tokens=800,
            temperature=0.7,
        )
        answer = resp['choices'][0]['message']['content']
        return answer
