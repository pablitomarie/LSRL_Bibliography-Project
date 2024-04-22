import pandas as pd
import spacy

df = pd.read_csv('LSRL.csv')
nullAbstracts = df[df['Abstract'].isnull()]  # dataframe of publications with empty abstracts
df = df.drop(nullAbstracts.index).reset_index(drop=True)

df['Title'] = df['Title'].str.lower()
df['Manual Tags'] = df['Manual Tags'].str.lower()
df['Abstract'] = df['Abstract'].str.lower()

# LANGUAGE TAGS
#############################
languages = ['english', 'spanish', 'french', 'italian', 'romanian', 'rumanian', 'portuguese', 'catalan']
# creates a dictionary with journal title as key and language tag as value
# only looks at journals with no manual tags
titlesLang = {}
for title in df[df['Manual Tags'].isna() == True]['Title']:
    langLst = []  # create a list of potential languages for each title
    for language in languages:
        if language in title:  # first check if any language is in the title and then add it to the list
            langLst.append(language)
        else:
            if language in df[df['Title'] == title]['Abstract'].item():  # check if language is in abstract
                langLst.append(language)
    if langLst:  # turn list into a string and add to dictionary
        langStr = ', '.join(langLst)
        titlesLang[title] = langStr
# add language to manual tags for journals with no manual tags
for title in titlesLang.keys():
    df.loc[df['Title'] == title, 'Manual Tags'] = titlesLang[title]

noTags = df[df['Manual Tags'].isna() == True]['Title']  # journal titles with no tags still

# load spacy english model
nlp = spacy.load("en_core_web_sm")
# remove stopwords and punct in abstracts and titles
df['Abstract'] = df['Abstract'].apply(lambda x: ' '.join([token.text for token in nlp(x) if (not token.is_stop and not token.is_punct)]))
df['Title'] = df['Title'].apply(lambda x: ' '.join([token.text for token in nlp(x) if (not token.is_stop and not token.is_punct)]))
# get value counts in ALL abstracts
# counts = pd.Series(' '.join(df['Abstract']).split()).value_counts()

df = df.assign(Decade = (df['Date'] // 10) * 10)
decades = sorted(list(df['Decade'].unique()))

for yr in decades:
    dfDecade = df[df['Decade'] == yr]
    top10Titles = pd.Series(' '.join(dfDecade['Title']).split()).value_counts()[:10]
    top10Abstracts = pd.Series(' '.join(dfDecade['Abstract']).split()).value_counts()[:10]
    print(top10Titles)
    print(top10Abstracts)


# OTHER
# top10Authors = df['Author'].value_counts()[:10].to_dict()
