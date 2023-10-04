from modules.VigenereCipher import VigenereCipher
from modules.VigenereBreaker import VigenereBreaker
import string
import re

def readFile(filename):
	text = None

	try:
		file = open(filename, 'r')
		text = file.read()
		file.close()
	except FileNotFoundError:
		print('\n[ERROR] FILE NOT FOUND IN CURRENT DIRECTORY: '+filename+'\n')

	return text

def writeFile(filename, text):
	file = open(filename, 'w')
	file.write(text)
	file.close()

if __name__ == "__main__":
	cipher = VigenereCipher(string.ascii_uppercase)
	breaker = VigenereBreaker()
	breaker.loadLang('pt',readFile('languages/ptBR.txt'))
	breaker.loadLang('en',readFile('languages/enUS.txt'))

	while True:
		print('VIGENÉRE CIPHER TOOL')
		print('1) Encode Plaintext')
		print('2) Decode Ciphertext')
		print('3) Break Ciphertext')
		print('4) Help')
		print('5) Stop Application')
		print()
		arg = input('Enter an option: ')
		print()

		if arg == '1':
			print('ENCODE PLAINTEXT')
			filename = input('        Enter plaintext filename : ')
			plaintext = readFile(filename)
			if plaintext:
				key = None
				while not key:
					key = input('                       Enter key : ')
					if re.sub('[^'+string.punctuation+'0123456789 \n\t]','',key):
						print('\n[ERROR] KEY MUST NOT CONTAIN NUMBERS OR SYMBOLS\n')
						arg = input('        Enter new key [y/n]? ')
						key = None
						if arg == 'n':
							break
					else:
						break
				if key:
					ciphertext = cipher.encode(plaintext,key)
					print('\n[INFO]  PLAINTEXT READ\n')
					print(plaintext)
					print('\n[INFO]  CIPHERTEXT GENERATED\n')
					print(ciphertext)
					arg = input('\n        Save ciphertext to file enc-'+filename+'[y/n]? ')
					if arg == 'y':
						writeFile('enc-'+filename, ciphertext)
			print()
		elif arg == '2':
			print('DECODE CIPHERTEXT')
			filename = input('        Enter ciphertext filename : ')
			ciphertext = readFile(filename)
			if ciphertext:
				key = None
				while not key:
					key = input('                        Enter key : ')
					if re.sub('[^'+string.punctuation+'0123456789 \n\t]','',key):
						print('\n[ERROR] KEY MUST NOT CONTAIN NUMBERS OR SYMBOLS\n')
						arg = input('        Enter new key [y/n]? ')
						key = None
						if arg == 'n':
							break
					else:
						break
				if key:
					plaintext = cipher.decode(ciphertext,key)
					print('\n[INFO]  CIPHERTEXT READ\n')
					print(ciphertext)
					print('\n[INFO]  PLAINTEXT GENERATED\n')
					print(plaintext)
					arg = input('\n        Save ciphertext to file dec-'+filename+'[y/n]? ')
					if arg == 'y':
						writeFile('dec-'+filename, plaintext)
			print()
		elif arg == '3':
			print('BREAK CIPHERTEXT')
			filename = input('          Enter ciphertext filename : ')
			ciphertext = readFile(filename)
			if ciphertext:
				language = input('        Enter language code [pt/en] : ')
				if breaker.hasLang(language):
					print('\n[INFO]  CIPHERTEXT READ\n')
					print(ciphertext+'\n')
					factors = breaker.keysize(ciphertext,language,3)

					for key, val in factors.items():
						print(str(key)+') '+str(val))

					keysize = input('\nEnter a keysize or ALL to run brute force: ')
					if keysize == 'ALL':
						for i in range(2,21):
							key = breaker.breakVigenere(ciphertext, language, i)
							print('\n[INFO] KEY FOUND: '+key)
							print('[INFO] DECODED TEXT: ')
							print(cipher.decode(ciphertext, key)+'\n')
					else:
						key = breaker.breakVigenere(ciphertext, language, int(keysize))
						print('\n[INFO] KEY FOUND: '+key)
						print('[INFO] DECODED TEXT: ')
						print(cipher.decode(ciphertext, key)+'\n')
				else:
					print('\n[ERROR] UNKNOWN LANGUAGE OPTION: '+language+'\n')
		elif arg == '4':
			print('YOU SHALL FIND NO HELP HERE!\n')
		elif arg == '5':
			break
		else:
			print('[ERROR] INVALID OPTION: '+arg+'\n')
