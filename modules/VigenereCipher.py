class VigenereCipher:
	def __init__(self, alphabet, case_sensitive = False):
		self.alphabet = alphabet
		self.tables = {}
		self.case_sensitive = case_sensitive

		for i in range(len(self.alphabet)):
			shift = self.alphabet[i:]+self.alphabet[:i]
			enc = {}
			dec = {}

			for j in range(len(self.alphabet)):
				enc[self.alphabet[j]] = shift[j]
				dec[shift[j]] = self.alphabet[j]

			self.tables[self.alphabet[i]] = (enc, dec)

	def encode(self, message, key):
		return self.vigenere(message, key)

	def decode(self, cipher, key):
		return self.vigenere(cipher, key, decode = True)

	def vigenere(self, text_in, key, decode = False):
		keystring = self.keystring(key, len(text_in))
		text_out = ''

		if not self.case_sensitive:
			text_in = text_in.upper()

		j = 0
		for i in range(len(text_in)):
			c = text_in[i]
			k = keystring[j]

			if c in self.alphabet and k in self.alphabet:
				text_out += self.tables[k][int(decode)][c]
				j += 1
			else:
				text_out += c

		return text_out

	def keystring(self, key, size):
		keystring = ''

		for i in range(size):
			keystring += key[i%len(key)].upper()

		return keystring
