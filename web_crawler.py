# -*- coding: utf-8 -*-
import bs4
import urllib.request
import urllib.parse
import os
import sys
import json
from typing import Tuple


def formating_URL(query: str) -> Tuple[str, str]:
    """与えられたクエリから検索用のURLを作成し，返す

    Args:
        query (str): クエリ

    Returns:
        Tuple[str, str]: 検索用URL, クエリ
    """
    query = query.split()
    query = '+'.join(query)

    url = "https://www.google.co.in/search?q="+urllib.parse.quote_plus(
            query, encoding='utf-8'
        )+"&source=lnms&tbm=isch"
    return (url, query)


def get_soup(url: str) -> bs4.BeautifulSoup:
    """BeautifulSoupを使ってリクエストを飛ばし，データを返す．

    Args:
        url (str): 検索URL

    Returns:
        bs4.BeautifulSoup: [description]
    """
    header = {
        'User-Agent': "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.134 Safari/537.36"
    }
    request = urllib.request.urlopen(
        urllib.request.Request(url, headers=header)
    )
    soup = bs4.BeautifulSoup(request, 'html.parser')
    return soup


def check_Dir(query: str):
    """検索用に新しくディレクトリを作成する．(もしすでに存在しているなら，そのまま)

    Args:
        query (str):クエリ
    Returns:
        [type]: ディレクトリパス
    """
    DIR = "Pictures"
    if not os.path.exists(DIR):
        os.mkdir(DIR)

    DIR = os.path.join(DIR, query.split()[0])
    if not os.path.exists(DIR):
        os.mkdir(DIR)
    return DIR


def crawring(query: str):
    """クローリングを実行する

    Args:
        query (str): クエリ
    """
    link_list = []
    url, query = formating_URL(query)
    print(url)
    soup = get_soup(url)
    DIR = check_Dir(query)
    label = str(len([i for i in os.listdir('./Pictures/')]) + 1)

    for a in soup.find_all("div", {"class": "rg_meta"}):
        link, Type = json.loads(a.text)["ou"], json.loads(a.text)["ity"]
        link_list.append((link, Type))

    print("Total Picture is", len(link_list))

    for _, (img, Type) in enumerate(link_list):
        try:
            img_data = urllib.request.urlopen(img).read()
            cntr = len([i for i in os.listdir(DIR) if label in i]) + 1
            if len(Type) == 0:
                f = open(os.path.join(DIR, label + "_" + str(cntr)+".jpg"), 'wb')
            else:
                f = open(os.path.join(DIR, label + "_" + str(cntr)+"."+Type), 'wb')

            f.write(img_data)
            f.close()

        except Exception as e:
            print("IMG loading failed : "+img)
            print(e)
    print("FINISH")


def print_usage():
    """
    実行時引数にエラーがあった場合呼ばれるメソッド
    """
    print("Usage: %s Query" % __file__)
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
