import sys
sys.path.insert(0, 'utilities/')
import listutilities

if len(sys.argv) > 1:
	filename = sys.argv[1]
else:
	filename = 'players.txt'
print "Reading from " + filename
listutilities.readList(filename)
