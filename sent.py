from flask import Flask,render_template
#init app by calling the constructor
app = Flask(__name__)
@app.route("/")
def home():
    # main program
    from bs4 import BeautifulSoup
    from urllib.request import Request,urlopen
    
    # ticker = input("Enter Ticker :")
    news_tables = {}
    
    finwiz1 = "https://finviz.com/quote.ashx?t="
    finwiz2 = "&p=d"
    
    # for ticker in tickers:
    url = finwiz1 + ticker + finwiz2
    req = Request(url=url, headers={"user-agent": "my-app"})
    response = urlopen(req)
    print("Response from HTML page: ",response)
    html = BeautifulSoup(response,features="html.parser")
    news_table = html.find(id="news-table")
    news_tables[ticker] = news_table
    
    ticker_data = news_tables[ticker]
    ticker_row = ticker_data.findAll("tr")
    
    for index,row in enumerate(ticker_row):
        title = row.a.text
        timestamp = row.td.text
    
    parsed_data = []
    
    for ticker, news_table in news_tables.items():
        for row in news_table.findAll("tr"):
            
            # extract title from anchor tag
            title = row.a.text
            # extracts dates from table cell data
            date_data = row.td.text
            #  strips the string of leading and trailing whitespaces
            date_data = date_data.strip()
            # splitting return the date_data into to parts date and        time.
            date_data = date_data.split(" ")
            
            if len(date_data)==1:
                time = date_data[0]
            else:
                date = date_data[0]
                time = date_data[1]
            parsed_data.append([ticker,date,time,title])
    
    import pandas as pd
    df = pd.DataFrame(parsed_data,columns=["Ticker","Date","Time","Title"])
    
    from nltk.sentiment.vader import SentimentIntensityAnalyzer 
    vader = SentimentIntensityAnalyzer()
    
    f = lambda title: vader.polarity_scores(title)['compound']
    df['compound'] = df['Title'].apply(f)
    
    df['Date'] = pd.to_datetime(df.Date,format="%b-%d-%y").dt.date
    
    import matplotlib.pyplot as plt
    
    mean_df = df.groupby(['Ticker','Date']).compound.mean()
    
    mean_df = mean_df.unstack()
    
    mean_df.plot(kind="bar")
    plt.show()
    
    return render_template("home.html")

@app.route("/result",methods=["GET","POST"])
def result():
    ticker = request.form['Stock Symbol']
if __name__ == "__main__":
    app.run(debug=True)





