from django.shortcuts import render
import json
import bs4
from urllib.request import urlopen
from django.http import HttpResponse
import pandas as pd

def URL(body, url):
    if body['Category']:
        Category = body['Category']
        url = url + "-" + Category.replace(" ", "-").lower() + "-internships"
    else:
        url = url + "-internships"
    if body['Location']:
        Location = body['Location']
        url = url + "-in-" + Location.replace(" ", "-").lower()
    if body['Stipend']:
        Stipend = body['Stipend']
        url = url + "/stipend-" + str(Stipend) 
    return url


def ScrapperApi(request):
    pages = 1
    url = "https://internshala.com/internships/work-from-home"

    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)
    final_url = URL(body, url)
    final_url = final_url + "/page-"
    print(final_url)
    x = InternshalaCall(final_url, pages)

    return HttpResponse(final_url)

def InternshalaCall(final_url, pages):
    page_no = 1
    # intern_list = []
    Title = []
    Company = []
    Stipend = []
    while page_no <= pages:
        response = urlopen(final_url + str(page_no))
        soup = bs4.BeautifulSoup(response)
        title = soup.findAll('h3', {'class': 'heading_4_5 profile'})
        company = soup.findAll('a', {'class': 'link_display_like_text view_detail_button'})
        # duration = soup.findAll('div', {'class': 'item_body'})
        stipend = soup.findAll('span', {'class': 'stipend'})
        print(len(title))
        print(len(stipend))
        print(stipend[0].text)
        print(stipend[1].text)
        print(stipend[2].text)
        print(stipend[3].text)
        for item in range(len(stipend)):
            Title.append(title[item].text.replace('\n','').replace(' ', ''))
            Company.append(company[item].text.replace('\n','').replace(' ', ''))
            Stipend.append(stipend[item].text)


        page_no = page_no + 1
    data = {
        'Title': Title,
        'Company': Company,
        'Stipend': Stipend,
    }

    df = pd.DataFrame(data)
    print(df)
    return df