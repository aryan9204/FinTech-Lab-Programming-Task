#Imports
from sec_edgar_downloader import Downloader
import google.generativeai as genai
import os
import re
import chardet
import matplotlib.pyplot as plt
import streamlit as st

#using edgar-sec-downloader library to get the 10K filings for a company of the user's choice
def getFilings():
    dl = Downloader("MyCompanyName", "my.email@domain.com", "./")
    dl.get("10-K", ticker, after="1995-01-01", before="2023-12-31")
    directory = './sec-edgar-filings/{ticker}/10-K'.format(ticker = ticker)
    return directory

#Google Gemini API for the LLM model
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
model = genai.GenerativeModel('gemini-1.5-pro-latest')

#cleaning data of all HTML tags and unnecessary information to make it easy for the LLM
def cleanData():
    #iterate through the directory with the 10K filings in it
    for root, dirs, files in os.walk(getFilings()):
        encoding = ""
        for filename in files:
            outputLines = []
            #check encoding because most 10K filings are ASCII encoded but one of them was UTF-8 encoded
            with open(os.path.join(root, filename), 'rb') as findEncoding:
                data = findEncoding.read()
                encoding = chardet.detect(data).get("encoding")
            with open(os.path.join(root, filename), encoding=encoding) as f:
                print(os.path.join(root, filename))
                lines = f.readlines()
                for i in range(len(lines)):
                    #clean data to remove HTML tags and replace character codes with their actual values
                    lines[i] = lines[i].replace('&amp;', '&')
                    lines[i] = lines[i].replace('&lt;', '<')
                    lines[i] = lines[i].replace('&gt;', '>')
                    lines[i] = lines[i].replace("#160;", ' ')
                    lines[i] = lines[i].replace("&nbsp;", '')
                    cleaner = re.compile('<.*?>')
                    lines[i] = re.sub(cleaner, '', lines[i])
                    if len(lines[i].strip()) != 0:
                        outputLines.append(lines[i])
                #search for lines with net income in them because that is the insight I chose to look at
                #output.txt is a file that contains the merged and cleaned data, so I only have to make one call to the API
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

#run model and create visualization
def visualization():
    cleanData()
    with open("output.txt") as f:
        #give prompt to model
        input = f.read()
        example = "Here is how you should return you answer: 1995: -1000, 1996: 1000, 1997: 500, and so on.\n"
        #try-except block so that if the model fails to return a response, it tries again
        while True:
            try:
                response = model.generate_content("Find the net income for each year from 1995-2023 and format your answer like a Python dictionary where the keys are the years and the values are the incomes. Keep your answer with units of millions.\n" + example + input, request_options={"timeout":600})
                print(response.text)
                
                #formatting model's response into a key-value system that I can turn into a hashmap
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

                #use matplotlib to create visualization and streamlit library to output it to the browser
                fig, ax = plt.subplots()

                ax.bar(years, incomes, width=0.4)

                plt.xlabel("Years (1995 - 2023)", axes=ax)
                plt.ylabel("Net income (in millions)", axes=ax)
                plt.title("Net income from 1995 - 2023")
                st.pyplot(fig)
                break
            #except block to make the model rerun if it fails
            except:
                 print(response.text)

    #delete the cleaned and merged file, so that the user can rerun the program by entering in another ticker
    os.remove("output.txt")
        

#streamlit code to create GUI
st.title("Trends in net incomes per year from 1995 - 2023")
st.write("Seeing trends in net income is important because it indicates if a company is doing well or poorly, which projects the direction of their stock. If a company has seen upward trajectories in their net income, then their stock will likely rise over the next few years. Conversely, if net incomes have been stagnant or on a downward trajectory, then the company's stock will likely fall in the next few years.")
st.write("Please enter in the ticker of the company to see a graph of their net incomes from 1995 - 2023!")
ticker = st.text_input("Enter in a ticker")
submitBtn = st.button("Submit")
if submitBtn and ticker:
     visualization()


        
