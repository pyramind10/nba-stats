# Continuous loop that prompts for a player and the player's
# opposing team. Prints out stats for last five games played
# as well as performance against the specified team.
# To exit loop, use 'exit'

import statutilities
from statutilities import center

while True:
	person = raw_input("Enter player name (exit to quit): ")
	if (person == 'exit'):
		break
	opp = raw_input("Enter opposing team name: ").upper()
	numGames = int(raw_input("Enter # of recent games: "))

	statutilities.printStats(statutilities.getStatsForLastNGames(person, numGames))
	listT = statutilities.getStatsAgainstTeam(person, opp)
	#print center("/// " + opp.upper() + " Adjusted Defensive Ranking: " + str(statutilities.getAdjDefRanking(opp)) + " \\\\\\")
	if (len(listT) == 0):
		print "Player has not played this team."
		print
	else:
		statutilities.printStats(listT)
	print center("==========================")
	print