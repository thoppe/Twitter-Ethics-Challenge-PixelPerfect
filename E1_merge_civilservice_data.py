import pandas as pd
from fuzzywuzzy import fuzz

df = pd.read_csv('data/demographic_labels.csv')
senate = pd.read_csv('data/us-senate.csv')
house  = pd.read_csv('data/us-house.csv')
congress = pd.concat([senate, house])

# Swap name order
congress['name'] = congress['name'].apply(lambda x: ' '.join(x.split()[::-1]))

#print(congress)

# Bad name matching
bad_name_match = [
    # Members can't name match (Kamala is now VP!)
    'Harris, Kamala D.',
    'Loeffler, Kelly',
    'Letlow, Julia',
    'Moore, Barry',
    'Reed, John',
    'Stansbury, Melanie Ann',
    'Tenney, Claudia',

    # Members-at-large not in dataset
    'Norton, Eleanor Holmes',
    'Plaskett, Stacey E.',
    'Gonzalez-Colon, Jenniffer',
    'Radewagen, Aumua Amata Coleman',
    'Sablan, Gregorio Kilili Camacho',
    'San Nicolas, Michael F. Q.',
]

for _, row in df.iterrows():
    dx = congress[congress.state_name == row.State].copy()

    target_name = row['name']
    
    if len(dx) == 0:
        print(target_name)
        continue

    if target_name in bad_name_match:
        continue
    
    dx['delta'] = dx['name'].apply(lambda x: fuzz.token_sort_ratio(target_name, x))
    dx = dx.sort_values('delta', ascending=False)

    score = dx['delta'].values

    cols = ['wikidata', 'title', 'party',
            'gender',	'ethnicity',	'religion',
            'openly_lgbtq'


    print(dx.columns)
    exit()
    
    '''
    # Code to examine and validate weak matches
    if score.max() < 70:
        print(dx[:2]['name'])
        print(row['name'])
        print(score[:2])
        print()
    '''
