from urllib.parse import quote_plus

from bs4 import BeautifulSoup

from . import models
import requests.compat
from django.shortcuts import render

# Create your views here.
BASE_URL = "https://losangeles.craigeslist.org/search/?query={}"
BASE_IMAGE_URL = "https://images.craigslist.org/{}_300x300.jpg"


def home(request):
    return render(request, 'base.html')


def new_search(request):
    search = request.POST['search']
    models.Search.objects.create(search=search)
    final_url = BASE_URL.format(quote_plus(search))
    response = requests.get(final_url)
    data = response.text
    soup = BeautifulSoup(data, features='html.parser')
    post_list = soup.find_all('li', {'class': 'result-row'})

    final_postings = []

    for post in post_list:
        post_title = post.find(class_="result_title").text
        post_url = post.find('a').get('href')
        if post.find(class_="result-price"):
            post_price = post.find(class_="result-price").text
        else:
            post_price = 'N/A'

        if post.find(class_="result_image").get("data-ids"):
            post_image = post.find(post.find(class_="result_image").get("data-ids")).split(',')[0].split(':')[1]
            post_image_url = BASE_IMAGE_URL.format(post_image)
        else:
            post_image_url = "https://craigslist.org/images/peace.jpg"
        final_postings.append((post_title, post_url, post_price, post_image_url))

    context_frontend = {
        "search": search,
        "final_postings": final_postings
    }

    return render(request, 'ListSearchApp/new_search.html', context_frontend)
