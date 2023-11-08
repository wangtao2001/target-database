phosphorylation_loci = ['Tyr', 'Thr', 'Ser']

flow_setting = [
    {
        "number": 1,
        "term": "phosphorylation cancer",
        "relate": "cancer",
        "keywords": ["phosphorylation", "cancer"],
        "loci": phosphorylation_loci,
        "optional": ['anti-apoptotic', 'cancer', 'carcinoma', 'tumor', 'migration', 'cell growth', 'proliferation', 'invasion', 'lymphoma', 'leukemia', 'carcinogenesis', 'Oncogenesis', 'Neoplasia', 'Neoplastic', 'Malignancy', 'Malignancies', 'Metastasis', ' Metastatic dissemination', 'Carcinogenic', 'Oncogenic', 'neuroblastoma', 'Adenocarcinoma', 'angiogenesis', 'tumorigenic', 'tumorigenesis', 'melanoma', 'oncoprotein', 'sarcomas', 'dysplasia', 'precancerous lesions', 'precancerosis', ' proapoptotic']
    },
    {
        "number": 2,
        "term": "phosphorylation activation",
        "relate": "activation",
        "keywords": ["phosphorylation", "activation"],
        "loci": phosphorylation_loci,
        "optional": ['regulate', 'modulate', 'increase activity', 'induce', 'upstream', 'mediate', 'upregulate']
    },
    {
        "number": 3,
        "term": "cancer",
        "relate": "cancer",
        "keywords": ["cancer"],
        "loci": phosphorylation_loci,
        "optional": ['overexpression', 'oncogenic', 'cancer', 'tumor', 'anti-apoptotic', 'carcinoma', 'migration', 'cell growth', 'proliferation', 'invasion']
    },
    {
        "number": 4,
        "term": "phosphorylation",
        "relate": "cancer",
        "keywords": ["phosphorylation"],
        "loci": phosphorylation_loci,
        "optional": ['anti-apoptotic', 'cancer', 'carcinoma', 'tumor', 'migration', 'cell growth', 'proliferation', 'invasion', 'lymphoma', 'leukemia', 'carcinogenesis', 'Oncogenesis', 'Neoplasia', 'Neoplastic', 'Malignancy', 'Malignancies', 'Metastasis', ' Metastatic dissemination', 'Carcinogenic', 'Oncogenic', 'neuroblastoma', 'Adenocarcinoma', 'angiogenesis', 'tumorigenic', 'tumorigenesis', 'melanoma', 'oncoprotein', 'sarcomas', 'dysplasia', 'precancerous lesions', 'precancerosis', ' proapoptotic']
    }
]
