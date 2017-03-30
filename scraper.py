# Scrapes data from set source for a given player

from lxml import html
from lxml import etree
import requests
import private

# playerName should be in format: "Firstname Lastname"
# Example: "Lebron James"

# Globals:
headerFile = private.headerFile
startOfRow = private.startOfRow
endOfRow = private.endOfRow

def condensePage(page):
	indexOfStart = page.find(startOfRow)
	indexOfEnd = page.rfind(endOfRow)
	return page[indexOfStart:indexOfEnd]

def getStatsForPlayer(playerName, year):
	num = 1
	nameArr = playerName.split(' ')
	firstName = nameArr[0].lower()
	lastName = nameArr[1].lower()
	if (len(nameArr) > 2):
		num = int(nameArr[2])

	foundPlayer = False
	keepLooping = True
	# Retrieve the HTML page in a condensed form
	while foundPlayer == False:
		urlStr = private.getURL(firstName, lastName, year, "0" + str(num))
		try:
			condensedPage = condensePage(requests.get(urlStr).content)
		except requests.exceptions.ConnectionError:
			print "Cannot Connect.\n"
			exit()
		try:
			tree = html.fromstring(condensedPage)
		except etree.XMLSyntaxError:
			num+=1
			if num == 5:
				print "Player " + playerName.upper() + " Not Found.\n"
				exit()
		else:
			foundPlayer = True


	# Retrieve the two forms of headers 
	file = open(headerFile)
	tableHeadersStr = file.readline()
	dataStatsStr = file.readline();
	tableHeaders = tableHeadersStr.replace(" ", "").strip().split(',')
	dataStats = dataStatsStr.replace(" ", "").strip().split(',')

	gameStats = []

	# Get number of games
	tempPath = private.getInitialPath(dataStats[0])
	numGames = len(tree.xpath(tempPath))

	# Traverse through games and retrieve all data
	lastIndex = 0
	rk = 1
	for count in range(0, numGames):
		dict = {}
		i = 0
		if condensedPage.find(startOfRow, lastIndex+len(startOfRow)) == -1:
			thisRow = condensedPage[lastIndex:]
		else:
			thisRow = condensedPage[lastIndex:condensedPage.find(startOfRow, lastIndex+len(startOfRow))]
		lastIndex = condensedPage.find(startOfRow, lastIndex+len(startOfRow))
		tree = html.fromstring(thisRow)
		for datastat in dataStats:
			if (datastat == 'ranker'):
				thisData = [str(rk)]
			else:
				xpathStr = private.getPath(datastat)
				thisData = tree.xpath(xpathStr)
			if (len(thisData) == 1):
				dict[tableHeaders[i]] = thisData[0]
			else:
				dict[tableHeaders[i]] = "N/A"
			i+=1
		dict['NAME'] = playerName.upper() # provides easy access to player's name
		dict['TITLE'] = "" # for titling purposes
		gameStats.append(dict)
		rk+=1

	#for s in gameStats:
	#	print s
	#	print
	return gameStats

def getAbbrevFromFullTeamName(fullTeamName):
	if fullTeamName == 'San Antonio Spurs':
		return 'SAS'
	elif fullTeamName == 'Golden State Warriors':
		return 'GSW'
	elif fullTeamName == 'Utah Jazz':
		return 'UTA'
	elif fullTeamName == 'Atlanta Hawks':
		return 'ATL'
	elif fullTeamName == 'Memphis Grizzlies':
		return 'MEM'
	elif fullTeamName == 'New Orleans Pelicans':
		return 'NOP'
	elif fullTeamName == 'Detroit Pistons':
		return 'DET'
	elif fullTeamName == 'Miami Heat':
		return 'MIA'
	elif fullTeamName == 'Dallas Mavericks':
		return 'DAL'
	elif fullTeamName == 'Oklahoma City Thunder':
		return 'OKC'
	elif fullTeamName == 'Charlotte Hornets':
		return 'CHO'
	elif fullTeamName == 'Chicago Bulls':
		return 'CHI'
	elif fullTeamName == 'Los Angeles Clippers':
		return 'LAC'
	elif fullTeamName == 'Houston Rockets':
		return 'HOU'
	elif fullTeamName == 'Washington Wizards':
		return 'WAS'
	elif fullTeamName == 'Philadelphia 76ers':
		return 'PHI'
	elif fullTeamName == 'Boston Celtics':
		return 'BOS'
	elif fullTeamName == 'Indiana Pacers':
		return 'IND'
	elif fullTeamName == 'Toronto Raptors':
		return 'TOR'
	elif fullTeamName == 'Milwaukee Bucks':
		return 'MIL'
	elif fullTeamName == 'Orlando Magic':
		return 'ORL'
	elif fullTeamName == 'Cleveland Cavaliers':
		return 'CLE'
	elif fullTeamName == 'Minnesota Timberwolves':
		return 'MIN'
	elif fullTeamName == 'Sacramento Kings':
		return 'SAC'
	elif fullTeamName == 'Brooklyn Nets':
		return 'BRK'
	elif fullTeamName == 'Phoenix Suns':
		return 'PHO'
	elif fullTeamName == 'New York Knicks':
		return 'NYK'
	elif fullTeamName == 'Portland Trail Blazers':
		return 'POR'
	elif fullTeamName == 'Los Angeles Lakers':
		return 'LAL'
	elif fullTeamName == 'Denver Nuggets':
		return 'DEN'

def getTeamRatings():
	urlStr = private.getTeamRatingsURL()
	try:
		condensedPage = condensePage(requests.get(urlStr).content)
	except requests.exceptions.ConnectionError:
		print "Cannot Connect.\n"
		exit()
	tree = html.fromstring(condensedPage)

	# Retrieve the two forms of headers 
	file = open(headerFile)
	file.readline()
	file.readline()
	tableHeadersStr = file.readline()
	dataStatsStr = file.readline();
	tableHeaders = tableHeadersStr.replace(" ", "").strip().split(',')
	dataStats = dataStatsStr.replace(" ", "").strip().split(',')

	teamStats = {}
	numTeams = 30

	# Traverse through teams and retrieve all data
	lastIndex = 0
	rk = 1
	for count in range(0, numTeams):
		dict = {}
		i = 0
		if condensedPage.find(startOfRow, lastIndex+len(startOfRow)) == -1:
			thisRow = condensedPage[lastIndex:]
		else:
			thisRow = condensedPage[lastIndex:condensedPage.find(startOfRow, lastIndex+len(startOfRow))]
		lastIndex = condensedPage.find(startOfRow, lastIndex+len(startOfRow))
		tree = html.fromstring(thisRow)
		teamName = "NONAME"
		for datastat in dataStats:
			if (datastat == 'ranker'):
				thisData = [str(rk)]
			else:
				xpathStr = private.getPath(datastat)
				thisData = tree.xpath(xpathStr)
			if (len(thisData) == 1):
				dict[tableHeaders[i]] = thisData[0]
			else:
				dict[tableHeaders[i]] = "N/A"
			i+=1
		teamName = dict['Team']
		teamStats[getAbbrevFromFullTeamName(teamName)] = dict
		rk+=1

	#print teamStats['GSW']['ORtg']
	return teamStats










