from flask import Flask, render_template, request
import random
import requests
from bs4 import BeautifulSoup
import pandas as pd
from IPython.display import HTML

app = Flask(__name__)

@app.route('/')
def home():
    random_number=random.randint(1,10)
    return render_template("index.html", random_number=random_number)
@app.route('/DisplayTable', methods=["POST","GET"])
def table():
    if request.method=='POST':
        ticker = request.form["stock"]
        print(ticker)
        table=getstock(ticker)
        if table.empty:
            result="<h1>Invalid stock name<h1>"
        else:
            result=table.to_html()
        return render_template('/DisplayTable.html', result=result)#pass in the function to display the table according the the input
    else:
        return render_template('/index.html')

def getstock(ticker):
    # tickers = ["AAPL", "MSFT"]  # list of tickers whose financial data needs to be extracted
    financial_dir = {}

    #for ticker in tickers:
        # getting balance sheet data from yahoo finance for the given ticker
    temp_dir = {}
    url = 'https://finance.yahoo.com/quote/' + ticker + '/balance-sheet?p=' + ticker
    headers = {'User-Agent': "Mozilla/5.0"}
    page = requests.get(url, headers=headers)
    if page.ok:  # Checking if the connection is successful
        print("all good")
    else:
        random_array=[]
        combined_financials = pd.DataFrame(random_array)
        return combined_financials
    page_content = page.content
    soup = BeautifulSoup(page_content, 'html.parser')
    tabl = soup.find_all("div", {"data-test": "fin-row"})
    for t in tabl:
        rows = t.find_all("div", {"class": "D(tbr) fi-row Bgc($hoverBgColor):h"})
        for row in rows:
            temp_dir[row.get_text(separator='|').split("|")[0]] = row.get_text(separator='|').split("|")[1]

    financial_dir[ticker] = temp_dir

    # storing information in pandas dataframe
    combined_financials = pd.DataFrame(financial_dir)

    return combined_financials

if __name__ == "__main__":
    app.run(debug=True)
