import requests
from bs4 import BeautifulSoup
from tqdm import tqdm


class PubMed:
    def __init__(self):
        self.base_url = 'https://pubmed.ncbi.nlm.nih.gov/'
        self.abstract_links = []

    def _get_page_nums(self, params):
        r = requests.get(self.base_url, params=params)
        r.encoding = 'utf-8'
        soup = BeautifulSoup(r.text, 'html.parser')
        page_nums = int(soup.findAll('label', attrs={'class': 'of-total-pages'})[0].text.lstrip('of '))
        return page_nums

    def get_links(self, term, filter=None):
        params = {'term': term}
        if filter:
            params['filter'] = filter
        page_nums = self._get_page_nums(params)
        with tqdm(total=page_nums) as tq:
            for page in range(1, page_nums+1):
                params['page'] = page
                r = requests.get(self.base_url, params)
                r.encoding = 'utf-8'
                soup = BeautifulSoup(r.text, 'html.parser')
                self.abstract_links.append(
                    [a.get('href').strip('/') for a in soup.findAll('a', attrs={'class': 'docsum-title'})]
                )
                tq.update(1)
        print(self.abstract_links)


p = PubMed()
p.get_links("HDAC1 phosphorylation cancer")
