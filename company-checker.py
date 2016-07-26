from bs4 import BeautifulSoup
import webbrowser, requests

choicearray = []

def File():
	pdf = 0
	print("AA = Annual Accounts")
	print("AR01 = Annual Return")
	print("etc...")
	pdf = input("What form do you want to see? ")
	fdo = pdf.upper()
	url = ("https://beta.companieshouse.gov.uk/company/"+compno+"/filing-history?page=1")
	r  = requests.get(url)
	data = r.text
	soup = BeautifulSoup(data, "html.parser")
	listy = []
	for link in soup.find_all('tr'):
		txt = str(link)
		if fdo in txt: 
			for link in link.find_all('a'):
				lonk = link.get('href')
				listy.append(lonk)
	if len(listy) <= 0:
		url=("https://beta.companieshouse.gov.uk/company/"+compno+"/filing-history?page=2")
		r  = requests.get(url)
		data = r.text
		soup = BeautifulSoup(data, "html.parser")
		listy = []
		for link in soup.find_all('tr'):
			txt = str(link)
			if fdo in txt: 
				for link in link.find_all('a'):
					lonk = link.get('href')
					listy.append(lonk)				
		if len(listy) <= 0:
			print("Sorry, no "+fdo+" found!")
		else:
			webbrowser.open_new_tab("https://beta.companieshouse.gov.uk"+listy[0])						
	else:
		webbrowser.open_new_tab("https://beta.companieshouse.gov.uk"+listy[0])
					
def Report():
	f1 = open("report "+compno+".txt", "w")
	#find name
	url = ("https://beta.companieshouse.gov.uk/company/"+compno )
	r  = requests.get(url)
	data = r.text
	soup = BeautifulSoup(data, "html.parser")
	for link in soup.find_all('p', id="company-name"):
		summer = link.contents[0]
		f1.write("=== "+summer+" ===")
	f1.write("\n")
	#find registered office		
	url = ("https://beta.companieshouse.gov.uk/company/"+compno )
	r  = requests.get(url)
	data = r.text
	soup = BeautifulSoup(data, "html.parser")
	for link in soup.find_all('dl'):
		string = str(link)
		if "id=" not in string:
			f1.write(link.find('dd').contents[0])
	f1.write("\n\n")
	#find company status
	url = ("https://beta.companieshouse.gov.uk/company/" +compno )
	r  = requests.get(url)
	data = r.text
	soup = BeautifulSoup(data, "html.parser")
	for link in soup.find_all('dl'):
		string = str(link)
		if "status" in string:
			winter = (link.find('dd').contents[0])
			spring = str(winter)
			f1.write("Status: "+spring[17:])
	f1.write("\n")
	#find company type
	url = ("https://beta.companieshouse.gov.uk/company/" +compno )
	r  = requests.get(url)
	data = r.text
	soup = BeautifulSoup(data, "html.parser")
	for link in soup.find_all('dl'):
		string = str(link)
		if "company-type" in string:
			summer = (link.find('dd').contents[0])
			autumn = str(summer)
			f1.write("Type: "+autumn[17:])
	f1.write("\n")
	#find incorporation date
	url = ("https://beta.companieshouse.gov.uk/company/" +compno )
	r  = requests.get(url)
	data = r.text
	soup = BeautifulSoup(data, "html.parser")
	for link in soup.find_all('dl'):
		string = str(link)
		if "creation" in string:
			f1.write("Incorporated: "+link.find('dd').contents[0])
	f1.write("\n\n")
	#print director name
	f1.write("-Directors-\n\n")
	url = ("https://beta.companieshouse.gov.uk/company/" +compno+"/officers")
	r  = requests.get(url)
	data = r.text
	soup = BeautifulSoup(data, "html.parser")
	for link in soup.find_all('a'):
		string = str(link)
		if "appointment" in string:
			f1.write(link.contents[0]+"\n")
	print("Report generated!")
	webbrowser.open('report '+compno+'.txt')

compno = input("Enter your company number or [S] for search: ")
if compno == "s" or compno == "S":
	query = input("Search company name: ")
	print()
	compurl = ("https://beta.companieshouse.gov.uk/search/companies?q="+query)
	r  = requests.get(compurl)
	data = r.text
	soup = BeautifulSoup(data, "html.parser")
	n = 0
	for link in soup.find_all('a'):
		namelist = []
		linktest = str(link)
		if 'SearchSuggestions' in linktest and 'strong' in linktest:
			#print(linktest)
			n = (n+1)
			linkdf = (link.get('href'))
			choicearray.append(linkdf)
			number = len(link)
			#number = int(number)
			num = 0
			for i in range(number):
				namepart = str(link.contents[num])
				num = num+1
				namepartstrip1 = namepart.replace("<strong>","")
				namepartstrip2 = namepartstrip1.replace("</strong>","")
				namepartstrip2 = namepartstrip2.strip()
				namestructured = namepartstrip2+' '
				namelist.append(namestructured)
#			namepart1 = namepart1[:-9]
#			namepart1 = namepart1[8::]
			companyname = ''.join(namelist)
			print(n,'- '+companyname),
		elif 'SearchSuggestions' in linktest:
			n = (n+1)
			linkdf = (link.get('href'))
			choicearray.append(linkdf)
			name = str(link.contents[0])
			names = name.strip()
			print(n, '- '+names)
			
	selection = int(input('Enter the number of your choice: '))
	print()
	selectionn = selection - 1
	selectionnn = choicearray[selectionn]
	cutter = selectionnn[9::]
	print('Company number:'+' '+cutter)
	print()
	compno = cutter
	
loop = True
while loop == True:
	choice = input("Generate a report [R] or obtain a File [F]: ")
	if choice == "r" or choice == "R":
		Report()
		retry = input("[Q] to quit or [Enter] to run again: ")
		if retry == "Q" or quiz == "q":
			loop = False
			quit()
	elif choice == "f" or choice == "F":
		File()
		retry = input("[Q] to quit or [Enter] to run again: ")
		if retry == "Q" or quiz == "q":
			loop = False
			quit()

