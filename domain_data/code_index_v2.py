import os
import sys
import re
import time
import errno
import nltk
import json
import xml.sax.handler
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer, SnowballStemmer
from nltk.tokenize import wordpunct_tokenize
from copy import deepcopy
from string import punctuation
from collections import defaultdict

# stopWords = set(stopwords.words('english'))
# stopWords.update(list(char for char in punctuation))

dpStemmer = dict()

# stemmer = PorterStemmer()
stemmer = SnowballStemmer('english')
stopWords = dict()

pattern = re.compile("[^a-zA-Z0-9]+")
cssExp = re.compile(r'{\|(.*?)\|}', re.DOTALL)
filePattern = re.compile(r'\[\[file:(.*?)\]\]', re.DOTALL)
linkExp = re.compile(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', re.DOTALL)

result = defaultdict()


class buildIndex(xml.sax.ContentHandler) :

	def __init__(self) :

		self.istitle = False
		self.isid = False
		self.istext = False
		self.title = ""
		self.id = ""
		self.text = ""
		self.pageCount = 0
	

	def loadStopWords(self, filePath) :

		global stopWords

		stopFile = open(filePath, "r")
		words = stopFile.readlines()
		for word in words :
			word = word.split("\n")
			stopWords[word[0]] = 1	  


	def infoboxProcessing(self, textString) :

		flag1 = 0
		flag2 = 0
		temp_str = textString
		# temp = re.split(r'\{\{\s?Infobox', temp_str, flags=re.IGNORECASE)
		# if len(temp) <=1 :
		# 	flag1 = 1
		words = re.split(pattern, textString)
		words = list(map(str.lower, words))
		for w in words :
			if w == "infobox" :
				flag1 = 1
				break
		if "{{ज्ञानसंदूक" in temp_str : 
			flag2 = 1
		if flag1==1 or flag2==1 :
			return True	
		else :	
			return False


	def textProcessing(self, textString) :

		# textString = linkExp.sub('', str(textString))
		# textString = cssExp.sub('', str(textString))
		# textString = filePattern.sub('', str(textString))
		infobox = self.infoboxProcessing(textString)

		return infobox


	def preprocessing(self, title, article_id, text) :

		global result
		pageCount = self.pageCount
		
		infobox = self.textProcessing(text)
		if infobox == False :
			result[article_id] = title
		

	def startElement(self, name, attribute) :

		if name == "title" :
			self.istitle = True
			self.title = list()
		elif name == "id" :
			self.isid = True
			self.id = list()	
		elif name == "text" :
			self.istext = True
			self.text = list()


	def endElement(self, name) :

		if name == "title" :
			self.istitle = False
		if name == "id" :
			self.isid = False	
		elif name == "text" :
			self.istext = False
		elif name == "page" :
			self.pageCount = self.pageCount + 1
			text = ''.join(self.text)
			title = ''.join(self.title)
			article_id = ''.join(self.id)
			self.preprocessing(title, article_id, text)
			if self.pageCount % 5000 == 0:
				print("Done : ", self.pageCount)


	def characters(self, content) :
		if self.istitle :
			self.title.append(content)
		elif self.isid :
			self.id.append(content)	
		elif self.istext :
			self.text.append(content)



if __name__ == "__main__" :

	indexPath = sys.argv[2]
	# statPath = sys.argv[3]
	# if not os.path.exists(indexPath) :
		# os.makedirs(indexPath)

	xml_parser = xml.sax.make_parser()
	print("here")
	Indexer = buildIndex()
	# Indexer.loadStopWords("2019201090/stopwords.txt")
	xml_parser.setContentHandler(Indexer)
	xml_parser.parse(sys.argv[1])
	print(Indexer.pageCount)
	with open(indexPath + "result.json", 'w') as fp :
		json.dump(result, fp)