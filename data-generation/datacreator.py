import os
import sys
import requests
import re
import datetime
import json

# Regex for condensing whitespace to a single space character
collapseWhitespaceRegex = re.compile(r'\s+')
scriptDir = os.path.realpath(os.path.dirname(__file__))
fileName = f"data_{datetime.datetime.now().strftime('%Y-%m-%d_%I-%M-%S_%p')}.json"
print(f"Writing data to {fileName}")
f = open(os.path.join(scriptDir,fileName), "a")


operators = ["+", "-", "*", "/", "%"]
parametersA = [*range(73,100)] + ["a", "b"]
parametersB = [*range(1,100)] + ["a", "b"]

print(f"Running {len(operators) * len(parametersA) * len(parametersB)} compilations...")

def main():
    first = False
    printAndRecordLine("[")
    for a in parametersA:
        for b in parametersB:
            for operator in operators:
                code = f"int func(int a, int b) {{ return {a} {operator} {b};}}"
                result = getCompilationLinesForCode(code)
                printAndRecordLine(("," if first else "") + json.dumps({"code" : code, "assembly" : result}))
                first = True
    printAndRecordLine("]")
    return 0

def getCompilationLinesForCode(code):
    response = requests.post("https://godbolt.org/api/compiler/g132/compile",json={
        "source": code,
        "options": {},
        "lang": "c++",
        "allowStoreCodeDebug": True
    })
    if (response.status_code == 200):
        lines = response.text.splitlines()[1:]
        processedLines = [collapseWhitespaceRegex.sub(" ",line.strip()) for line in lines]
        return processedLines
    else:
        return ["!!!" + response.text]
    
def printAndRecordLines(message):
    for line in message:
        printAndRecordLine(line)

def printAndRecordLine(message):
    print(message)
    f.write(message + "\n")

if __name__ == "__main__":
    sys.exit(main())

f.close()