from bs4 import BeautifulSoup
import requests
#pip install progress
from progress.bar import Bar
import json

history = None

try:
	f = open("history.json", "r")
	choice = input('Há um histórico, deseja carregar as páginas à partir dele [s/n]? ')
	if(str(choice).lower() == 's'):
		history = json.load(f)
	f.close()
except FileNotFoundError:
	print('Não há um histórico')


url = "http://deeplearningbook.com.br/capitulos/page/%d/"
headers = {
	 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36'}
numberPagina = 0

links = []

bar = Bar('Obtendo links', max=4)
bar.next()

while True:
	numberPagina += 1
	page = requests.get(url % numberPagina, headers = headers)

	if page.status_code != 200:
		if(len(links) == 0):
			print("Erro %s" % page.status_code)
		break
	
	soup = BeautifulSoup(page.text, "html.parser")
	try:
		tagTitle = soup.find("div", class_="posts-layout").find_all("h4",class_="entry-title")
	except:
		pass
	else:
		for tagTitleItem in tagTitle:
			tagLink = tagTitleItem.find("a")
			links.append(tagLink.attrs["href"])
		bar.next()

bar.finish()
# Link no array links
links.reverse()

capitulos = []
newHistory = {}

arq = open("links.txt", "w+")

soup_ul = BeautifulSoup("<ul></ul>", "html.parser")
ul_tag = soup_ul.ul

bar = Bar('Lendo capítulos', max=len(links))

for idx,link in enumerate(links, start=1):
	arq.write(link + '\n')

	if history is not None and idx <= len(history):
		soup = BeautifulSoup(history[str(idx)], "html.parser")
	else:
		try:
			page = requests.get(link, headers = headers)
			if page.status_code != 200:
				if(idx != len(links)):
					print("\nErro %s" % page.status_code)
				break
		except Exception as e:
			print(e)
			break

		soup = BeautifulSoup(page.text, "html.parser")

	h1_tag = soup.find("h1", class_="entry-title")
	h1_tag['id'] = "capitulo-%d" % idx

	dados = h1_tag.prettify()
	dados += soup.find("div", class_="entry-content").prettify()
	capitulos.append(dados)

	newHistory[str(idx)] = dados

	new_li = soup_ul.new_tag("li")
	new_a = soup_ul.new_tag("a", href="#capitulo-%d" % idx)
	new_a.string = h1_tag.text
	new_li.append(new_a)
	ul_tag.append(new_li)
	
	bar.next()
#Para fechar arquivo
arq.close()
if(history is not None and not newHistory):
	newHistory = history
arq = open("history.json", 'w+')
json.dump(newHistory, arq)
arq.close()

bar.finish()

arq = open("dados2.html", 'w+')
arq.write("""
<!DOCTYPE html><html lang=pt-br prefix='og: https://ogp.me/ns# fb: https://ogp.me/ns/fb#'><head><meta charset="utf-8" /><style>p img{\display:block;margin-left:auto;margin-right:auto}.one-page{min-height:1550px;display:block;margin-bottom:50px}.first-page{position:relative;border:3px solid #0a2f5c}.content-first-page{margin:0;position:absolute;top:50%;left:50%;-ms-transform:translate(-50%,-50%);transform:translate(-50%,-50%);text-align:center}.content-first-page h1,.content-first-page p{text-align:center;margin-bottom:5em}.summary li{font-size:1.1em;margin-top:.2em}</style></head><body><div class="first-page one-page"><div class=content-first-page><h1> DEEPLEARNING BOOK BY V1pi</h1><p><img width=690 height=318 src="https://i0.wp.com/deeplearningbook.com.br/wp-content/uploads/2018/01/deep-learning-book.jpg?fit=690%2C318" alt="Deep Learning Book" srcset="https://i0.wp.com/deeplearningbook.com.br/wp-content/uploads/2018/01/deep-learning-book.jpg?w=780 780w, https://i0.wp.com/deeplearningbook.com.br/wp-content/uploads/2018/01/deep-learning-book.jpg?resize=300%2C138 300w, https://i0.wp.com/deeplearningbook.com.br/wp-content/uploads/2018/01/deep-learning-book.jpg?resize=768%2C354 768w, https://i0.wp.com/deeplearningbook.com.br/wp-content/uploads/2018/01/deep-learning-book.jpg?resize=200%2C92 200w, https://i0.wp.com/deeplearningbook.com.br/wp-content/uploads/2018/01/deep-learning-book.jpg?resize=690%2C318 690w" sizes="(max-width: 690px) 100vw, 690px" data-attachment-id=113 data-permalink=http://deeplearningbook.com.br/deep-learning-book/deep-learning-book/ data-orig-file="https://i0.wp.com/deeplearningbook.com.br/wp-content/uploads/2018/01/deep-learning-book.jpg?fit=780%2C360" data-orig-size=780,360 data-comments-opened=0 data-image-meta={&quot;aperture&quot;:&quot;0&quot;,&quot;credit&quot;:&quot;&quot;,&quot;camera&quot;:&quot;&quot;,&quot;caption&quot;:&quot;&quot;,&quot;created_timestamp&quot;:&quot;0&quot;,&quot;copyright&quot;:&quot;&quot;,&quot;focal_length&quot;:&quot;0&quot;,&quot;iso&quot;:&quot;0&quot;,&quot;shutter_speed&quot;:&quot;0&quot;,&quot;title&quot;:&quot;&quot;,&quot;orientation&quot;:&quot;0&quot;} data-image-title="Deep Learning Book" data-image-description data-medium-file="https://i0.wp.com/deeplearningbook.com.br/wp-content/uploads/2018/01/deep-learning-book.jpg?fit=300%2C138" data-large-file="https://i0.wp.com/deeplearningbook.com.br/wp-content/uploads/2018/01/deep-learning-book.jpg?fit=780%2C360"></p><p class=description>Cópia não oficial do livro disponível no <a href=http://deeplearningbook.com.br/>site</a> da galera do Data Science Academy. Este arquivo é disponibilizado em formato PDF e mobi.</p></div></div><div class="one-page summary"><h1>Sumário</h1>
	"""+ul_tag.prettify()+"</div>")

bar = Bar('Escrevendo HTML', max=len(capitulos))
for capitulo in capitulos:
	arq.write(capitulo + "<br/><hr><br/>")
	bar.next()

bar.finish()

arq.write("</body></html>")
arq.close()
