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
        if len(articles)>21:
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
    # print(f'{list_of_names}\n\n\n\n\n\n\n\n\n{list_of_links}\n\n\n\n\n\n\n\n\n{list_of_views}')
    return list_of_names,list_of_links,list_of_views,list_of_images

def getDetails(url):
    detSoup=BS(getHtml(url),'lxml')
    title=detSoup.find('div',class_='Article--block-content').find('h1',class_='Article--title').find('span').text
    listOfDescriptions=detSoup.find('div',class_='BbCode').find_all('p')
    # listOfDescriptions1=detSoup.find('div',class_='BbCode').text
    description=''
    for x in listOfDescriptions:
        # try:
            # i=x.findAll('a')
            # if not i==None:
            #     for g in i:
            #         x=x.replace(g,g.text)
            # x=str(x).replace('<p>','').replace('  ',' ').replace('</p>','\n').strip().replace('<b>',' ').replace('</b>',' ').replace('<em>',' ').replace('</em>',' ').replace('<br>',' ').replace('</br>','\n')
            # description=description+''.join(x)            
        # except:
            x=str(x).replace('<p>','').replace('  ',' ').replace('</p>','\n').strip().replace('<b>',' ').replace('</b>',' ').replace('<em>',' ').replace('</em>',' ').replace('<br>',' ').replace('</br>','\n')
            
            # var2=x.index('<a class=')
            # var3=x.index('</a>')
            # var4=var3-var2
            # print(var2,var3,var4)
            # for h in range(var4):
            #     var5=[lo for lo in x]
            #     var5[var2]=''
            #     ki=''
            #     for km in var5:
            #         x=ki+''.join(km)

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
            # print(list_ofPhotos)
            for x in list_ofPhotos:
                # print(x.get('href'))
                j=x.get('href').strip()
                listPhotos.append(j)
            set_of_photos=set(listPhotos)
            photosList=list(set_of_photos)
            return photosList
        except:
            return 1
    except:
        try:
            photo=var1.find('div',class_='Gallery--single-image').find('a').get('href')
            return photo
        except:
            return False













if __name__=='__main__':
    # print(getDetails('https://kaktus.media/doc/474699_myzey_izo_povysil_ceny_na_bilet._i_sdelal_ee_raznoy_dlia_kyrgyzstancev_i_inostrancev.html'))
    print(findArticles(getHtml(BASE_URL))[0])