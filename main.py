from download import PubMed


if __name__ == '__main__':
    p = PubMed('HDAC1 phosphorylation cancer')
    p.save_excel()
