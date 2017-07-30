import nltk
import numpy as np
from sklearn.preprocessing import normalize

path = nltk.data.path[0] + '/corpora/brown/brown_vocab_100.txt'
readPath = nltk.data.path[0] + '/corpora/brown/brown_100.txt'
wordDict = {}
with open(path, 'r') as inputFile:
	for count, line in enumerate(inputFile):
		wordDict[line.rstrip()] = count

counts = np.zeros((813,813))

with open(readPath, 'r') as inputFile:
	for line in inputFile:
		line = line.rstrip('\n')
		words = line.split(' ')
		for i in range(len(words)):
			words[i] = words[i].lower()
		words.append('</s>')
		previous_word = '<s>'
		i = 0
		j = 0
		for word in words:
			if word in wordDict.keys():
				j = wordDict[word]
			if previous_word in wordDict.keys():
				i = wordDict[previous_word]
			# print "[",word, "]is word [", previous_word, "]is previousWord"
			# print "indices of i and j are", i,j
			counts[i][j] +=1
			# print counts[i][j], "is countsOf",i,j
			previous_word = word
		# print counts
# print counts.max(), "is the max of the counts matrix"
counts += 0.1
probs = normalize(counts, norm='l1', axis=1)
# print probs
with open('smoothed_probs.txt', 'a') as bigramFile:
	bigramFile.write(str(probs[0][603])+"\n")
	bigramFile.write(str(probs[603][80])+"\n")
	bigramFile.write(str(probs[603][107])+"\n")
	bigramFile.write(str(probs[34][802])+"\n")
# print probs[0][603]
# print probs[603][80]
# print probs[603][107]
# print probs[34][802]

sentenceListProb = []
perplexityList = []
toyPath = nltk.data.path[0] + '/corpora/brown/toy_corpus.txt'
with open(toyPath, 'r') as corpusFile:
	for line in corpusFile:
		line = line.rstrip('\n')
		words = line.split(' ')
		for i in range(len(words)):
			words[i] = words[i].lower()
		words.append('</s>')
		sentprob = 1
		wordCount = 0
		previous_word = '<s>'
		i = 0
		j = 0
		for word in words:
			if word in wordDict.keys():
				j = wordDict[word]
			if previous_word in wordDict.keys():
				i = wordDict[previous_word]
			wordProb = probs[i][j]
			# print wordProb
			sentprob *= wordProb
			# print sentprob
			wordCount +=1
			previous_word = word
		# print sentprob, "is the sentence probability"	
		sentenceListProb.append(sentprob)
		# print wordCount
		perplexity = 1/(pow(sentprob, 1.0/wordCount))
		perplexityList.append(perplexity)

# print sentenceListProb
# print perplexityList

with open('smoothed_eval.txt', 'a') as finalFile:
	# for prob in sentenceListProb:
	# 	finalFile.write(str(prob)+"\n")
	for perplex in perplexityList:
		finalFile.write(str(perplex)+"\n")