import requests
from colored import fg, attr
from tls_client import Session
from websocket  import WebSocket
from toml       import load
from os         import _exit, system
from datetime   import datetime
from time       import time, sleep
from colorama   import Fore
from random     import choice
from json       import dumps
from solver     import solver
from threading  import Thread, Lock, active_count
from base64     import b64encode


thread_lock = Lock()
xtrack = 'eyJvcyI6IldpbmRvd3MiLCJicm93c2VyIjoiQ2hyb21lIiwiZGV2aWNlIjoiIiwic3lzdGVtX2xvY2FsZSI6ImVuLVVTIiwiYnJvd3Nlcl91c2VyX2FnZW50IjoiTW96aWxsYS81LjAgKFdpbmRvd3MgTlQgMTAuMDsgV2luNjQ7IHg2NCkgQXBwbGVXZWJLaXQvNTM3LjM2IChLSFRNTCwgbGlrZSBHZWNrbykgQ2hyb21lLzExMi4wLjAuMCBTYWZhcmkvNTM3LjM2IiwiYnJvd3Nlcl92ZXJzaW9uIjoiMTEyLjAuMC4wIiwib3NfdmVyc2lvbiI6IjEwIiwicmVmZXJyZXIiOiIiLCJyZWZlcnJpbmdfZG9tYWluIjoiIiwicmVmZXJyZXJfY3VycmVudCI6IiIsInJlZmVycmluZ19kb21haW5fY3VycmVudCI6IiIsInJlbGVhc2VfY2hhbm5lbCI6InN0YWJsZSIsImNsaWVudF9idWlsZF9udW1iZXIiOjk5OTksImNsaWVudF9ldmVudF9zb3VyY2UiOm51bGx9'


class Console:
    @staticmethod
    def print(content: str):
        # config["data"]["debug"])
        if (("(!)" in content) or ("(-)" in content) or ("(~)" in content)) and (CONFIG_debug == False): return
        # thread_lock.acquire()
        print(
            f'{Fore.LIGHTBLACK_EX}{datetime.fromtimestamp(time()).strftime("%H:%M:%S")}{Fore.RESET} ' +
            content
            .replace("[", f"{Fore.LIGHTBLACK_EX}[{Fore.MAGENTA}")
            .replace("]", f"{Fore.LIGHTBLACK_EX}]{Fore.RESET}")
            .replace("|", f"{Fore.LIGHTBLACK_EX}|{Fore.LIGHTBLUE_EX}")
            .replace("->", f"{Fore.LIGHTBLACK_EX}->{Fore.LIGHTBLUE_EX}")

            # .replace("(", f"{Fore.LIGHTBLACK_EX}({Fore.RESET}").replace(")", f"{Fore.LIGHTBLACK_EX}){Fore.RESET}")
            .replace("(+)", f"{Fore.LIGHTBLACK_EX}({Fore.GREEN}+{Fore.LIGHTBLACK_EX}){Fore.LIGHTBLUE_EX}")
            .replace("($)", f"{Fore.LIGHTBLACK_EX}({Fore.GREEN}${Fore.LIGHTBLACK_EX}){Fore.LIGHTBLUE_EX}")
            .replace("(-)", f"{Fore.LIGHTBLACK_EX}({Fore.RED}-{Fore.LIGHTBLACK_EX}){Fore.LIGHTBLUE_EX}")
            .replace("(!)", f"{Fore.LIGHTBLACK_EX}({Fore.RED}!{Fore.LIGHTBLACK_EX}){Fore.LIGHTBLUE_EX}")
            .replace("(~)", f"{Fore.LIGHTBLACK_EX}({Fore.YELLOW}~{Fore.LIGHTBLACK_EX}){Fore.LIGHTBLUE_EX}")
            .replace("(#)", f"{Fore.LIGHTBLACK_EX}({Fore.BLUE}#{Fore.LIGHTBLACK_EX}){Fore.LIGHTBLUE_EX}")
            .replace("(*)", f"{Fore.LIGHTBLACK_EX}({Fore.CYAN}*{Fore.LIGHTBLACK_EX}){Fore.LIGHTBLUE_EX}")
        , end=f"{Fore.RESET}\n")
        # thread_lock.release()

class Profile:
    def __init__(self, session, token, headers, cookies):
        self.token = token
        headers['Referer'] = 'https://discord.com/channels/@me'
        self.headers = headers
        self.cookies = cookies
        self.ws = WebSocket()
        self.session = session


    def ConnectWS(self):
        self.ws.connect('wss://gateway.discord.gg/?encoding=json&v=9')
        self.ws.send(dumps({
            "op": 2,
            "d": {
                "token": self.token,
                "capabilities": 8189,
                "properties": {
                    "os": "Windows",
                    "browser": "Chrome",
                    "device": "",
                    "system_locale": "en-US",
                    "browser_user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36",
                    "browser_version": "112.0.0.0",
                    "os_version": "10",
                    "referrer": "",
                    "referring_domain": "",
                    "referrer_current": "",
                    "referring_domain_current": "",
                    "release_channel": "stable",
                    "client_build_number": 192149,
                    "client_event_source": None,
                    "design_id": 0
                },
                "presence": {
                    "status": "idle",
                    "since": 0,
                    "activities": [
                        {
                            "name": "Custom Status",
                            "type": 4,
                            "state": "vast#1337",
                            "emoji": None
                        }
                    ],
                    "afk": False
                },
                "compress": False,
                "client_state": {
                    "guild_versions": {},
                    "highest_last_message_id": "0",
                    "read_state_version": 0,
                    "user_guild_settings_version": -1,
                    "user_settings_version": -1,
                    "private_channels_version": "0",
                    "api_code_version": 0
                }
            }
        }))

    def JoinServer(self, invite):
        try:
            headers = self.headers
            try:
                res = self.session.get(
                    f"https://discord.com/api/v9/invites/{invite}?inputValue={invite}&with_counts=true&with_expiration=true", headers=headers).json()
                jsonContext = {
                    "location": "Join Guild",
                    "location_guild_id": str(res['guild']['id']),
                    "location_channel_id": str(res['channel']['id']),
                    "location_channel_type": int(res['channel']['type'])
                }
                json_str = dumps(jsonContext)
                xContext = b64encode(json_str.encode()).decode()
                headers["x-context-properties"] = xContext
            except: pass
            headers["content-length"] = "2"
            r = self.session.post(f'https://discord.com/api/v9/invites/{invite}', headers=headers, json={})
            if r.status_code == 200:
                Console.print(f"(+) Joined [{invite}] - [200]")
            elif r.status_code == 429:
                Console.print(f"(-) JoinRES : RATELIMIT BY CLOUDFLARE")
                return sleep(3)
            elif r.status_code == 403:
                return Console.print(f"(-) JoinRES : Token Locked. [{self.token[:25]}]")
            elif r.status_code == 400:
                return Console.print("(-) JoinRES : Captcha Gay ~ solver coming soon")
            else:
                return Console.print(f"(!) Error [{r.text}]")
        except Exception as e:
            Console.print(f"(!) Join Exception: {e}")
            return self.JoinServer(invite)
    
    def UpdateDOB(self):
        payload = {
            "date_of_birth": "2000-05-18"
        }
        dobres = self.session.patch('https://discord.com/api/v9/users/@me', headers=self.headers, cookies=self.cookies, json=payload)
        return dobres

    def AddBio(self, custom_bio: str = None):
        payload = {
            "bio": "discord.gg/vast" if custom_bio is None else custom_bio
        }
        headers = self.headers
        headers["content-length"] = str(len(dumps(payload)))
        biores = self.session.patch('https://discord.com/api/v9/users/@me/profile', headers=headers, json=payload)
        return biores
        
    def AddPFP(self):
        with open(f'./avatars/avatar_1.jpg', "rb") as image_file:
            encoded_string = b64encode(image_file.read())
            
        payload = {
            "avatar": f"data:image/png;base64,{(encoded_string.decode('utf-8'))}",
        }
        headers = self.headers
        headers["content-length"] = str(len(dumps(payload)))
        addpfp = self.session.patch('https://discord.com/api/v9/users/@me', headers=headers, json=payload)
        return addpfp
    
    def AddHypesquad(self):
        payload = {
            'house_id': choice(['1', '2', '3'])
        }
        headers = self.headers
        headers["content-length"] = str(len(dumps(payload)))
        hyperes = self.session.post("https://discord.com/api/v9/hypesquad/online", json=payload, headers=self.headers)
        return hyperes
        
    def EnableDevmode(self):
        payload = {
            "settings": "agIQAQ=="
        }
        devres = requests.patch('https://discord.com/api/v9/users/@me/settings-proto/1', headers=self.headers, cookies=self.cookies, json=payload)
        return devres


class Discord:
    def __init__(self) -> None:
        self.proxy = (choice(open("./proxies.txt", "r").readlines()).strip()
            if len(open("./proxies.txt", "r").readlines()) != 0
            else None)
        self.proxies = {
            "http": "http://" + self.proxy,
            "https": "http://" + self.proxy
        }
        self.session = Session(
            client_identifier="chrome_110",
            ja3_string="771,4865-4867-4866-49195-49199-52393-52392-49196-49200-49162-49161-49171-49172-156-157-47-53-255,0-11-10-35-23-13-43-45-51,29-23-24-25,0-1-2",
            h2_settings={"HEADER_TABLE_SIZE": 65536,"MAX_CONCURRENT_STREAMS": 1000,"INITIAL_WINDOW_SIZE": 6291456,"MAX_HEADER_LIST_SIZE": 262144},
            h2_settings_order=["HEADER_TABLE_SIZE","MAX_CONCURRENT_STREAMS","INITIAL_WINDOW_SIZE","MAX_HEADER_LIST_SIZE"],
            supported_signature_algorithms=["ECDSAWithP256AndSHA256","PSSWithSHA256","PKCS1WithSHA256","ECDSAWithP384AndSHA384","PSSWithSHA384","PKCS1WithSHA384","PSSWithSHA512","PKCS1WithSHA512",],
            supported_versions=["GREASE", "1.3", "1.2"],
            key_share_curves=["GREASE", "X25519"],
            cert_compression_algo="brotli",
            pseudo_header_order=[":method",":authority",":scheme",":path"],
            connection_flow=15663105,
            header_order=["accept","user-agent","accept-encoding","accept-language"]
        )
                
                
    @staticmethod
    def getCookies() -> list:
        headers = {
            'Accept': '*/*',
            'Accept-Language': 'en-US,en;q=0.9',
            'Connection': 'keep-alive',
            'Referer': 'https://discord.com/',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
            'Sec-GPC': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36',
            'X-Track': xtrack,
        }

        response = requests.get('https://discord.com/api/v9/experiments', headers=headers)
        return response.cookies, response.json().get("fingerprint")


    def register(self) -> bool:
        try:
            xcookies, fingerprint = self.getCookies()
            cookies = {
                '__dcfduid': xcookies.get('__dcfduid'),
                '__sdcfduid': xcookies.get('__sdcfduid'),
                '__cfruid': xcookies.get('__cfruid'),
                'locale': 'en-US',
            }
            
            xses = requests.Session()
            xses.proxies = self.proxies
            capKey = solver.solveCaptcha(xses)

            payload = {
                "consent": True,
                "fingerprint": fingerprint,
                "username": "vast best gen" if CONFIG_uname == "" else CONFIG_uname,
                "captcha_key": capKey
            }
            headers = {
                'Accept': '*/*',
                'Accept-Language': 'en-US,en;q=0.9',
                'Connection': 'keep-alive',
                'content-length': str(len(dumps(payload))),
                'Content-Type': 'application/json',
                'Origin': 'https://discord.com',
                'Referer': 'https://discord.com/',
                'Sec-Fetch-Dest': 'empty',
                'Sec-Fetch-Mode': 'cors',
                'Sec-Fetch-Site': 'same-origin',
                'Sec-GPC': '1',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36',
                'X-Fingerprint': fingerprint,
                'X-Track': xtrack,
            }

            response = self.session.post('https://discord.com/api/v9/auth/register', headers=headers, cookies=cookies, proxy=self.proxies, json=payload)
            if "token" not in response.text:
                Console.print(f"(-) Failed to gen: {response.text}")
                return False

            token = response.json().get('token')

            headers.pop('content-length')
            headers.pop('X-Fingerprint')
            headers['Authorization'] = token
            status = requests.get('https://discord.com/api/v10/users/@me/library', headers=headers)
            if status.status_code != 200:
                Console.print(f"(-) Locked Token: {token} [{status.status_code}]")
                return False

            Console.print(f"(+) {token}")

            profile = Profile(self.session, token, headers, cookies)
            profile.ConnectWS()
            profile.UpdateDOB()

            if CONFIG_addBio:
                biores = profile.AddBio()
                Console.print(f"(~) BioRES: {biores.status_code}")
            if CONFIG_addHype:
                hyperes = profile.AddHypesquad()
                Console.print(f"(~) HypeRES: {hyperes.status_code}")
            if CONFIG_enableDev:
                devres = profile.EnableDevmode()
                Console.print(f"(~) DevRES: {devres.status_code}")
            if CONFIG_addPFP:
                pfpres = profile.AddPFP()
                Console.print(f"(~) PfpRES: {pfpres.status_code}")
                        
            if CONFIG_joinGuild != "":
                profile.JoinServer(CONFIG_joinGuild)
                
            return True
        except Exception as e:
            print(e)


    
if __name__ == "__main__":
    config = load('config.toml')
    
    PROFILE          = config['profile']
    CONFIG_enableDev = PROFILE['enableDev']
    CONFIG_addHype   = PROFILE['addHype']
    CONFIG_addPFP    = PROFILE['addPFP']
    CONFIG_addBio    = PROFILE['addBio']
    
    DATA              = config['data']
    CONFIG_uname      = DATA['username']
    CONFIG_joinGuild  = DATA['joinGuild']
    CONFIG_threads    = DATA['threads']
    CONFIG_debug      = DATA['debug']

    system("cls||clear")

    a = fg("#babaf8")
    b = fg("#7c7cf8")
    c = fg("#3e3ef8")
    r = attr(0)

    print(f"""
        {a}┬  ┬  ┌─┐  ┌─┐  ┌┬┐
        {b}└┐┌┘  ├─┤  └─┐   │ 
        {c} └┘   ┴ ┴  └─┘   ┴ 
    """ + r)
    
    try:
        while True:
            while active_count() < CONFIG_threads:
                discord = Discord()
                Thread(target=discord.register).start()
            sleep(1)
    except KeyboardInterrupt:
        print("-> KeyboardInterrupt <-")
        _exit(0)
