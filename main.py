# Some utilities and testing the getStatsForPlayer function

from scraper import getStatsForPlayer

def getStatsForLastFiveGames(playerName):
	statsList = getStatsForPlayer(playerName, 2017)
	return statsList[-5:]

def printStats(statList):
	for stat in statList:
		print "Game: " + stat['Rk'] + ", Date: " + stat['Date'] + ":"
		print "Points: " + stat['PTS'] + ", Rebounds: " + stat['TRB'] + ", Assists: " + stat['AST']
		print

printStats(getStatsForLastFiveGames("James Harden"))
