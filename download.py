from typing import List

import requests
from bs4 import BeautifulSoup
from tqdm import tqdm
import pandas as pd


class PubMed:
    def __init__(self, term: str, filters: List[str] = None):
        self.base_url = 'https://pubmed.ncbi.nlm.nih.gov/'
        self.links = []
        self.term = term
        self.filters = filters

    def _get_page_nums(self, params):
        r = requests.get(self.base_url, params=params)
        r.encoding = 'utf-8'
        soup = BeautifulSoup(r.text, 'html.parser')
        page_nums = int(soup.find('label', attrs={'class': 'of-total-pages'}).text.lstrip('of '))
        return page_nums

    def _get_links(self):
        params = [['term', self.term]]
        if self.filters:
            for f in self.filters:
                params.append(['filter', f])
        page_nums = self._get_page_nums(params)
        with tqdm(total=page_nums, desc='get links') as tq:
            for page in range(1, page_nums + 1):
                if params[-1][0] != 'page':
                    params.append(['page', page])
                else:
                    params[-1][-1] = page
                r = requests.get(self.base_url, params)
                r.encoding = 'utf-8'
                soup = BeautifulSoup(r.text, 'html.parser')
                self.links.extend(
                    [a.get('href').strip('/') for a in soup.findAll('a', attrs={'class': 'docsum-title'})]
                )
                tq.update(1)

    def _get_info(self, link):
        r = requests.get(self.base_url + link)
        r.encoding = 'utf-8'
        soup = BeautifulSoup(r.text, 'html.parser')
        title = soup.find('h1', attrs={'class': 'heading-title'}).text.strip()
        ps = soup.find('div', attrs={'class': 'abstract-content'}).findAll('p')
        abstract = ''
        if len(ps) > 1:  # 摘要分段
            for p in ps:
                if len(p.contents) == 1:  # 有些分段没有title
                    abstract += p.contents[0].text.strip() + '\n'
                else:
                    abstract += p.contents[1].text.strip() + p.contents[2].text.strip() + '\n'
            abstract = abstract.strip()
        else:
            abstract = ps[0].text.strip()
        keywords = ''  # 可能不含有关键词
        for s in soup.find('div', attrs={'class': 'abstract'}).children:
            if s.name == 'p':
                keywords += s.contents[2].text.strip()
        return self.base_url + link, title, abstract, keywords

    def save_excel(self):
        self._get_links()
        data = pd.DataFrame(columns=['link', 'title', 'abstract', 'keywords'])
        with tqdm(total=len(self.links), desc='download abstract') as tq:
            for link in self.links:
                data.loc[len(data)] = list(self._get_info(link))
                tq.update(1)
        data.to_excel(f"data/pubmed-{self.term}-{self.filters if self.filters else ''}.xlsx", index=False)
