# Contains function that reads .csv file for a certain player and returns 
# a list of dictionaries with all stats

# Example of how to access stats using this list: (Remember that games[0] refers to the 1st game)
# games[0]['Opp'] would return the name of the opponent's team of the player's first game

def getStats(fileName):
	file = open(fileName)

	games = []
	headers = file.readline()
	headerArr = headers.strip().split(',')
	for line in file:
		arr = line.strip().split(',')
		dict = {}
		i = 0
		for char in arr:
			dict[headerArr[i]] = char
			i+=1
		games.append(dict)

	return games

getStats("aaron-gordon.csv")

