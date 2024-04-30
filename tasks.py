from sec_edgar_downloader import Downloader
import google.generativeai as genai
import os
import re
import chardet
import matplotlib.pyplot as plt

def getFilings(ticker):
    dl = Downloader("MyCompanyName", "my.email@domain.com", "./")
    dl.get("10-K", ticker, after="1995-01-01", before="2023-12-31")
    directory = './sec-edgar-filings/{ticker}/10-K'.format(ticker = ticker)
    return directory

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
model = genai.GenerativeModel('gemini-1.5-pro-latest')

def cleanData():
    for root, dirs, files in os.walk(getFilings("AAPL")):
        encoding = ""
        for filename in files:
            outputLines = []
            with open(os.path.join(root, filename), 'rb') as findEncoding:
                data = findEncoding.read()
                encoding = chardet.detect(data).get("encoding")
            with open(os.path.join(root, filename), encoding=encoding) as f:
                lines = f.readlines()
                for i in range(len(lines)):
                    lines[i] = lines[i].replace('&amp;', '&')
                    lines[i] = lines[i].replace('&lt;', '<')
                    lines[i] = lines[i].replace('&gt;', '>')
                    lines[i] = lines[i].replace("#160;", ' ')
                    lines[i] = lines[i].replace("&nbsp;", '')
                    cleaner = re.compile('<.*?>')
                    lines[i] = re.sub(cleaner, '', lines[i])
                    if len(lines[i].strip()) != 0:
                        outputLines.append(lines[i])
                for i in range(len(outputLines)):
                    if "Net income".lower() in outputLines[i].lower():
                        if not os.path.isfile("output.txt"):
                            with open("output.txt", 'w') as f:
                                for j in range(i - 40, i + 5, 1):
                                    f.write(outputLines[j])
                        else:
                            with open("output.txt", 'a') as f:
                                for j in range(i - 40, i + 5, 1):
                                    f.write(outputLines[j]) 
                        break

def visualization():
    cleanData()
    with open("output.txt") as f:
            input = f.read()
            example = "Here is how you should return you answer: 1995: -1000, 1996: 1000, 1997: 500, and so on.\n"
            response = model.generate_content("Find the net income for each year from 1995-2023 and format your answer like a Python dictionary where the keys are the years and the values are the incomes. Keep your answer with units of millions.\n" + example + input, request_options={"timeout":600})

            parsedOutput = ""
            map = {}
            for i in range(len(response.text)):
                    if response.text[i].isdigit() or response.text[i] == "," or response.text[i] == ":" or response.text[i] == "-":
                            parsedOutput += response.text[i]

            parsedOutput = parsedOutput.split(",")
            for pair in parsedOutput:
                    pair = pair.split(":")
                    map[int(pair[0])] = int(pair[1])

            years = list(map.keys())
            incomes = list(map.values())

            fig = plt.figure(figsize=(10, 5))

            plt.bar(years, incomes, width=0.4)

            plt.xlabel("Years (1995 - 2023)")
            plt.ylabel("Net income (in millions)")
            plt.title("Net income from 1995 - 2023")
            plt.show()

def main():
     visualization()

if(__name__ == "__main__"):
     main()

        
