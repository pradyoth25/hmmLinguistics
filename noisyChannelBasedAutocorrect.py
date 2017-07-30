import numpy as np

dictionaryWordFile = '/sscc/home/k/kob734/hw4materials/vocab.txt'
langprobsFile = '/sscc/home/k/kob734/hw4materials/lm.txt'
noiseFile = '/sscc/home/k/kob734/hw4materials/noise.txt'
wordDict = {}
with open(dictionaryWordFile, 'r') as dictionaryWordFile:
	for count, line in enumerate(dictionaryWordFile):
		wordDict[line.rstrip()] = count
# print wordDict, "ends here"
invWordDict = {v: k for k, v in wordDict.iteritems()}
# print invWordDict
langprobs = np.zeros(len(wordDict))
noiseprobs = np.zeros(len(wordDict))
# print langprobs.shape
with open(langprobsFile, 'r') as langprobsFile:
	for line in langprobsFile:
		wordAndProb = line.split('\t')
		# print wordAndProb
		langprobs[wordDict[wordAndProb[0]]] = float(wordAndProb[1])
# print langprobs

with open(noiseFile, 'r') as noiseFile:
	for line in noiseFile:
		wordAndProb = line.split('\t')
		# print wordAndProb
		noiseprobs[wordDict[wordAndProb[0]]] = float(wordAndProb[1])
# print noiseprobs

unnorm_posterior = langprobs * noiseprobs
posterior = unnorm_posterior / np.sum(unnorm_posterior)

max_idx = np.argmax(posterior)
# print invWordDict[max_idx]

# val = posterior[wordDict[max_idx].value()]
print posterior[max_idx]
print np.where(posterior > 0.05)[0]
# print invWordDict[np.where(posterior > 0.05)[0]]
for w in np.where(posterior > 0.05)[0]:
	print invWordDict[w], posterior[w]