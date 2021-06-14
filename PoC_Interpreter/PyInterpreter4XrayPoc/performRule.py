import requests

def checkExpressions(request,rule):
    return True


def actRule(rule,ip):
    url=ip+rule['path']
    header=dict()
    resps=[]
    if 'headers' in rule:
        for k,v in rule['headers'].items():
            header[k]=v
            if "GET" in rule['method']:
                resps.append( requests.get(url,headers=header) )
                print(resps)
            elif "POST" in rule['method']:
                resps.append( requests.post(url, data=rule['body']) )    
                print(resps)
    return resps