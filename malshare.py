import urllib3
import time
import datetime

API_KEY = "5b2b7ebb48146bf73a55903b282bdb3ca2f0d69bf0f4b860e1c9caf78c9d0c53"

http = urllib3.PoolManager()

Main_url = "https://www.malshare.com/"

def get_24h_hash():
    List_hash_24h = "/api.php?api_key="+API_KEY+"&action=getlist"
    url = Main_url+List_hash_24h
    print(url)
    respons = http.request(method="GET",url = url, headers = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.135 Safari/537.36"})
    hash_md5 = []
    hash_sha1 = []
    hash_sha256 = []
    print(respons.data.decode('utf-8'))
    for sample in eval(respons.data.decode('utf-8')):
        print(sample)
        hash_md5.append(sample["md5"])
        hash_sha1.append(sample["sha1"])
        hash_sha256.append(sample["sha256"])
    return hash_md5, hash_sha1, hash_sha256

def download(hash_md5):
    for hash in hash_md5:
        url = Main_url + "/api.php?api_key="+API_KEY+"&action=getfile&hash="+str(hash)
        url_info = Main_url + "/api.php?api_key="+API_KEY+"&action=details&hash="+str(hash)
        print(url)
        print(url_info)
        info = http.request(method="GET", url=url_info, headers={
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.135 Safari/537.36"})
        print(info.data)
        print(type(info.data.decode('utf-8')))
        sample_type = eval(info.data.decode("utf-8"))["F_TYPE"]
        if sample_type == "PE32":
            respons = http.request(method="GET", url=url, headers={
                "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.135 Safari/537.36"})    
            with open(str(hash),"wb") as f :
                f.write(respons.data)

#https://malshare.com/daily/2019-11-22/malshare_fileList.2019-11-22.sha1.txt
#https://malshare.com/daily/2019-11-24/malshare_fileList.2019-11-24.sha1.txt
def get_fileList_sha1():
    fornt_name = "malshare_fileList."
    back_name = ".sha1"
    front_url = "https://malshare.com/daily/"
    mid_url = "/malshare_fileList."
    back_url = ".sha1.txt"
    for i in range(1,365):
        date = datetime.date.today() - datetime.timedelta(days = i)
        url = front_url+str(date) +mid_url+str(date) + back_url
        name = fornt_name+str(date)+back_name
        print(url)
        print(name)
        result = http.request(method="GET", url=url, headers={
                "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.135 Safari/537.36"})
        print(result.status)
        if result.status == 200:
            with open("./"+name,"wb") as f :
                f.write(result.data)

            
    



if __name__ == "__main__":
    # hash_md5, hash_sha1, hash_sha256 = get_24h_hash()
    # print(len(hash_md5))
    # download(hash_md5)
    get_fileList_sha1()

