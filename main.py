from download import PubMed
from parse import AbstractParser
from llm import GPT

if __name__ == '__main__':
    pubmed = PubMed('HDAC1 phosphorylation cancer')
    excel_file = pubmed.save_excel()
    parse = AbstractParser(excel_file)
    parse.parse(['phosphorylation'],
                 ['Tyr'],
                 ['anti-apoptotic', 'cancer', 'carcinoma', 'tumor', 'migration', 'cell growth', 'proliferation', 'invasion'])
    gpt = GPT("sk-yhdhYzsSfkfeNXK9T98xdH1TNGOlpspVUeDTVT8oxkbDbLSe", excel_file)
    gpt.run('HDAC1 phosphorylation')
