import requests
from bs4 import BeautifulSoup as bs
import csv
import re
import time
from math import inf

def parse_main(url:str, parent_tag:str, parent_class:str, level:tuple, link_split="/", trailing_zero="", url_ext="",incl_prepend ="", incl_post="", exc_tld=False, exc_additional="", numerical=False)->list:

    '''
    Get links from main page.
    '''

    urls = []
    response = requests.get(url)
    html = response.text
    res = bs(html, "html.parser")

    root = url

    if exc_tld:
        root_lst = url.split(".")
        root = ".".join(root_lst[:-1])

    if exc_additional != "":
        root = root[:-len(exc_additional)]
    if parent_class == "":
        tags = res.find_all(parent_tag)
    else:
        tags = res.find_all(parent_tag, {parent_class})
    
    for x in tags:
        links = x.find_all("a", href=True)

        if numerical:

            if len(links) > 0:
                last_ind = -1
                last = [links[last_ind].get('href')]

 
                while has_tld(url_ext, last[0]) == False:
                    try:
                        last_ind -= -1
                        last = [links[last_ind].get('href')]
                    except:
                        break
    

                if abs(last_ind) == len(links) and not has_tld(url_ext, last[0]):
                    continue

                i = 0
                while i < len(link_split):
                    last = decompose_link(last, link_split[i])
                    i+=1

                if len(last) == 0:
                    continue

                total = last[level[0]:level[1]][0]
 
                if not total.isnumeric():
                    continue

                urls.extend(root + trailing_zero + incl_prepend + str(x) + incl_post + url_ext for x in range(1, int(total)+1) if x<10)
                urls.extend(root + incl_prepend + str(x) + incl_post + url_ext for x in range(1, int(total)+1) if x>10)


            else:
                urls.append(url)

        else:
            for link in links:
                urls.append(link.get('href'))

    urls = sorted(list(set(urls)))

    return urls

def parse_pages(url:str, directory:str, filename:str, parent_tag:str, parent_class:str, content_ind = None,extension=".csv", headers=[], exclude=[]):

    links_file = filename + "_links.txt" 
    with open(links_file, 'a', encoding='UTF8') as file:            
        file.write(url + "\n")

    response = requests.get(url)
    html = response.text
    res = bs(html, "html.parser")
    out_file = directory + '/' + filename +  extension

    if parent_class != "":
        tags = res.find_all(parent_tag, {parent_class})
    else:
        tags = res.find_all(parent_tag)

    if tags == "":
        return ""

    contents = ""

    i = 0
    for x in tags:
        i += 1
        if content_ind is not None:
            if (len(x) - 1) >= content_ind:
                contents = x.contents[content_ind]
            elif content_ind == inf and len(x.contents) > 0:
                try:
                    contents = "".join(list(x.contents[0]))
                except:
                    return ""
            else:
                return ""
        else:
            contents = x.contents
        contents = clean_content(contents, exclude)
        with open(out_file, 'a', encoding='UTF8') as file:            
            file.write(contents)

    return contents

def has_tld(tld, link):
    if link.endswith(tld):
        return True
    elif tld in link:
        return True
    return False

def decompose_link(link_strs:list, split_string:str):
    if not link_strs == []:
        for link_str in link_strs:
            if split_string in link_str:
                link_list = link_str.split(split_string)
                return link_list

    return []

def clean_content(text, tags):

    str(text).replace("<p>", "")
    str(text).replace("</p>", "")
    str(text).replace("</br>", "")
    str(text).strip()

    for tag in tags:
        tag_string = "<[" + tag + "][^>]*>(.+?)</[" + tag + "]>"
        str_mod = re.sub(tag_string, "", str(text))

    str_mod = re.sub(">(.+?)<", '', str_mod)
    str_mod = re.sub("<(.+?)>", '',str_mod)
    str_mod = re.sub("\n", " ", str_mod)
    str_mod = re.sub("\r", '',str_mod)
    str_mod = re.sub(" +", " ", str_mod)
    str_mod = re.sub('\.+', ".", str_mod)

    return str_mod

def main():

    print("===PARSING DATA===")
    start = time.time()
    print("Parsing Bible website links ... ")

    bible_url = "https://www.wordproject.org/bibles/sw/index.htm"
    bible_urls = []

    det = {
        "url":bible_url,
        "parent_tag":"ul",
        "parent_class":"nav nav-tabs nav-stacked",
        "level":(0,1),
        "link_split":["/"],
        "trailing_zero":"0",
        "url_ext":".htm",
        "incl_post":"/1",
        "exc_tld":True,
        "exc_additional" : "index",
        "numerical" : True
    }

    bible_main_pages = parse_main(**det)
    total_subp = len(bible_main_pages)

    print("Total subpage links: ", total_subp)
    print("Parsing Bible subpages for links ...")


    bible_main_pages = ['https://www.wordproject.org/bibles/sw/32/1.htm', 'https://www.wordproject.org/bibles/sw/57/1.htm', 'https://www.wordproject.org/bibles/sw/63/1.htm', 'https://www.wordproject.org/bibles/sw/64/1.htm', 'https://www.wordproject.org/bibles/sw/65/1.htm', 'https://www.wordproject.org/bibles/sw/01/1.htm', 'https://www.wordproject.org/bibles/sw/02/1.htm', 'https://www.wordproject.org/bibles/sw/03/1.htm', 'https://www.wordproject.org/bibles/sw/04/1.htm', 'https://www.wordproject.org/bibles/sw/05/1.htm', 'https://www.wordproject.org/bibles/sw/06/1.htm', 'https://www.wordproject.org/bibles/sw/07/1.htm', 'https://www.wordproject.org/bibles/sw/08/1.htm', 'https://www.wordproject.org/bibles/sw/09/1.htm', 'https://www.wordproject.org/bibles/sw/11/1.htm', 'https://www.wordproject.org/bibles/sw/12/1.htm', 'https://www.wordproject.org/bibles/sw/13/1.htm', 'https://www.wordproject.org/bibles/sw/14/1.htm', 'https://www.wordproject.org/bibles/sw/15/1.htm', 'https://www.wordproject.org/bibles/sw/16/1.htm', 'https://www.wordproject.org/bibles/sw/17/1.htm', 'https://www.wordproject.org/bibles/sw/18/1.htm', 'https://www.wordproject.org/bibles/sw/19/1.htm', 'https://www.wordproject.org/bibles/sw/20/1.htm', 'https://www.wordproject.org/bibles/sw/21/1.htm', 'https://www.wordproject.org/bibles/sw/22/1.htm', 'https://www.wordproject.org/bibles/sw/23/1.htm', 'https://www.wordproject.org/bibles/sw/24/1.htm', 'https://www.wordproject.org/bibles/sw/25/1.htm', 'https://www.wordproject.org/bibles/sw/26/1.htm', 'https://www.wordproject.org/bibles/sw/27/1.htm', 'https://www.wordproject.org/bibles/sw/28/1.htm', 'https://www.wordproject.org/bibles/sw/29/1.htm', 'https://www.wordproject.org/bibles/sw/30/1.htm', 'https://www.wordproject.org/bibles/sw/31/1.htm', 'https://www.wordproject.org/bibles/sw/32/1.htm', 'https://www.wordproject.org/bibles/sw/33/1.htm', 'https://www.wordproject.org/bibles/sw/34/1.htm', 'https://www.wordproject.org/bibles/sw/35/1.htm', 'https://www.wordproject.org/bibles/sw/36/1.htm', 'https://www.wordproject.org/bibles/sw/37/1.htm', 'https://www.wordproject.org/bibles/sw/38/1.htm', 'https://www.wordproject.org/bibles/sw/39/1.htm', 'https://www.wordproject.org/bibles/sw/40/1.htm', 'https://www.wordproject.org/bibles/sw/41/1.htm', 'https://www.wordproject.org/bibles/sw/42/1.htm', 'https://www.wordproject.org/bibles/sw/43/1.htm', 'https://www.wordproject.org/bibles/sw/44/1.htm', 'https://www.wordproject.org/bibles/sw/45/1.htm', 'https://www.wordproject.org/bibles/sw/46/1.htm', 'https://www.wordproject.org/bibles/sw/47/1.htm', 'https://www.wordproject.org/bibles/sw/48/1.htm', 'https://www.wordproject.org/bibles/sw/49/1.htm', 'https://www.wordproject.org/bibles/sw/50/1.htm', 'https://www.wordproject.org/bibles/sw/51/1.htm', 'https://www.wordproject.org/bibles/sw/52/1.htm', 'https://www.wordproject.org/bibles/sw/53/1.htm', 'https://www.wordproject.org/bibles/sw/54/1.htm', 'https://www.wordproject.org/bibles/sw/55/1.htm', 'https://www.wordproject.org/bibles/sw/56/1.htm', 'https://www.wordproject.org/bibles/sw/57/1.htm', 'https://www.wordproject.org/bibles/sw/58/1.htm', 'https://www.wordproject.org/bibles/sw/59/1.htm', 'https://www.wordproject.org/bibles/sw/60/1.htm', 'https://www.wordproject.org/bibles/sw/61/1.htm', 'https://www.wordproject.org/bibles/sw/62/1.htm', 'https://www.wordproject.org/bibles/sw/63/1.htm', 'https://www.wordproject.org/bibles/sw/64/1.htm', 'https://www.wordproject.org/bibles/sw/65/1.htm', 'https://www.wordproject.org/bibles/sw/66/1.htm']

    for ind, page in enumerate(bible_main_pages): 
        
        det_sub = {
            "url":page,
            "parent_tag":"p",
            "parent_class":"ym-noprint",
            "level":(0,1),
            "link_split":["."],
            "url_ext":".htm",
            "exc_tld":True,
            "exc_additional":str(1),
            "numerical" : True
        }

        bible_urls.extend(parse_main(**det_sub))

    
    bible_urls.extend(bible_main_pages)

    print("Parsing Bible pages for text ...")

    for ind, page in enumerate(bible_urls):
        parse_pages(page, 'C:/Users/imran/Documents/NLP', "bible_text", "div", "textBody", 6, ".txt", ["span"])
    
    print("Run time ...", time.time() - start)

    start = time.time()

    quran_url = "https://www.iium.edu.my/deed/quran/swahili/"
    quran_urls = []

    print("Parsing Quran website links ... ")

    det = {
        "url":quran_url,
        "parent_tag":"td",
        "parent_class":"",
        "level":(2,3),
        "link_split":[".", "/"],
        "trailing_zero":"",
        "url_ext":".htm",
        "incl_prepend":"without/",
        "exc_additional" : "",
        "numerical" : True
    }

    quran_urls.extend(parse_main(**det))
    quran_urls.remove(quran_url)

    # append links for commentary of each chapter
    commentary_urls = []
    for url in quran_urls:
        commentary_urls.append(append_comm(url, "/", "c", 0))
    
    quran_urls.extend(commentary_urls)

    print("Parsing Quran pages for text ... ")

    for ind, page in enumerate(quran_urls):
        parse_pages(page, 'C:/Users/imran/Documents/NLP', "quran_text", "p", "", 6, extension = ".txt")

    print("Run time ...", time.time() - start)

    start = time.time()

    sheng_urls = ["https://sheng.co.ke/bonga/bonga.php?topic_id="+str(x) for x in range(1, 1000)]

    print("Parsing sheng pages for text ... ")

    for ind, page in enumerate(sheng_urls):
        print(ind)
        parse_pages(page, 'C:/Users/imran/Documents/NLP', "sheng_text", "p", "", inf, extension = ".txt")

    print("Run time ...", time.time() - start)
    print("Parsing News pages for text ...")

    start = time.time()

    news_urls = ["https://taifaleo.nation.co.ke/sehemu/habari/page/"+str(x) for x in range(2, 101)]
    news_urls.extend(["https://taifaleo.nation.co.ke/sehemu/siasa/page/"+str(x) for x in range(2, 101)])
    news_urls.extend(["https://taifaleo.nation.co.ke/sehemu/michezo/page/"+str(x) for x in range(2, 101)])
    news_urls.extend(["https://taifaleo.nation.co.ke/sehemu/makala/page/"+str(x) for x in range(2, 101)])
    news_urls.extend(["https://taifaleo.nation.co.ke/sehemu/maoni/page/"+str(x) for x in range(2, 51)])

    news_pages = []

    for url in news_urls:
        det = {
        "url":url,
        "parent_tag":"h3",
        "parent_class":"title-semibold-dark",
        "level":(2,3),
        "link_split":[".", "/"],
        "trailing_zero":"",
        "url_ext":".htm",
        "incl_prepend":"without/",
        "exc_additional" : "",
        "numerical" : True
        }
        
        news_pages.extend(parse_main(**det))

    print("Parsing news pages for text ... ")

    for ind, page in enumerate(news_urls):
        parse_pages(page, 'C:/Users/imran/Documents/NLP', "news_text", "p", "", inf, extension = ".txt", exclude=["strong"])

    print("Run time ...", time.time() - start)

    
def append_comm(url:str, divider:str, char:str, position:str):

    # https://www.iium.edu.my/deed/quran/swahili/without/1.htm
    # to https://www.iium.edu.my/deed/quran/swahili/without/c1.htm

    url_lst = url.split(divider)
    url_lst[-1] = url_lst[-1][:position] + char + url_lst[-1][position:]
    new_url = "/".join(url_lst)


    return new_url

if __name__ == '__main__':
    main()