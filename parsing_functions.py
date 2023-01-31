from multiprocessing import Pool
from bs4 import BeautifulSoup as BS
import datetime
import requests
var1=str(datetime.datetime.today().date())
BASE_URL=f'https://kaktus.media/?lable=8&date={var1}&order=popular'




def getHtml(url):
    '''Requests HTML from url'''
    return requests.get(url).text

def findArticles(html):
    '''Finds all articles in popular ones. Returns LIST'''
    catSoup=BS(html,'lxml')
    articles=catSoup.find('div',class_='Tag--articles').findAll('div',class_='Tag--article')
    for x in range(len(articles)):
        if len(articles)>20:
            articles.pop()
    return articles

def parseArticles(listOfArticles:list):
    '''Returns List of names, list of links, list of views, list of image-links'''
    list_of_names=[]
    list_of_links=[]
    list_of_views=[]
    list_of_images=[]
    for x in listOfArticles:
        try:
            var1=x.find('a',class_='ArticleItem--name').text.strip().replace('\n','')
        except:
            var1='NameNotFound'
        try:
            var2=x.find('a',class_='ArticleItem--name').get('href').strip().replace('\n','')
        except:
            var2='LinkNotFound'
        try:
            var3=x.find('div',class_='ArticleItem--views').text.strip().replace('\n','')
        except:
            var3='ViewsNotFound'
        try:
            var4=x.find('img').get('src')
        except:
            var4=False
        list_of_names.append(var1)
        list_of_links.append(var2)
        list_of_views.append(var3)
        list_of_images.append(var4)
    return list_of_names,list_of_links,list_of_views,list_of_images

def getDetails(url):
    detSoup=BS(getHtml(url),'lxml')
    title=detSoup.find('div',class_='Article--block-content').find('h1',class_='Article--title').find('span').text
    listOfDescriptions=detSoup.find('div',class_='BbCode').find_all('p')
    description=''
    for x in listOfDescriptions:
        x=str(x.text)
        description=description+''.join(x)
    return title+'\n\n'+description


def getPhoto(url):
    photoSoup=BS(getHtml(url),'lxml')
    try:
        var1=photoSoup.find('div',class_='BbCode')
    except:
        return False
    try:
        list_ofPhotos=var1.find('div',class_='Gallery Gallery--multi').find_all('a')
        try:
            listPhotos=[]
            for x in list_ofPhotos:
                j=x.get('href').strip()
                listPhotos.append(j)
            set_of_photos=set(listPhotos)
            photosList=list(set_of_photos)
            return photosList
        except:
            return False
    except:
        try:
            photo=var1.find('div',class_='Gallery--single-image').find('a').get('href')
            return photo
        except:
            return False




def getVideo(url):
    list_of_vids=[]
    try:
        videoSoup=BS(getHtml(url),'lxml')
        var1=videoSoup.find('div',class_='BbCode')
        var2=var1.find('div',class_='bb-video').find('div',class_='bb-video-content').findAll('iframe')
        for x in var2:
            j=x.get('src')
            list_of_vids.append(j.strip())
        return list_of_vids
    except:
        return False








if __name__=='__main__':
    getVideo('https://kaktus.media/doc/474710_genprokyror_iskluchil_davlenie_na_sledovateley_v_kempir_abadskom_dele.html')