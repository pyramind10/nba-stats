# Some utilities and testing the getStatsForPlayer function

from scraper import getStatsForPlayer, getTeamRatings
from math import sqrt
import operator

teamStats = getTeamRatings()

# Get shortened statList only against team teamName
def getStatsAgainstTeam(playerName, teamName):
	statsList = getStatsForPlayer(playerName, 2018)
	newList = []
	teamName = teamName.upper()
	for stat in statsList:
		if stat['Opp'] == teamName:
			newList.append(stat)
	if len(newList) > 0:
		newList[0]['TITLE'] = "PERFORMANCE AGAINST " + teamName
	return newList

# Get shortened statList for last N games
def getStatsForLastNGames(playerName, n):
	statsList = getStatsForPlayer(playerName, 2018)
	if len(statsList) < n:
		n = len(statsList)
	statsList[-n]['TITLE'] = "LAST " + str(n) + " GAMES"
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

# Get the adjusted defensive rating for a team
def getAdjDefRating(teamName):
	global teamStats
	if teamName in teamStats:
		return float(teamStats[teamName]['DRtg/A'])
	return 0.0

# Get ranking of adjusted defensive rating out of 30
def getAdjDefRanking(teamName):
	global teamStats
	defRatings = {}
	for team in teamStats:
		defRatings[team] =  teamStats[team]['DRtg/A']
	sortedRatings = sorted(defRatings.items(), key=operator.itemgetter(1))
	ranking = 1
	for ratings in sortedRatings:
		if ratings[0].upper() == teamName.upper():
			return ranking
		ranking+=1
	return 0

# Returns float of minutes given string timecode MM:SS
def minutesFromTimeCode(timecode):
	if timecode == 'N/A' or timecode == '00:00':
		return 1.0
	tempMin = int(timecode[:timecode.find(':')])
	tempSec = int(timecode[timecode.find(':')+1:])
	totalSeconds = 60.0 * tempMin + tempSec
	return totalSeconds / 60.0

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
	avgLRPerMin = 0
	lrperminStdDev = 0
	subtract = 0
	lrScores = []
	lrPerMin = []
	fdScores = []
	print
	print center("=====" + statList[0]['NAME'] + " (" + statList[0]['Tm'] + ")=====")
	if (statList[0]['TITLE'] != ""):
		print center("----" + statList[0]['TITLE'] + "----")
	print
	for stat in statList:
		print "Game: " + stat['Rk'] + ", Date: " + stat['Date'] + ":\t\tLR Score - " + str(calculateLRScore(stat)) + "\t\tLR / MIN - " + str(round(calculateLRScore(stat) / minutesFromTimeCode(stat['MP'])))
		if (stat['PTS'] == 'N/A'):
			print "Did Not Play"
		else:
			print "Opponent: " + stat['Opp'] + " (ADR: " + str(getAdjDefRanking(stat['Opp'])) + "), Minutes: " + stat['MP']
			print "Points: " + stat['PTS'] + ", Assists: " + stat['AST'] + ", Rebounds: " + stat['TRB']
			lrScores.append(calculateLRScore(stat))
			lrPerMin.append(calculateLRScore(stat) / minutesFromTimeCode(stat['MP']))
			fdScores.append(calculateFDScore(stat))
		print
	if (len(lrScores) > 0):
		avgLR = mean(lrScores)
		lrStdDev = stdev(lrScores)
		avgFD = mean(fdScores)
		fdStdDev = stdev(fdScores)
		avgLRPerMin = mean(lrPerMin)
		lrperminStdDev = stdev(lrPerMin)
	print center("AVERAGE LR SCORE: " + round(avgLR) + ", STD DEV: " + round(lrStdDev))
	print center("AVERAGE LR / MIN: " + round(avgLRPerMin) + ", STD DEV: " + round(lrperminStdDev))
	#print center("AVERAGE FD SCORE: round(avgFD))
	print
	return avgLR, lrStdDev, avgFD, fdStdDev # Return averages and std devs for potential use
