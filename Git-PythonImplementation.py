# Git-Python Implementation 
# Levi Pelham - a1695061
# Secure Software Engineering Exercise 2

import os, calendar
from git import Repo
from datetime import date

def breakpoint(): 
	print("---------------------------------------------------------------------------------------------------------------------------------------------------")

def main():
	repositories = ['tomcat', 'spring-framework', 'camel']
	commits = ['913d94b289e056107e521dbab8e79cc72a62a33','7576274874deeccb6da6b09a8d5bd62e8b5538b7','ccf149c76bf37adc5977dc626e141a14e60b5aee']
		
	while(1):
		print('Tomcat (0)\nSpring-Framework (1)\nCamel (2)\nEXIT (9)\n\nEnter Repository above.\n')
		inp = input()
		args = inp.split(' ')
		if args[0] == '9':
			return
		git = Repo(repositories[int(args[0])]).git 		#create a new repository.
		commands(commits[int(args[0])], git)			#send command line arguments to the switcher below

def commands(x, res):		#switcher to individually select questions
	switcher={
		97: a(x, res),
		98: b(x, res, 0),
		99: c(x, res),
		100: d(x, res),
		101: e(x, res),
		102: f(x, res),
		103: g(x, res),
		104: h(x, res),
		105: i(x, res),
		106: j(x, res),
		107: k(x, res)
			}

def searchLines(commit, repository, term, flag):		#helper function for searching for additions and deletions
	count = 0
	count2 = 0
	if term is '+': 
		term2 = '+++'
	else:
		term2 = '---'

	for lines in repository.show(commit).split('\n'):
		if lines.startswith(term):						# additions or deletions
			if not lines.startswith(term2):		# is not a file 
					if flag == 0:
						count += 1
						continue
					else:  
						lines = lines[1:]
						if len(lines.strip()) != 0 and lines.find("*") == -1 and lines.find("//") == -1 and lines.find("<!-") == -1:	#remove comments and spaces from the count
							count2 += 1
	if flag == 0:					
		print(count)
	else:
		print(count2)
	return

def a(commit, repository):
	print("Fixing Commit Information :")
	for lines in repository.show(commit).split('\n'):	#show the commit information and message
		if lines.startswith('diff'):
			return 
		else:
			print(lines)
	breakpoint()

def b(commit, repository, flag):	#helper function for returning number of files affected by the commit
	count = 0
	tempFiles = []
	for lines in repository.show(commit).split('\n'):	
		if lines.startswith('+++'):						#find the number of files altered by the commit
			count += 1
			tempFiles.append(lines[6:])
	
	if flag == 0:		
		print("Files Affected By Commit :")
		print(count)
		breakpoint()

	return tempFiles

def c(commit, repository):
	print("Repositories Affected By Commit :")
	count = 0
	files = list()
	for lines in repository.show(commit).split('\n'):
		if lines.startswith('+++'):						#if file
			while lines[-1] is not '/':					#remove file from path
				lines = lines[:-1]
			files.append(lines)
	print(len(set(files)))								#remove duplicate paths to leave the unique count
	breakpoint()
	return 

def d(commit, repository):		
	print("Total Lines Deleted :")
	searchLines(commit, repository,'-', 0)
	breakpoint()

def e(commit, repository):
	print("Total Lines Added :")
	searchLines(commit, repository,'+', 0)
	breakpoint()

def f(commit, repository):
	print("Total Lines Deleted (no spaces/comments) :")	#flagged 1 to indicate no spaces or comments
	searchLines(commit, repository,'-', 1)
	breakpoint()

def g(commit, repository):
	print("Total Lines Added (no spaces/comments) :")
	searchLines(commit, repository,'+', 1)
	breakpoint()

def h(commit, repository):
	print("Days Between Current And Previous Commits :")
	data = [-1]
	cal = {mon: num for num,mon in enumerate(calendar.month_abbr)}		#used to differentiate between months in string and integer form
	modifiedFiles = b(commit, repository, 1)
	
	for i in modifiedFiles:
		revisions = []
		for lines in repository.log('-n 2','--follow', '--', i).split('\n'):
			if lines.startswith("Date:"):										#find the date of the commit
				data = lines.split(' ')
				day = data[5]
				month = cal[data[4]]
				year = data[7]
				revisions.append(date(int(year),int(month),int(day)))			#turn date information into date format to calculate difference
		print(i)
		print(revisions[0] - revisions[1])
	
	breakpoint()
	return 

def i(commit, repository):
	print("Number Of Modifications Of File :")		
	modifiedFiles = b(commit, repository, 1)
	
	for i in modifiedFiles:							#for each file, count the number of commits 
		print(i)
		count = 0	
		for lines in repository.log('--follow', '--', i).split('\n'):
			if lines.startswith("commit"):
				count += 1
		print(count)
	
	breakpoint()
	return

def j(commit, repository):
	print("Developers That Have Altered The File :")
	modifiedFiles = b(commit, repository, 1)
	
	for i in modifiedFiles:
		authors = []
		for lines in repository.log('--follow', '--', i).split('\n'):		#for each file, count the authors and remove duplicates
			if lines.startswith("Author:"):
				authors.append(lines)
		print(i)
		for index in set(authors):
			print(index)
		print('\n')
	
	breakpoint()
	return

def k(commit, repository):
	print("Total Commits Made By Each Developer :")					#use shortlog to count the total number of commits of each author
	for lines in repository.shortlog().split('\n'):
		if lines.find("):") != -1 and not lines.startswith(" "):
			print(lines)

	breakpoint()
	return

main()

