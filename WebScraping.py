#importar bibliotecas
import urllib.request as urllib2
from bs4 import BeautifulSoup ,Comment
import html2text
import csv
from selenium import webdriver
import time
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
import Selenium2Library


#pegar o menu pincipal
url = 'https://lista.mercadolivre.com.br/veiculos/carros-caminhonetes/gol/'
request = urllib2.Request(url,headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.190 Safari/537.36'})
page = urllib2.urlopen(request)
soup = BeautifulSoup(page, 'html.parser')

rows = soup.find("section" ,class_='ui-search-results ui-search-results--without-disclaimer').find_all('li',class_ = 'ui-search-layout__item')


#pegar a categoria
url2 = ('https://www.mercadolivre.com.br/c/carros-motos-e-outros#menu=categories')
request2 = urllib2.Request(url2,headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.190 Safari/537.36'})
page2 = urllib2.urlopen(request2)
soup2 = BeautifulSoup(page2,'html.parser')

categoria_row = soup2.find('div',class_='desktop__view')

#abrir o arquivo csv
ml = open('MercadoLivre.csv','w',newline='')
writer = csv.writer(ml,delimiter = ';')
writer.writerow(['Categoria','Data','Grupo','Produto','Ano Do Carro','Estado','Valor'])

#Selenium
driver = webdriver.Chrome(ChromeDriverManager().install())
driver.get(url)
def Simulador_teclas():
    prox_pag = driver.find_element_by_xpath("//a[@title = 'Seguinte']").send_keys(Keys.ENTER)
    time.sleep(10)


#Web scraping
def Scrap():
    for row in rows:
            data = '25/02/2021' 
            grupo = soup.h1.contents[0]
            categoria = categoria_row.find('h2',class_='category-list__title').text.strip()
            itens = row.find("h2" ,class_="ui-search-item__title ui-search-item__group__element").text.strip()
            ano_carro = row.find("li", class_="ui-search-card-attributes__attribute").text.strip()
            valor = row.find("div", class_ = "ui-search-price__second-line").text.strip()
            estado = row.find("span", class_ = "ui-search-item__group__element ui-search-item__location")
            writer.writerow([categoria,data,grupo,itens,ano_carro,estado,valor])
    

for i in range(10):
    Scrap()
    try:
        Simulador_teclas()
    except:
        print('O limite de paginas foi alcançado')
        break
    print('{}º Vez'.format(i+1))
    new_url = driver.current_url
    url = new_url
    request = urllib2.Request(url,headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.190 Safari/537.36'})
    page = urllib2.urlopen(request)
    soup = BeautifulSoup(page, 'html.parser')
    rows = soup.find("section" ,class_='ui-search-results ui-search-results--without-disclaimer').find_all('li',class_ = 'ui-search-layout__item')

ml.close()
























  