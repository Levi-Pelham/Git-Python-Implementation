# Git-Python Implementation 
# Levi Pelham - a1695061
# Secure Software Engineering Exercise 3

import os, operator, calendar
from git import Repo
from datetime import date

paths = []

def main():
	repositories = ['tomcat', 'spring-framework', 'camel']
	commits = ['913d94b289e056107e521dbab8e79cc72a62a33','7576274874deeccb6da6b09a8d5bd62e8b5538b7','ccf149c76bf37adc5977dc626e141a14e60b5aee']
	vcc = ['4b6bbff0cf9', 'ed3823b045f', '0936806dca8']

	selected = 1;
	
	git = Repo(repositories[selected]).git 		#create a new repository.

	vcca(vcc[selected], git)
	vccb(vcc[selected], git)
	vccc(vcc[selected], git)

	a(vcc[selected], git)
	b(vcc[selected], git, 0)
	c(vcc[selected], git)
	d(vcc[selected], git)
	e(vcc[selected], git)
	f(vcc[selected], git)
	g(vcc[selected], git)
	h(vcc[selected], git)
	i(vcc[selected], git)
	j(vcc[selected], git)

# -------------------------------------------------- VCC identification -----------------------------------------------------

def searchvcc(commit, repository, t, t2):		#Helper function for searching for additions and deletions
	arr = []
	for lines in repository.show(commit).split('\n'):
		if lines.startswith(t):						# Additions or deletions
			lines = lines[1:]
			if lines.startswith(t2):		# Is a file
				paths.append(lines[5:])
			elif len(lines.strip()) != 0:	# Is not a blank line
				while lines[0] == ' ':		# Remove leading white space
					lines = lines[1:]
				arr.append(lines)
	return arr

def vcca(commit, repository):		
	print("\033[1;33;40mLatest Commit of Deleted Lines:\033[0;37;40m")
	dels = searchvcc(commit, repository, '-', '--')
	
	for files in paths:												# For every file affected by the commit
		if files.find("null") == -1 and len(files.strip()) != 0:	# If path is not dev/null or blank
			for deletions in dels:									# For every deleted line in the file
				for lines in repository.blame(commit+'^', "--", files).split('\n'):	#for each line in the blame log 
					if len(dels) > 0 and lines.find(deletions) != -1:
						print(lines[:12] + ' ' + deletions)			# extract the commit from the result
	paths.clear()

def vccb (commit, repository):
	scope = 'Global'												# If there is no presented scope, global
	print("\033[1;33;40mScope Of Added Lines:\033[0;37;40m")
	for lines in repository.show(commit).split('\n'):				# If a scope is found at the end of the line
		if lines.find('{') == len(lines)-1: 
			scope = lines
		if lines.startswith('+') and not lines.startswith('+++'):	# If line is an addition and not a file
			print(scope)

def vccc (commit, repository):
	print("\033[1;33;40mFrequent Commits Of File:\033[0;37;40m")	
	vccs, result = [], []
	searchvcc(commit, repository, '+', '++')	
	
	for files in paths:												
		for lines in repository.blame(commit, '--', files).split('\n'):	# For each possible VCC in the current commit
			vccs.append(lines[:11])									
	
	for item in set(vccs):												# For each potential VCC
		temp = (item,vccs.count(item))									# Store the commit and the count in a tuple 
		result.append(temp)	

		result.sort(key = operator.itemgetter(1), reverse = True)		# Sort tuples by count
	
	for counts in result:
		print(counts)

# -------------------------------------------------- VCC details -----------------------------------------------------


def searchLines(commit, repository, term, flag):		#Helper function for searching for additions and deletions
	count = 0
	count2 = 0
	if term is '+': 
		term2 = '+++'
	else:
		term2 = '---'

	for lines in repository.show(commit).split('\n'):
		if lines.startswith(term):						# Additions or deletions
			if not lines.startswith(term2):		# Is not a file 
					if flag == 0:
						count += 1
						continue
					else:  
						lines = lines[1:]
						if len(lines.strip()) != 0 and lines.find("*") == -1 and lines.find("//") == -1 and lines.find("<!-") == -1:	#Remove comments and spaces from the count
							count2 += 1
	if flag == 0:							# If flag = 0, return file count. else return line count		
		print(count)
	else:
		print(count2)

def a (commit, repository):
	count = 0
	for lines in repository.log(commit, "-n 1").split('\n'):		#Iterate over the lines in the commit log and return the message
		if count > 3:
			print(lines)
		count += 1

def b(commit, repository, flag):	#Helper function for returning number of files affected by the commit
	count = 0
	tempFiles = []
	for lines in repository.show(commit).split('\n'):	
		if lines.startswith('+++'):						#Find the number of files altered by the commit
			count += 1
			tempFiles.append(lines[6:])
	
	if flag == 0:		
		print("\033[1;33;40mFiles Affected By Commit :\033[0;37;40m")
		print(count)

	return tempFiles

def c(commit, repository):
	print("\033[1;33;40mRepositories Affected By Commit :\033[0;37;40m")
	count = 0
	files = list()
	for lines in repository.show(commit).split('\n'):
		if lines.startswith('+++'):						#If file
			while lines[-1] is not '/':					#Remove file from path
				lines = lines[:-1]
			files.append(lines)
	print(len(set(files)))								#Remove duplicate paths to leave the unique count

def d(commit, repository):		
	print("\033[1;33;40mTotal Lines Deleted :\033[0;37;40m")
	searchLines(commit, repository,'-', 0)

def e(commit, repository):
	print("\033[1;33;40mTotal Lines Added :\033[0;37;40m")
	searchLines(commit, repository,'+', 0)

def f(commit, repository):
	print("\033[1;33;40mTotal Lines Deleted (no spaces/comments) :\033[0;37;40m")	#Flagged 1 to indicate no spaces or comments
	searchLines(commit, repository,'-', 1)

def g(commit, repository):
	print("\033[1;33;40mTotal Lines Added (no spaces/comments) :\033[0;37;40m")
	searchLines(commit, repository,'+', 1)

def h(commit, repository):
	print("\033[1;33;40mDays Between Current And Previous Commits :\033[0;37;40m")
	data = [-1]
	cal = {mon: num for num,mon in enumerate(calendar.month_abbr)}		#Used to differentiate between months in string and integer form
	modifiedFiles = b(commit, repository, 1)
	
	for i in modifiedFiles:
		revisions = []
		for lines in repository.log('-n 2','--follow', '--', i).split('\n'):
			if lines.startswith("Date:"):										#Find the date of the commit
				data = lines.split(' ')
				day = data[5]
				month = cal[data[4]]
				year = data[7]
				revisions.append(date(int(year),int(month),int(day)))			#Turn date information into date format to calculate difference
		print(i)
		print(abs(revisions[0] - revisions[1]))

def i(commit, repository):
	print("\033[1;33;40mNumber Of Modifications To File :\033[0;37;40m")		
	modifiedFiles = b(commit, repository, 1)
	
	for i in modifiedFiles:							#For each file, count the number of commits 
		count = 0	
		for lines in repository.log('--follow', '--', i).split('\n'):
			if lines.startswith("commit"):
				count += 1
		print(i + " : " + str(count))
	
def j(commit, repository):
	print("\033[1;33;40mDevelopers That Have Altered The File :\033[0;37;40m")
	modifiedFiles = b(commit, repository, 1)
	
	for i in modifiedFiles:
		authors = []
		for lines in repository.log('--follow', '--', i).split('\n'):		#For each file, count the authors and remove duplicates
			if lines.startswith("Author:"):
				authors.append(lines)
		print(i)
		for index in set(authors):
			print(index)
		print('\n')

def k(commit, repository):
	print("\033[1;33;40mTotal Commits Made By Each Developer :\033[0;37;40m")					#Use shortlog to count the total number of commits of each author
	for lines in repository.shortlog().split('\n'):
		if lines.find("):") != -1 and not lines.startswith(" "):
			print(lines)

main()
