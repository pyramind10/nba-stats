# Some utilities and testing the getStatsForPlayer function

from scraper import getStatsForPlayer

def getStatsAgainstTeam(playerName, teamName):
	statsList = getStatsForPlayer(playerName, 2017)
	newList = []
	for stat in statsList:
		if stat['Opp'] == teamName:
			newList.append(stat)
	return newList

def getStatsForLastFiveGames(playerName):
	statsList = getStatsForPlayer(playerName, 2017)
	return statsList[-5:]

def printStats(statList):
	for stat in statList:
		print "Game: " + stat['Rk'] + ", Date: " + stat['Date'] + ":"
		print "Points: " + stat['PTS'] + ", Rebounds: " + stat['TRB'] + ", Assists: " + stat['AST']
		print

while True:
	person = raw_input("Enter player name (exit to quit): ")
	if (person == 'exit'):
		break
	opp = raw_input("Enter opposing team name: ")
	print
	print "--LAST FIVE GAMES--"
	printStats(getStatsForLastFiveGames(person))
	print "--PERFORMANCE AGAINST " + opp + "--"
	list = getStatsAgainstTeam(person, opp)
	if (len(list) == 0):
		print "Player has not played this team."
	else:
		printStats(getStatsAgainstTeam(person, opp))
