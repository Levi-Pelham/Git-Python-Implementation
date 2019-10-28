# Git-Python Implementation 
# Levi Pelham - a1695061
# Secure Software Engineering Exercise 2

import os, operator, calendar
from git import Repo
from datetime import date

paths = []		#global list to store the file paths from the commit to the VCC commits

def main():
	repositories = ['tomcat', 'spring-framework', 'camel', 'cxf-fediz', 'lucene-solr', 'jolokia']
	commits = ['913d94b289e056107e521dbab8e79cc72a62a33','7576274874deeccb6da6b09a8d5bd62e8b5538b7','ccf149c76bf37adc5977dc626e141a14e60b5aee', 'ccdb12b26ff89e0a998a333e84dd84bd713ac76', '02c693f3713add1b4891cbaa87127de3a55c10f','5895d5c137c335e6b473e9dcb9baf748851bbc5f']
	vcc = ['4b6bbff0cf9', 'ed3823b045f', '0936806dca8', '8fe5f0045', '4eb362c0b36', '99346b3c3']

	selected = 4		#Used to select the respository and commit above.

	git = Repo(repositories[selected]).git 		#create a new repository.
	
	# searchvcc(vcc[selected], git, '+')		#Initialise modified paths in the commit
	
	# vcca(commits[selected], git, None)		# Questions 1-3 of thje assignment
	# vccb(commits[selected], git, None)
	# vccc(commits[selected], git, None)

	vcctask5(commits[selected], git)

	# a(vcc[selected], git)			# Exercise 2 questions modifed to accomodate the new VCC format
	# b(vcc[selected], git, 0)
	# c(vcc[selected], git)
	# d(vcc[selected], git)
	# e(vcc[selected], git)
	# f(vcc[selected], git)
	# g(vcc[selected], git)
	# h(vcc[selected], git)
	# i(vcc[selected], git)
	# j(vcc[selected], git)
	# k(vcc[selected], git)

# -------------------------------------------------- VCC identification -----------------------------------------------------

def checkPaths(commit, repository, t):
	counts = []

	if len(paths) > 5:		#find 5 most modified files in the commit.
		for i in paths:
			count = 0
			for lines in repository.show(commit, '--', i).split('\n'):
				if lines.startswith(t):						# Additions or deletions
					if not lines.startswith(t+t):		# Is not a file 
								count += 1
								continue
			counts.append((i,count))
		counts.sort(key = operator.itemgetter(1), reverse = True)		# Sort tuples by count
		paths.clear()
		
		for k in range(5): 
			paths.append(counts[k][0])

		set(paths)

def searchvcc(commit, repository, t):		#Helper function for searching for additions and deletions
	arr = []
	index = 5
	for lines in repository.show(commit).split('\n'):
		if lines.startswith(t):						# Additions or deletions
			lines = lines[1:]
			if lines.startswith(t+t):		# Is a file
				if lines[4] != '/':
					index = 5				#dev/null case
				paths.append(lines[index:])
			elif len(lines.strip()) != 0:	# Is not a blank line
				while lines[0] == ' ':		# Remove leading white space
					lines = lines[1:]
				arr.append(lines)
	checkPaths(commit, repository, t)
	return arr

def vcca(commit, repository, para):		
	print("\033[1;32;40mLatest Commit of Deleted Lines:\033[0;37;40m")
	dels = searchvcc(commit, repository, '-')
	for files in set(paths):												# For every file affected by the commit
		if files.find("null") == -1 and len(files.strip()) != 0:	# If path is not dev/null or blank
			for deletions in dels:									# For every deleted line in the file
				for lines in repository.blame(para, commit+'^', "--", files).split('\n'):	#for each line in the blame log 
					if len(dels) > 0 and lines.find(deletions) != -1:
						print(lines[:12].strip() + ' ' + deletions.strip())			# extract the commit from the result
	paths.clear()

def vccb(commit, repository, para):
	searchvcc(commit, repository, '+')
	print("\033[1;32;40mScope Of Added Lines:\033[0;37;40m")
	
	for files in paths:
		scope = " Global"												# If there is no presented scope, global
		if files.find("null") == -1 and len(files.strip()) != 0:
			for lines in repository.show(commit, '--', files).split('\n'):				# If a scope is found at the end of the line
				if lines.find('{') != -1 and lines.find('{') == len(lines)-1 and len(lines[1:].strip()) != 0:
					if len(lines) == 1:
						scope = saved
					else:
						scope = lines
				
				if lines.startswith('+') and not lines.startswith('+++'):	# If line is an addition and not a file
					for comms in repository.blame(para, commit, "--", files).split('\n'):	#for each line in the blame log
						if comms.find(lines[1:]) != -1: 
							print(comms[:12], scope[1:].strip(), "\033[1;35;40m", lines[1:].strip(),"\033[0;37;40m")
							break
				saved = lines

def vccc(commit, repository, para):
	print("\033[1;32;40mFrequent Commits Of File:\033[0;37;40m")	
	vccs, result = [], []
	searchvcc(commit, repository, '+')	

	for files in set(paths):												
		for lines in repository.blame(para, commit, '--', files).split('\n'):	# For each possible VCC in the current commit
			vccs.append(lines[:11])									
	
	for item in set(vccs):												# For each potential VCC
		temp = (item,vccs.count(item))									# Store the commit and the count in a tuple 
		result.append(temp)	

		result.sort(key = operator.itemgetter(1), reverse = True)		# Sort tuples by count
	
	for x in range(5):
		print(result[x])

	paths.clear()

def vcctask5(commit, repository):
	print("\033[1;32;40mGit Blame Parameter Testing:\033[0;37;40m")
	parameters = ['-w', '-wM', '-wC', '-wCC', '–wCCC']
 
	for p in parameters:
		print("\033[1;32;40m",p,"\033[0;37;40m")
		# vcca(commit, repository, p)		
		# vccb(commit, repository, p)	
		vccc(commit, repository, p)

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
	print("\033[1;32;40mCommit message:\033[0;37;40m")
	count = 0
	searchvcc(commit, repository, '+')
	for lines in repository.log(commit, "-n 1").split('\n'):		#Iterate over the lines in the commit log and return the message
		if count > 3:
			print(lines.strip())
		count += 1

def b(commit, repository, flag):	#Helper function for returning number of files affected by the commit
	count = 0
	tempFiles = []
	for lines in repository.show(commit).split('\n'):	
		if lines.startswith('+++'):						#Find the number of files altered by the commit
			count += 1
			tempFiles.append(lines[6:])
	
	if flag == 0:		
		print("\033[1;32;40mFiles Affected By Commit :\033[0;37;40m")
		print(count)

	return tempFiles

def c(commit, repository):
	print("\033[1;32;40mRepositories Affected By Commit :\033[0;37;40m")
	count = 0
	files = list()
	for lines in repository.show(commit).split('\n'):
		if lines.startswith('+++'):						#If file
			while lines[-1] is not '/':					#Remove file from path
				lines = lines[:-1]
			files.append(lines)
	print(len(set(files)))								#Remove duplicate paths to leave the unique count

def d(commit, repository):		
	print("\033[1;32;40mTotal Lines Deleted :\033[0;37;40m")
	searchLines(commit, repository,'-', 0)

def e(commit, repository):
	print("\033[1;32;40mTotal Lines Added :\033[0;37;40m")
	searchLines(commit, repository,'+', 0)

def f(commit, repository):
	print("\033[1;32;40mTotal Lines Deleted (no spaces/comments) :\033[0;37;40m")	#Flagged 1 to indicate no spaces or comments
	searchLines(commit, repository,'-', 1)

def g(commit, repository):
	print("\033[1;32;40mTotal Lines Added (no spaces/comments) :\033[0;37;40m")
	searchLines(commit, repository,'+', 1)

def h(commit, repository):
	print("\033[1;32;40mDays Between Current And Previous Commits :\033[0;37;40m")
	data = [-1]
	cal = {mon: num for num,mon in enumerate(calendar.month_abbr)}		#Used to differentiate between months in string and integer form
	
	for i in paths:
		revisions = []
		for lines in repository.log('-n 2','--follow', '--', i).split('\n'):
			if lines.startswith("Date:"):										#Find the date of the commit
				data = lines.split(' ')
				day = data[5]
				month = cal[data[4]]
				year = data[7]
				revisions.append(date(int(year),int(month),int(day)))			#Turn date information into date format to calculate difference
		print(i)

		if len(revisions) > 1:
			print(abs(revisions[0] - revisions[1]))

		else:
			print("No modifications after initial commit for file.")

def i(commit, repository):
	print("\033[1;32;40mNumber Of Modifications To File :\033[0;37;40m")		
	
	for i in paths:							#For each file, count the number of commits 
		count = 0	
		for lines in repository.log('--follow', '--', i).split('\n'):
			if lines.startswith("commit"):
				count += 1
		print(i + " : " + str(count))
	
def j(commit, repository):
	print("\033[1;32;40mDevelopers That Have Altered The File :\033[0;37;40m")
	
	for i in paths:
		authors = []
		for lines in repository.log('--follow', '--', i).split('\n'):		#For each file, count the authors and remove duplicates
			if lines.startswith("Author:"):
				authors.append(lines)
		print(i)
		for index in set(authors):
			print(index)
		print('\n')

def k(commit, repository):
	print("\033[1;32;40mTotal Commits Made By Each Developer :\033[0;37;40m")					#Use shortlog to count the total number of commits of each author
	for lines in repository.shortlog().split('\n'):
		if lines.find("):") != -1 and not lines.startswith(" "):
			print(lines.strip())

main()
