from bs4 import BeautifulSoup

import urllib.request as urllib2
import re
import pandas as pd

row_ids = []
sentences = []

def get_sentences(url, ref):
	
	row_id = ".".join(ref.split('/')[3:])

	html = urllib2.urlopen(url)
	soup = BeautifulSoup(html, "html.parser")

	content = soup.find('div', attrs={'class':'field-item even'})
	soup = BeautifulSoup(str(content), "html.parser")
	part_1 = [sentence for sentence in soup.stripped_strings]


	content = soup.find('div', attrs={'class':'field-item odd'})
	soup = BeautifulSoup(str(content), "html.parser")
	part_2 = [sentence for sentence in soup.stripped_strings]

	sent_num = 0
	for sent in filter(lambda x: x != 'None', part_1 + part_2):
		sent_num += 1
		row_ids.append(row_id+'.'+str(sent_num))
		sentences.append(sent)

		# print(row_id+'.'+str(sent_num), sent)



def crawl(url, ref):

	print(url)

	try:
		html = urllib2.urlopen(url)
		soup = BeautifulSoup(html, "html.parser")

		content = soup.find_all('span', attrs={'class':'field-content'})
		
		if len(content) == 0 and re.match('/en/sb/[0-9]+/[0-9]+.*', ref):
			get_sentences(url, ref)
		else:

			for span_obj in content:

				soup = BeautifulSoup(str(span_obj), "html.parser")
				a = soup.find('a', href=True)

				if a is not None:
					crawl(mainpageurl+a.get('href'), a.get('href'))

	except urllib2.HTTPError:
		print("exception")
		pass
	except:
		print("exception")
		pass





# url = "https://www.vedabase.com/en/sb/1/1/1"
# print(get_sentences(url))

mainpageurl="https://www.vedabase.com"
crawl(mainpageurl+"/en/sb/11/", "dummy")

sub = pd.DataFrame()
sub['ids'] = row_ids
sub['sentences'] = sentences
sub.to_csv('canto11.csv', index=False, encoding='utf-8')
