import praw

reddit = praw.Reddit(
    client_id='vbxHSv02ElO_FPgVXcTkZA',
    client_secret='RnknXC3zZGZmoFb-8vPFFUmZm0l7xA',
    user_agent='script:crawler:v1.0 (by /u/Adam_Zhang_pku)',
    username='Adam_Zhang_pku',
    password='zyq990717@'
)

# Example: Access the top 10 hot posts from the Python subreddit
subreddit = reddit.subreddit('all')

keywords = ['$MSFT', '$GOOG', '$NVDA', '$META', '$TSLA', '$ADBE', '$IBM', '$PLTR', '$MBLY', '$DT', '$PATH', '$S', '$AUR', '$DARK.L', '$PRESIGHT.AE', '$AI', '$NWTN', '$UPST', '$ODD', '$BAYANAT.AE', '$RXRX', '$PRO', '$SOUN', '$EXAI', '$NNOX', '$CRNC', '$BBAI', '$STEM', '$LGCL', '$INOD', '$AISP', '$STIX', '$AIXI', '$APX.AX', '$AUID', '$BTH.AX', '$TSP', '$LTRN', '$KSCP', '$AIRE', '$DUOT', '$BFRG', '$PRST', '$SPPL', '$JTAI', '$FRGT']

# Define your search query
query = " OR ".join(keywords[:10])

# Fetch the search results
search_results = subreddit.search(query, limit=None)

print(search_results)

# Print the titles and URLs of the search results
for i,post in enumerate(search_results):
    continue
print(i)
