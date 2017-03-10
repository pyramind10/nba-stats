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
	print
	title = "=========" + person.upper() + "========="
	print center(title)
	print
	print center("--LAST FIVE GAMES--")
	statutilities.printStats(statutilities.getStatsForLastNGames(person, 5))
	print center("--PERFORMANCE AGAINST " + opp + "--")
	listT = statutilities.getStatsAgainstTeam(person, opp)
	if (len(listT) == 0):
		print "Player has not played this team."
		print
	else:
		statutilities.printStats(statutilities.getStatsAgainstTeam(person, opp))
	print center("==========================")
	print