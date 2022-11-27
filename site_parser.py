import requests
from bs4 import BeautifulSoup as bs
import csv
import re


def parse_pages(root_url, pages, url_tld, directory, filename, extension=".csv", headers=[], exclude={}):

    for i in range(1,pages):

        url = root_url + "/" + str(i) + url_tld
        # print(url)
        response = requests.get(url)
        html = response.text
        res = bs(html, "html.parser")
        out_file = directory + '/' + filename +  extension

        # with open(out_file, 'a', encoding='UTF8') as file:
        #     file.write("Hii")

        for x in res.find_all("div", {"textBody"}):
            contents = x.contents[6]
            contents = clean_content(contents, "span")

            with open(out_file, 'a', encoding='UTF8') as file:            
                file.write(contents)

        return contents
        # if extension == '.csv':
        #     header = ["name", "purchase_price", "image_1"]
        # for x in res.find_all("a", {"woocommerce-LoopProduct-link woocommerce-loop-product__link"}):

        #     h = x.find("h2", {"woocommerce-loop-product__title"})
        #     s = x.find("span", {"woocommerce-Price-amount"})
        #     i = x.find("img")['src']

        #     title = h.contents[0]
        #     price = s.contents[1].strip('\xa0')
        #     image = i

        #     item = [title,price,image]

        #     with open(, 'a', encoding='UTF8') as file:
        #         writer = csv.writer(file)
        #         writer.writerow(item)
        
        # elif extension == '.txt':

def clean_content(text, tag):
    # print("Text ", text)
    str(text).replace("<p>", "")
    str(text).replace("</p>", "")
    str(text).replace("</br>", "")
    str(text).strip()
    tag_string = "<[" + tag + "][^>]*>(.+?)</[" + tag + "]>"
    str_mod = re.sub(">(.+?)<", '', str(text))
    str_mod = re.sub("<(.+?)>", '',str_mod)
    str_mod = re.sub("\r", '',str_mod)
    # str_mod.replace("\r", "")
    # print(str_mod)
    return str_mod

if __name__ == '__main__':
    parse_site("https://www.wordproject.org/bibles/sw/01", 51,'.htm','C:/Users/imran/Documents/NLP',"bible_text", ".txt", {"span":"verse", "<br/>" : ""})
