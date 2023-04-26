# source of this on https://github.com/deepakkumar132/Discord-Token-Generator/blob/main/src/solver.py

import toml, requests, time

config = toml.load('config.toml')
captchaService = config.get("captcha").get("service")
key = config.get("captcha").get("capKey")

class solver():
    def solveCaptcha(session: requests.Session) -> str:
        publicKey = "4c672d35-0701-42b2-88c3-78380b0db560"
        siteUrl = "https://discord.com"

        if captchaService == "DORT":
            return solver.solveDortCaptcha(publicKey, siteUrl, session=session)
        elif captchaService == "CAPSOLVER":
            return solver.solveGeneric(publicKey, siteUrl, domain="https://api.capsolver.com", session=session)
        elif captchaService == "ANTI[CAPTCHA]":
            return solver.solveGeneric(publicKey, siteUrl, domain="https://api.anti-captcha.com", session=session)
        elif captchaService == "CAPMONSTER":
            return solver.solveGeneric(publicKey, siteUrl, domain="https://api.capmonster.cloud", session=session)

    
    def solveGeneric(publicKey: str, siteUrl: str, session: requests.Session, domain: str = "https://api.capsolver.com") -> str:
        taskType = "HCaptchaTurboTaskProxyless" if "capsolver" in domain else "HCaptchaTurboTask"
        data1 = {
            "clientKey": key,
            "appId": "5C4B67D5-D8E9-485D-AF57-4F427464F0CF",
            "task": {
                "type": taskType,
                "websiteURL": siteUrl,
                "websiteKey": publicKey,
                # "proxyType": "http",
                #"proxyAddress":"8.8.8.8",
                #"proxyPort":8080,
                "userAgent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36',
                #"enableIPV6": True,
                # "proxy": solver.getProxyFromSession(session)
            }
        }
        resp1 = requests.post(f"{domain}/createTask", json=data1)
        if resp1.json().get("errorId") == 0:
            taskId = resp1.json().get("taskId")
            data = {
                "clientKey": key,
                "taskId": taskId
            }
            resp = requests.post(f"{domain}/getTaskResult", json=data)
            status = resp.json().get("status")

            while status == "processing":
                time.sleep(1)
                resp = requests.post(f"{domain}/getTaskResult", json=data)
                status = resp.json().get("status")

            if status == "ready":
                captchaToken = resp.json().get("solution").get("gRecaptchaResponse")
                return resp.json().get("solution").get("gRecaptchaResponse")
            else:
                return solver.solveCaptcha(session=session)
        else:
            return solver.solveGeneric(publicKey, siteUrl, session, domain)
    
    def getProxyFromSession(session: requests.Session) -> str:
        protocol, sessionProxy = session.proxies.get("http").split("://")
        sessionProxy = sessionProxy.replace(":", "big juicy fat cock").replace("@", "big juicy fat cock")
        if len(sessionProxy.split("big juicy fat cock")) == 4:
            user, password, host, port = sessionProxy.split("big juicy fat cock")
            return f"{protocol}:{host}:{port}:{user}:{password}"
        else:
            host, port = sessionProxy.split("big juicy fat cock")
            return f"{protocol}:{host}:{port}"
