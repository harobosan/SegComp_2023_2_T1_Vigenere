import re

class VigenereBreaker:
	def __init__(self):
		self.alphabets = {}

	def breakVigenere(self, cipher, lang, keysize = 4):
		chars = ''.join(list(self.alphabets[lang].keys()))
		freqs = list(self.alphabets[lang].values())

		cipher = re.sub('[^'+chars+']','',cipher.upper())

		key = ''
		for i in range(keysize):
			subset = cipher[i::keysize]
			offset = self.freqAnalysis(self.textFreq(subset, chars), freqs)
			key += chr(ord('A')+offset)

		return self.splitKey(key)

	def freqAnalysis(self, text, lang):
		match = []

		for _ in range(len(lang)):
			match.append(sum([text[i]*lang[i] for i in range(len(lang))]))
			text.append(text.pop(0))

		return match.index(max(match))

	def textFreq(self, text, chars):
		freq = dict([(c,0) for c in chars])

		for c in text:
			freq[c] += 1

		for c in chars:
			if freq[c] != 0:
				freq[c] /= len(text)

		return list(freq.values())

	def splitKey(self, key):
		for i in range(int(len(key)/2),1,-1):
			if len(key)%i == 0:
				l = int(len(key)/i)

				for j in range(1,i):
					if key[l*j:].find(key[:l]) != 0:
						l = 0
						break

				if l:
					return key[:int(len(key)/i)]

		return key

	def keysize(self, cipher, lang, size):
		chars = ''.join(list(self.alphabets[lang].keys()))
		cipher = re.sub('[^'+chars+']','',cipher.upper())
		factors = {}

		for i in range(len(cipher)-(size-1)):
			for j in range(i+size, len(cipher)-(size-1)):
				if cipher[j:j+size] == cipher[i:i+size]:
					for k in range(2,21):
						if (j-i)%k == 0:
							factors[k] = 1+factors.get(k,0)
					break

		if len(factors):
			return dict(sorted(factors.items(), key=lambda item: item[0]))
		else:
			return self.keysize(cipher, lang, size-1) if size else {}

	def loadLang(self, lang, alphabet):
		self.alphabets[lang] = {}
		for char in alphabet.split(','):
			pair = char.split(':')
			self.alphabets[lang][pair[0]] = float(pair[1])

	def hasLang(self, lang):
		return bool(self.alphabets.get(lang,None))
