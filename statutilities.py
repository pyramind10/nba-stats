# Some utilities and testing the getStatsForPlayer function

from scraper import getStatsForPlayer
from math import sqrt

# Get shortened statList only against team teamName
def getStatsAgainstTeam(playerName, teamName):
	statsList = getStatsForPlayer(playerName, 2017)
	newList = []
	teamName = teamName.upper()
	for stat in statsList:
		if stat['Opp'] == teamName:
			newList.append(stat)
	return newList

# Get shortened statList for last N games
def getStatsForLastNGames(playerName, n):
	statsList = getStatsForPlayer(playerName, 2017)
	return statsList[-n:]

# Calculates score for a statline for letsRUMBL
def calculateLRScore(stat):
	if (stat['PTS'] == 'N/A'):
		return 0
	totalScore = int(stat['PTS']) + 1.5 * int(stat['TRB']) + 1.5 * int(stat['AST']) + 2 * int(stat['BLK']) + 2 * int(stat['STL']) - int(stat['TOV'])
	return totalScore

# Calculates score for a statline for FanDuel
def calculateFDScore(stat):
	if (stat['PTS'] == 'N/A'):
		return 0
	totalScore = int(stat['PTS']) + 1.2 * int(stat['TRB']) + 1.5 * int(stat['AST']) + 2 * int(stat['BLK']) + 2 * int(stat['STL']) - int(stat['TOV'])
	return totalScore

# Centers given string in terminal
def center(string):
	return "{:^80}".format(string)

# Round float to 2 digits
def round(decimal):
	return "{0:.2f}".format(decimal)

# Returns mean of given list
def mean(numList):
	if (len(numList) == 0):
		return 0
	sum = 0
	for item in numList:
		sum += item
	return sum / len(numList)

# Returns std dev of given list
def stdev(lst):
	if (len(lst) <= 1):
		return 0
	num_items = len(lst)
	mean = sum(lst) / num_items
	differences = [x - mean for x in lst]
	sq_differences = [d ** 2 for d in differences]
	ssd = sum(sq_differences)
	variance = ssd / (num_items - 1)
	return sqrt(variance)


# Prints stats of statList out to screen and returns LR, FD averages
def printStats(statList):
	lrStdDev = 0
	fdStdDev = 0
	avgLR = 0
	avgFD = 0
	subtract = 0
	lrScores = []
	fdScores = []
	for stat in statList:
		print "Game: " + stat['Rk'] + ", Date: " + stat['Date'] + ":\t\tLR Score - " + str(calculateLRScore(stat)) + "\t\tFD Score - " + str(calculateFDScore(stat))
		if (stat['PTS'] == 'N/A'):
			print "Did Not Play"
		else:
			print "Points: " + stat['PTS'] + ", Rebounds: " + stat['TRB'] + ", Assists: " + stat['AST']
			lrScores.append(calculateLRScore(stat))
			fdScores.append(calculateFDScore(stat))
		print
	if (len(lrScores) > 0):
		avgLR = mean(lrScores)
		lrStdDev = stdev(lrScores)
		avgFD = mean(fdScores)
		fdStdDev = stdev(fdScores)
	print center("AVERAGE LR SCORE: " + round(avgLR) + ", STD DEV: " + round(lrStdDev))
	#print center("AVERAGE FD SCORE: round(avgFD))
	print
	return avgLR, lrStdDev, avgFD, fdStdDev # Return averages and std devs for potential use


