from bs4 import BeautifulSoup
from requests import get
from typing import Optional
from fastapi import FastAPI, Request
from time import time
import uvicorn


class RankScrapper:
    def __init__(self, user_url) -> None:
        self.baseUrl:str = "https://www.alexa.com/siteinfo/"
        self.url:str = self.baseUrl + user_url
    async def get_rank(self) -> int:
        self.timeStart:float = time()
        self.htmlData:str = get(url=self.url).text
        self.soup:BeautifulSoup = BeautifulSoup(self.htmlData, features="lxml")
        self.rankData:str = self.soup.find("div", {"class": "rankmini-rank"})
        self.timeEnd:float = time()
        self.totalTimeTaken:float = float("%0.2f"%(self.timeEnd - self.timeStart))
        try: return (int(self.rankData.text.strip()[1:]), self.totalTimeTaken)
        except: return (None, None)

class RestAPI():
    def __init__(self) -> None:
        self.app:FastAPI = FastAPI()
        @self.app.get('/')
        def index(request:Request):
            return {'status':'online', 'host':request.headers.get('host')}
        @self.app.get("/getrank")
        async def get_renk(url: Optional[str] = None):
            self.user_url = url
            self.rs = RankScrapper(self.user_url)
            self.rank, self.timeTaken = await self.rs.get_rank()
            if self.rank: return {'domain_name':self.user_url, 'alexa_rank': self.rank, 'time_taken(s)': self.timeTaken} 
            else: return{'message': "Invalid domain name given", 'domain':self.user_url}



ra:RestAPI = RestAPI()
app:FastAPI = ra.app

if __name__ == '__main__':
    uvicorn.run('main:app', host='0.0.0.0',port=5099,log_level='info')