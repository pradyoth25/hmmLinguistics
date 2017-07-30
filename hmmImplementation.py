import numpy as np
from sklearn.preprocessing import normalize

trainingCorpus = '/sscc/home/k/kob734/nltk_data/corpora/brown/brown_100_pos.txt'
dictionaryWordFile = '/sscc/home/k/kob734/nltk_data/corpora/brown/brown_words_hw3.txt'
dictionaryTagFile = '/sscc/home/k/kob734/nltk_data/corpora/brown/brown_tags_hw3.txt'
toyCorpusFile = '/sscc/home/k/kob734/nltk_data/corpora/brown/toy_pos_corpus.txt'
emissionFile = 'emission.txt'
transitionFile = 'transition.txt'
finalFile = open('pos_eval.txt', 'a')


wordDict = {}
with open(dictionaryWordFile, 'r') as dictionaryWordFile:
	for count, line in enumerate(dictionaryWordFile):
		wordDict[line.rstrip()] = count
# print wordDict

tagDict = {}
with open(dictionaryTagFile, 'r') as dictionaryTagFile:
	for count, line in enumerate(dictionaryTagFile):
		tagDict[line.rstrip()] = count

# print tagDict
wordEmission = np.zeros((len(tagDict), len(wordDict)))
tagTransmission = np.zeros((len(tagDict), len(tagDict)))

with open(trainingCorpus, 'r') as inputFile:
	for line in inputFile:
		line = line.rstrip('\n')
		words = line.split(' ')
		# print words
		for i in range(len(words)):
			words[i] = words[i].lower()
		words.append('<end>/<end>')
		# previousWord = '<s>'
		previousTag = '<s>'
		i1 = 0
		j1 = 0
		i2 = 0
		j2 = 0
		for wordTag in words:
			word, tag = wordTag.split('/')
			# print word, tag
		# print ' '
			if word in wordDict.keys():
				j1 = wordDict[word]
				# print j1, "is j1", word, "is word"
			if tag in tagDict.keys():
				i1 = tagDict[tag]
				# print i1, "is i1", tag, "is tag"
			if tag in tagDict.keys():
				j2 = tagDict[tag]
				# print j2, "is j2", tag, "is tag"
			if previousTag in tagDict.keys():
				i2 = tagDict[previousTag]
				# print i2, "is i2", previousTag, "is previosTag"
			# print "------------------"
			wordEmission[i1][j1] += 1
			# print str(wordEmission[i1][j1]), "Incremented wordEmission of",i1,j1
			tagTransmission[i2][j2] += 1
			# print str(tagTransmission[i2][j2]), "Incremeneted tagEmission of", i2,j2
			previousTag = tag
		# previousWord = word

# print wordEmission.max()
# print tagTransmission.max()

wordProbs = normalize(wordEmission, norm='l1', axis=1)
tagProbs = normalize(tagTransmission, norm='l1', axis=1)

# print wordProbs
# print tagProbs
with open(emissionFile, 'a') as emissionFile:
	emissionFile.write(str(wordProbs[tagDict['nn']][wordDict['weekend']]) + "\n")
	emissionFile.write(str(wordProbs[tagDict['np']][wordDict['texas']])+ "\n")
	emissionFile.write(str(wordProbs[tagDict['to']][wordDict['to']])+ "\n")
	emissionFile.write(str(wordProbs[tagDict['jj']][wordDict['old']])+ "\n")

with open(transitionFile, 'a') as transitionFile:
	transitionFile.write(str(tagProbs[tagDict['nn']][tagDict['nn']])+ "\n")
	transitionFile.write(str(tagProbs[tagDict['nn']][tagDict['.']])+ "\n")
	transitionFile.write(str(tagProbs[tagDict['.']][tagDict['<end>']])+ "\n")
	transitionFile.write(str(tagProbs[tagDict['to']][tagDict['vb']])+ "\n")

with open(toyCorpusFile, 'r') as toyFile:
	for line in toyFile:
		line = line.rstrip('\n')
		words = line.split(' ')
		# print words
		for i in range(len(words)):
			words[i] = words[i].lower()
		words.append('<end>/<end>')
		# previousWord = '<s>'
		previousTag = '<s>'
		i1 = 0
		j1 = 0
		i2 = 0
		sentProb = 1
		sum1 = 0
		# j2 = 0
		for wordTag in words:
			word, tag = wordTag.split('/')
			if word in wordDict.keys():
				j1 = wordDict[word]
			if tag in tagDict.keys():
				i1 = tagDict[tag]
			if previousTag in tagDict.keys():
				i2 = tagDict[previousTag]	
			wordTagProb = wordProbs[i1][j1]
			tagTagProb = tagProbs[i2][i1]
			sentProb *= wordTagProb
			sentProb *= tagTagProb
			# print sentProb, "is sentProb"
			previousTag = tag
		finalFile.write(str(sentProb)+"\n")
		# print 'sentence is over'

finalFile.close()
