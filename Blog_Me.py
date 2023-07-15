#import library
import pandas as pd
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer


#reading excell/xlsx files
articles_df = pd.read_excel('articles.xlsx')

#summary of data
articles_df.describe()
articles_df.info()

#count the number of articles per source
articles_df.groupby(['source_id'])['article_id'].count()

#number of reaction by publisher
articles_df.groupby(['source_id'])['engagement_reaction_count'].sum()

#dropping a colum
articles_df = articles_df.drop('engagement_comment_plugin_count', axis=1)

# a function that search key word in the title
def keywordflag(keyword):
    length = len(articles_df)
    keyword_flag=[]
    for i in range(0,length):
        heading = articles_df['title'] [i]
        keyword = keyword.casefold()
        try:
            if keyword in heading:
                flag = 1
            else:
                flag = 0
        except:
            flag = 0
        keyword_flag.append(flag)
    return keyword_flag

flag= keywordflag('peace')

#creating a new colum
articles_df['Flag Keywords'] = pd.Series(flag)
 
# #SentimentIntensityAnalyzer
# sent_int =SentimentIntensityAnalyzer()

# text = articles_df['title'][3710]
# sent=sent_int.polarity_scores(text)

# neg = sent['neg']
# pos = sent['pos']
# neu = sent['neu']

#for for sentanalyse

pos_title = []
neg_title = []
neu_title = []

for x in range(0,len(articles_df)):
    try:
        text = articles_df['title'] [x]
        sent_int =SentimentIntensityAnalyzer()
        sent=sent_int.polarity_scores(text)
        neg = sent['neg']
        pos = sent['pos']
        neu = sent['neu']
    except:
        neg = 0
        pos = 0
        neu = 0
    pos_title.append(pos) 
    neg_title.append(neg)
    neu_title.append(neu)


title_pos = pd.Series(pos_title)
title_neg = pd.Series(neg_title)
title_neu = pd.Series(neu_title)

articles_df['Pos_title'] = title_pos
articles_df['Neg_title'] = title_neg
articles_df['Neu_title'] = title_neu

articles_df.to_excel('blogme_clean.xlsx', sheet_name ='blogmedata', index=False)