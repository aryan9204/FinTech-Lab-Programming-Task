from sec_edgar_downloader import Downloader
import google.generativeai as genai
import os
import re
from bs4 import BeautifulSoup
import openai
import chardet
import time
import matplotlib.pyplot as plt
"""
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

model = genai.GenerativeModel('gemini-1.5-pro-latest')
#response = model.generate_content("What is the meaning of life?")
#print(response.text)
"""
def getFilings(ticker):
    dl = Downloader("MyCompanyName", "my.email@domain.com", "./")
    dl.get("10-K", ticker, after="1995-01-01", before="2023-12-31")
    directory = './sec-edgar-filings/{ticker}/10-K'.format(ticker = ticker)
    return directory
"""
path = "./sec-edgar-filings/AAPL/10-K/0000320193-18-000145/full-submission.txt"
processed_chunks = []

with open(path, 'r') as file:
    while True:
        chunk = file.read(1024)
        if not chunk:
            break  # Exit loop if end of file is reached
            # Process the chunk (e.g., perform text analysis)
        processed_chunks.append(chunk)
prompt_parts = [
  processed_chunks[:10],
  "\ncan you read through this and find the earnings per share?",
]

prompt = "Summarize this document for me"
input = 
response = model.generate_content([prompt, sample_file])
print(response.text)

with open("output.txt") as f:
    input = f.readlines()
    response = model.generate_content("Tell me some insights based on the following information\n" + input)
    print(response.text)

#getFilings("AAPL")
"""
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
model = genai.GenerativeModel('gemini-1.5-pro-latest')
"""
with open("./sec-edgar-filings/AAPL/10-K/0000320193-17-000070/full-submission.txt") as f:
   lines = f.readlines()
   input = '\n'.join(lines[:100])
   response = model.generate_content("Find the earnings per share and give me the answer in just one line\n" + input)
   print(response.text)

with open(path, 'r') as file:
   lines = file.read()
   response = model.generate_content("Find the earnings per share and give me the answer in just one line\n" + lines)
   print(response.text)
"""

def cleanData():
    for root, dirs, files in os.walk(getFilings("AAPL")):
        encoding = ""
        for filename in files:
            outputLines = []
            with open(os.path.join(root, filename), 'rb') as findEncoding:
                data = findEncoding.read()
                encoding = chardet.detect(data).get("encoding")
            with open(os.path.join(root, filename), encoding=encoding) as f:
                print(os.path.join(root, filename))
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
            print(response.text + "\n==========================")
            parsedOutput = ""
            map = {}
            firstChar = response.text.find('`')
            for i in range(firstChar, len(response.text)):
                    if response.text[i].isdigit() or response.text[i] == "," or response.text[i] == ":" or response.text[i] == "-":
                            parsedOutput += response.text[i]

            parsedOutput = parsedOutput.split(",")
            for pair in parsedOutput:
                    print(pair)
                    pair = pair.split(":")
                    print(pair[0])
                    print(pair[1])
                    map[int(pair[0])] = int(pair[1])
            for key, value in map.items():
                    print(key)
                    print(value)

            years = list(map.keys())
            incomes = list(map.values())

            fig = plt.figure(figsize=(10, 5))

            plt.bar(years, incomes, width=0.4)

            plt.xlabel("Years (1995 - 2023)")
            plt.ylabel("Net income (in millions)")
            plt.title("Net income from 1995 - 2023")
            plt.show()
                
                        
    """                
    with open("output.txt", 'w') as f:
        for entry in outputLines:
            f.write(entry)
    time.sleep(5)
    with open("output.txt") as f:
        input = f.read()
        response = model.generate_content("Find the net income for each year and give me the answer as pairs with the following format: (year: net income)\n" + input)
        print(response.text)

    for j in range(i + 1, i + 6):
        outputLines.append(lines[j])
    """

                    
"""
outputLines = []
with open(directory, 'rb') as findEncoding:
            data = findEncoding.read()
            encoding = chardet.detect(data).get("encoding")
            with open(directory, encoding=encoding) as f:
                lines = f.readlines()
                for i in range(len(lines)):
                    if "net income".lower() in lines[i].lower():
                        lines[i] = lines[i].replace('&amp;', '&')
                        lines[i] = lines[i].replace('&lt;', '<')
                        lines[i] = lines[i].replace('&gt;', '>')
                        lines[i] = lines[i].replace("#160;", ' ')
                        cleaner = re.compile('<.*?>')
                        lines[i] = re.sub(cleaner, '', lines[i])
                        outputLines.append(lines[i])
                        for j in range(i + 1, i + 10):
                            lines[j] = lines[j].replace('&amp;', '&')
                            lines[j] = lines[j].replace('&lt;', '<')
                            lines[j] = lines[j].replace('&gt;', '>')
                            cleaner = re.compile('<.*?>')
                            lines[j] = re.sub(cleaner, '', lines[j])
                            outputLines.append(lines[j])
"""
"""
encoding = ""
outputLines = []
with open(directory, 'rb') as findEncoding:
            data = findEncoding.read()
            encoding = chardet.detect(data).get("encoding")
            with open(directory, encoding=encoding) as f:
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
with open('output.txt', 'w') as f:
       for entry in outputLines:
              f.write(entry)
"""
                    
"""
with open("output.txt") as f:
    input = f.read()
    response = model.generate_content("Find the net income for each year and give me the answer in one line\n" + input)
    print(response.text)
"""

def main():
     visualization()

if(__name__ == "__main__"):
     main()

        
