import os
import sys
import json

if len(sys.argv) < 2:
    print("needs filename")
    exit()

scriptDir = os.path.realpath(os.path.dirname(__file__))
fileName = sys.argv[1]
csvFileName = fileName.replace(".json",".csv")
jsonf = open(os.path.join(scriptDir,fileName), "r")
csvf = open(os.path.join(scriptDir,csvFileName), "a")
jobj = json.loads(jsonf.read())

print("code,assembly", file=csvf)
for item in jobj:
    print(f'"{item["code"]}","{os.linesep.join(item["assembly"])}"', file=csvf)

csvf.close()
jsonf.close()