import aiohttp
import asyncio
import time
import requests
def find_slat(url):
    cnt=0
    n=len(url)
    for i in range(n):
        if url[i]=='/':
            cnt+=1
            if cnt==3:
                return i
    return n
class MakeRequest:
    response_count=0
    lock=asyncio.Lock()
    numrequest=0
    percent=[]
    start_time=0
    success_request=0
    timetaken=[]
    idx=0
    total_size=0
    url=""
    data=[]
    
    async def fetch(self,session,url):
        data={
            'username':'haduchau456',
            'password':'1234567'
        }
        try:
            
            async with session.post(url,data=data) as response:
                async with self.lock:
                    self.response_count+=1
                    # idx=binary_search_recursive(percent,response_count,0,9)
                    self.success_request+=1
                    if self.percent[self.idx]==self.response_count:
                        # print("start time=",start_time)
                        self.timetaken.append(time.time()-self.start_time)
                        self.idx+=1
                        # print(f"Đã nhận được {response_count} phản hồi({(idx+1)*10}%) trong {time.time()-start_time:.2f} s ")
                self.total_size+=len( await response.text())
        except Exception as e:

            print(f"Request failed: {e}")
    async def load_test(self,url,num_requests):
        async with aiohttp.ClientSession() as session:
            
            tasks=[self.fetch(session,url) for _ in range(num_requests) ]
            results=await asyncio.gather(*tasks,return_exceptions=True)
    def run(self,url,numrequest,data=[]):
        self.url=url
        self.numrequest=numrequest
        self.data=data
        pos=find_slat(self.url)
        print(f"Server Hostname: {self.url[:pos]}")
        print(f"Server Port: 80")
        document_path='/'
        if pos<len(self.url):
            document_path=self.url[pos:]
        print(f"Document Path: {document_path}")
        for i in range (1,11):
            self.percent.append(round(self.numrequest*i/10))
        # asyncio.run(fetch_info(url))
        # global start_time
        self.start_time=time.time()
        asyncio.run(self.load_test(self.url,self.numrequest))
        end_time=time.time()
        total_time=end_time-self.start_time
        # print(f"Sent {num_request} request in {total_time:.2f} seconds")
        print(f"Time taken for tests: {total_time:.2f} seconds")
        print(f"Complete requests: {self.success_request}")
        print(f"Failed requests: {self.numrequest-self.success_request}")
        print(f"Requests per second: {self.numrequest/total_time:.2f}")
        print(f"Time per request: {total_time/self.numrequest:.4f} s")
        print(f"Total tranfer: {self.total_size/total_time/1024} KB/s")
        print("Percentage of the requests served within a certain time (ms)")
        for i in range(10):
            print(f"{(i+1)*10}%\t{self.timetaken[i]}")


def main():
    url=input("Your URL:")
    
    num_request=int(input("Number request: "))
    a=MakeRequest()
    a.run(url,num_request)
    

if __name__=="__main__":
    main()