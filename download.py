from typing import List, Union

import requests
from bs4 import BeautifulSoup
from tqdm import tqdm
import pandas as pd


class PubMed:
    def __init__(self, term: str):
        self.base_url = 'https://pubmed.ncbi.nlm.nih.gov/'
        self.term = term

    def _get_page_nums(self, params) -> int:
        r = requests.get(self.base_url, params=params)
        r.encoding = 'utf-8'
        soup = BeautifulSoup(r.text, 'html.parser')
        s = soup.find('label', attrs={'class': 'of-total-pages'})
        page_nums = 0
        if s is not None:
            page_nums = int(s.text.lstrip('of ').replace(',', ''))
        # 这里还有一种情况 只有一个搜索结果会直接跳转到详情页
        if soup.find('div', attrs={'class': 'multiple-results-actions '}) is not None:
            page_nums = -1
        if page_nums > 10:
            page_nums = 10
        return page_nums

    def _get_links(self) -> List[str]:
        links = []
        params = [['term', self.term], ['filter', 'years.2010-2024']]
        page_nums = self._get_page_nums(params)
        if page_nums == 0:
            return links
        if page_nums == -1:
            r = requests.get(self.base_url, params=params)
            return [r.url.split('/')[-2]]  # 获取302真实url
        with tqdm(total=page_nums, desc='get links') as tq:
            for page in range(1, page_nums + 1):
                if params[-1][0] != 'page':
                    params.append(['page', page])
                else:
                    params[-1][-1] = page
                r = requests.get(self.base_url, params)
                r.encoding = 'utf-8'
                soup = BeautifulSoup(r.text, 'html.parser')
                links.extend(
                    [a.get('href').strip('/') for a in soup.findAll('a', attrs={'class': 'docsum-title'})]
                )
                tq.update(1)
        return links

    def _get_info(self, link):
        r = requests.get(self.base_url + link)
        r.encoding = 'utf-8'
        soup = BeautifulSoup(r.text, 'html.parser')
        t = soup.find('h1', attrs={'class': 'heading-title'})
        title = ''
        if t is not None:  # 没有标题
            title = t.text.strip()
        ab = soup.find('div', attrs={'class': 'abstract-content'})
        if ab is None:  # 没有摘要
            return None
        ps = ab.findAll('p')
        abstract = ''
        try:
            if len(ps) > 1:  # 摘要分段
                for p in ps:
                    if len(p.contents) == 1:  # 有些分段没有title
                        abstract += p.contents[0].text.strip() + '\n'
                    else:
                        abstract += p.contents[1].text.strip() + p.contents[2].text.strip() + '\n'
                abstract = abstract.strip()
            else:
                abstract = ps[0].text.strip()
        except IndexError:
            ...
        keywords = ''  # 可能不含有关键词
        for s in soup.find('div', attrs={'class': 'abstract'}).children:
            if s.name == 'p':
                keywords += s.contents[2].text.strip()
        return self.base_url + link, title, abstract, keywords

    def download(self) -> Union[pd.DataFrame, None]:
        links = self._get_links()
        if len(links) == 0:
            return None
        data = pd.DataFrame(columns=['link', 'title', 'abstract', 'keywords'])
        with tqdm(total=len(links), desc='download abstract') as tq:
            for link in links:
                info = self._get_info(link)
                if info is None:
                    continue
                data.loc[len(data)] = list(info)
                tq.update(1)
        return data
