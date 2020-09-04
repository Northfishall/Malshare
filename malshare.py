import urllib3
import time
import datetime
import os 
import random 
import re

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
        try:
            info_data = eval(info.data.decode("utf-8"))
            print(type(info_data))
            print(info_data)
        except Exception as e:
            return "fail"
        sample_type = info_data["F_TYPE"]
        if sample_type == "PE32" or sample_type == "PE32+":
            respons = http.request(method="GET", url=url, headers={
                "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.135 Safari/537.36"})    
            with open("../malware_sample/sha1/"+str(hash),"wb") as f :
                f.write(respons.data)
            return "success"
        else:
            return "fail"

#https://malshare.com/daily/2019-11-22/malshare_fileList.2019-11-22.sha1.txt
#https://malshare.com/daily/2019-11-24/malshare_fileList.2019-11-24.sha1.txt
def get_fileList_sha1():
    fornt_name = "./fileList/malshare_fileList."
    back_name = ".sha1.txt"
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
            print("success download")
            with open(name,"wb") as f :
                f.write(result.data)
        else:
            print("error")
        time.sleep(5)

def download_all():
    files = os.walk("./fileList/")
    error_list = []
    for path, dir_list , file_list in files :
        for file_name in file_list:
            path_txt = os.path.join(path,file_name)
            f = open(path_txt)
            print("open txt"+ str(path_txt) +" success!")
            line = f.readline()
            while line:
                line = str(line).strip('\n')
                print("sha1"+ str(line))
                md5 = get_md5_by_sha1(str(line))
                if md5 != "error":
                    list_for_download = []
                    list_for_download.append(md5)
                    download(list_for_download)
                else:
                    error_list.append(line)
                    print("error sha1 list:" + str(error_list))
                line = f.readline()
                time.sleep(random.randint(3,8))
            f.close()
            time.sleep(random.randint(53,95))

    
def get_md5_by_sha1(sha1):
    front_url = "https://malshare.com/search.php?query="
    url = front_url + str(sha1)
    web = http.request(method="GET", url=url, headers={
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.135 Safari/537.36"})
    re_md5 = r'<td class="hash_font"><a href="sample.php\?action=detail&hash=(.+?)">'
    result = re.findall(re_md5,web.data.decode('utf-8'),re.S)
    if len(result)>0:
        return result[0]
    else:
        return "error"



if __name__ == "__main__":
    # hash_md5, hash_sha1, hash_sha256 = get_24h_hash()
    # print(len(hash_md5))
    # download(["7487eeb2fe088fcff1bca7c934b06148"])
    # get_fileList_sha1()
    download_all()
    #get_md5_by_sha1("7f1f19e1fcc4c3c9bfa329a8260a65562d9c8d6a")

