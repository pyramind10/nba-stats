# Utilities to read in lists of players and get averages, etc.
# Format of one line in .txt (no space between player and opp team):
# lebron james,gsw

import statutilities as su
import time
import operator

# GLOBALS:
lastNGames = 10

# Used for color text output
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def readList(fileName):
	file = open("lists/" + fileName)
	players = {} # dict containing statLists
	oppTeamNames = {} # dict containing opposing team names
	avgLRScore = {} # dict containing average LR scores
	avgFDScore = {} # dict containing average FD scores
	lrStdDeviations = {} # dict containing std. devs
	fdStdDeviations = {}

	# Populate dictionary of players
	for line in file:
		time.sleep(1.2)
		arr = line.strip().split(',')
		players[arr[0]] = su.getStatsForLastNGames(arr[0], lastNGames)
		oppTeamNames[arr[0]] = arr[1].strip()
		avgLRScore[arr[0]], lrStdDeviations[arr[0]], avgFDScore[arr[0]], fdStdDeviations[arr[0]] = su.printStats(players[arr[0]])
		print

	# Get players with top 7 LR Scores
	l = 8;
	sortedAvgs = sorted(avgLRScore.items(), key=operator.itemgetter(1), reverse=True)
	if (len(sortedAvgs) < l):
		l = len(sortedAvgs)
	sortedAverages = sortedAvgs[:l]
	# Each item in sortedAverages is a tuple,
	# where avg[0] is the player name and avg[1] is the LRScore average
	# Example: sortedAverages = [('James Harden', 45.5), ('Lebron James', 55.2)]

	# Print ranked averages
	print bcolors.OKGREEN + su.center("=========================================")
	print su.center("TOP " + str(l) + " LR AVERAGES OVER LAST " + str(lastNGames) + " GAMES")
	print su.center("=========================================")

	rank = 1
	for avg in sortedAverages:
		print "\t  {:18}".format(str(rank) + ": " + avg[0].upper()) + "\t - LR Average: " + su.round(avg[1]) + ", STD DEV: " + su.round(lrStdDeviations[avg[0]])
		rank+=1

	# Print last N games
	print bcolors.ENDC
	print su.center("=========================================")
	print su.center("LAST " + str(lastNGames) + " GAMES")
	print su.center("=========================================")

	for avg in sortedAverages:
		su.printStats(players[avg[0]])

	# Print performances against specified teams
	print
	print su.center("=========================================")
	print su.center("PERFORMANCES AGAINST SPECIFIED TEAMS")
	print su.center("=========================================")

	print
	for avg in sortedAverages:
		listT = su.getStatsAgainstTeam(avg[0], oppTeamNames[avg[0]])
		#print su.center("/// " + oppTeamNames[avg[0]].upper() + " Adjusted Defensive Ranking: " + str(su.getAdjDefRanking(oppTeamNames[avg[0]])) + " \\\\\\")
		if len(listT) == 0:
			print su.center("=====" + avg[0].upper() + "=====")
			print su.center("Player did not play " + oppTeamNames[avg[0]].upper() + "\n")
		else:
			su.printStats(listT)
