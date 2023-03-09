import requests

def getcat(coun):
    if len(coun) != 0:
        try:
            r = requests.get('https://thecatapi.com/api/images/get?format=src')
            url = r.url
        except:
            url = getcat(coun)
    else:
        url = open("D:\PROJECTS\\tgbot\cat1.png", 'rb')
        coun.append(1)
    return url
