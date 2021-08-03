from dspipe import Pipe
import pandas as pd
import bs4

def compute(f0):
    with open(f0) as FIN:
        soup = bs4.BeautifulSoup(FIN.read(), 'lxml')

    data = []
    for block in soup.find_all('div', class_="quick-search-member"):

        info = { }
        try:
            img = block.find('img')
            filename = img['src'].split('/')[-1].split('.jpg')[0]
        except:
            continue

        info['filename'] = filename
        info['name' ] = img['alt']

        for item in block.find_all('span', class_ = "result-item"):
            label = item.find('strong').get_text().strip(':')
            text = item.find('span').get_text().strip()
            info[label] = text

        print(info)
        data.append(info)
    return data


P = Pipe('data/html_rip/', input_suffix='*.html')

data = []
for block in P(compute, -1):
    data.extend(block)

df = pd.DataFrame(data).set_index('filename')
df = df.drop_duplicates(subset=['name']).sort_values('filename')
df.to_csv("extended_labels.csv")
print(df)

