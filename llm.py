import openai
import pandas as pd


class GPT:
    def __init__(self, key, excel_file):
        openai.api_key = key
        openai.api_base = "https://api.chatanywhere.com.cn/v1"
        self.excel_file = excel_file
        self.data = pd.read_excel(excel_file)

    def run(self, keyword):
        for i in range(self.data.shape[0]):
            if self.data.iloc[i, 4] == 1:
                abstract = self.data.iloc[i, 2]
                resp = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system",
                         "content": "You are ChatGPT, a large language model trained by OpenAI. Knowledge cutoff: 2021-09. Current date: 2023-09-07"},
                        {"role": "user",
                         "content": f"Based on the following summary of the literature: {abstract}, please determine if {keyword} is related to cancer by answering with Y or N. Do not have to explain why."}
                    ],
                    max_tokens=800,
                    temperature=0.7,
                )
                answer = resp['choices'][0]['message']['content']
                if answer == 'Y':
                    self.data.iloc[i, 4] = 2
        self.data.to_excel(self.excel_file, index=False)
