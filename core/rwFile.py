import json

def get_setting(Data=None):
    if Data == None:
        with open("setting.json", "r", encoding="utf8") as jsettings:
            return json.load(jsettings)
    else:
        with open("setting.json", "r", encoding="utf8") as jsettings:
            return json.load(jsettings)[Data]


def rFile(File):
    with open(f"{File}.json", "r", encoding="utf8") as jFile:
        return json.load(jFile)


def wFile(data, File):
    with open(f"{File}.json", "w", encoding="utf8") as jFile:
        json.dump(data, jFile, indent=4)
