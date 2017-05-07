# -*- coding: utf-8 -*-
import bs4
import urllib.request
import os
import sys
import json

def formating_URL(query):
    query= query.split()
    query='+'.join(query)
    url="https://www.google.co.in/search?q="+query+"&source=lnms&tbm=isch"
    return (url,query)

def get_soup(url):
    header={'User-Agent':"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.134 Safari/537.36"
    }

    request = urllib.request.urlopen(urllib.request.Request(url,headers=header))
    soup = bs4.BeautifulSoup(request,'html.parser')
    return soup

def check_Dir(query):
    DIR = "Pictures"
    if not os.path.exists(DIR):
        os.mkdir(DIR)

    DIR = os.path.join(DIR,query.split()[0])
    if not os.path.exists(DIR):
        os.mkdir(DIR)
    return DIR

def crawring(query):
    link_list = []
    label = "0"
    url,query = formating_URL(query)
    print(url)
    soup = get_soup(url)
    DIR = check_Dir(query)

    for a in soup.find_all("div",{"class":"rg_meta"}):
        link , Type =json.loads(a.text)["ou"]  ,json.loads(a.text)["ity"]
        link_list.append((link,Type))

    print("Total Picture is",len(link_list))

    for i , (img , Type) in enumerate( link_list):
        try:
            img_data = urllib.request.urlopen(img).read()
            cntr = len([i for i in os.listdir(DIR) if label in i]) + 1
            if len(Type)==0:
                f = open(os.path.join(DIR , label + "_"+ str(cntr)+".jpg"), 'wb')
            else :
                f = open(os.path.join(DIR , label + "_"+ str(cntr)+"."+Type), 'wb')

            f.write(img_data)
            f.close()

        except Exception as e:
            print("IMG loading failed : "+img)
            print(e)
    print("FINISH")

def print_usage():
    print("Usage: %s Query" %__file__)
    print("Queryに検索したいキーワードを入力してください")
    print("ちなみに日本語は不可．")

def main():
    if len(sys.argv) != 2:
        print_usage()
        sys.exit()

    query = sys.argv[1]
    crawring(query)


if __name__ == "__main__":
    main()
