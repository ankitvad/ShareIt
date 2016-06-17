#Check if file is clean or not.
import re
def mainFunction(commentEntered):
	commentEntered = commentEntered.lower()
	commentEntered = re.sub(r'[^ \w]+','',commentEntered)
	commentEntered = commentEntered.replace("_"," ")
	commentEntered = commentEntered.split()
	location = open("dirLocation.txt").read().rstrip("\n")
	textfile = open(location+"/bad-words.txt")
	badwords = textfile.read()
	badwords = badwords.split(",")
	if (set(commentEntered).intersection(badwords)):
		return 0
	else:
		return 1
