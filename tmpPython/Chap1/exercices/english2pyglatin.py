#saving in a variable the tail of each translated word
pyg = 'ay'

#requesting the user to submit a word
original = raw_input("Enter a word: ")

#checking if the word isn't empty and if it's formed only by alphabetical charcaters
if (len(original) > 0) and original.isalpha():
	#preparing the word for translation
	original = original.lower()
	first = original[0]
	#determining if the original word begins with vowel or consonant
	if first == 'a' or first == 'e' or first == 'i' or first == 'o' or first == 'u':
		print original + pyg
	else:
		print original[1:len(original)] + first + pyg

else:
	print "empty or no valid word"
