import re


class HeuristicService:
    def get_keywords(self, text):
        kw = re.findall("Testing|Software development|Quality Assurance|Agile tools and methodologies|test case planning|automation development|Java|Kibana|ElasticSearch|scripting languages|Python|Perl|shell script|Groovy|Github|Jenkins|CI/CD|Snowflake|AWS|Azure|IBM Cloud|RedHat OpenShift|Jupyter|Kubernetes", text)
        return kw
