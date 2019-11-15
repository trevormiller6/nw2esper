"""Simple APP USED TO PULL EVENTS FROM NETWITNESS WITH API AND MODIFY THE OUTPUT IN THE FORMAT NEEDED FOR THE ESPER TRYOUT PAGE."""

import os
import re
import json
import time
import platform
import webbrowser
import threading
import shutil
from tkinter import messagebox as tkMessageBox
from tkinter import *


class GUI:
	"""MAIN FUNCTIONS FOR GUI OPPERATION."""

	def __init__(self, master):
		"""BUILD GUI."""
		self.master = master
		self.statusText1 = StringVar(root)
		self.statusText = StringVar(root)
		self.statusText2 = StringVar(root)
		self.statusText.set(" \n Fill in Blanks, then press the Get Events button. \n ")
		self.statusText2.set("If you don't want to obfuscate any Meta Keys, leave these blank")

		label = Label(self.master, text="SERVICE\n(http://ipaddress:port) ")
		label.grid(row=1, column=0, sticky=E)
		self.entry = Entry(self.master, width=100)
		self.entry.insert(0, "http://10.10.10.10:50103")
		self.entry.grid(row=1, column=1, ipadx=3, ipady=3, padx=15, pady=5)

		label3 = Label(self.master, text="USERNAME")
		label3.grid(row=2, column=0, sticky=E)
		self.entry3 = Entry(self.master, width=100)
		self.entry3.grid(row=2, column=1, ipadx=3, ipady=3, padx=15, pady=5)

		label4 = Label(self.master, text="PASSWORD")
		label4.grid(row=3, column=0, sticky=E)
		self.entry4 = Entry(self.master, show="*", width=100)
		self.entry4.grid(row=3, column=1, ipadx=3, ipady=3, padx=15, pady=5)

		label2 = Label(self.master, text="QUERY")
		label2.grid(row=4, column=0, sticky=E)
		self.entry2 = Entry(self.master, width=100)
		self.entry2.grid(row=4, column=1, ipadx=3, ipady=3, padx=15, pady=5)

		label5 = Label(self.master, text="NAME OF OUTPUT FILE\n(optional)")
		label5.grid(row=5, column=0, sticky=E)
		self.entry5 = Entry(self.master, width=100)
		self.entry5.grid(row=5, column=1, ipadx=3, ipady=3, padx=15, pady=5)

		label6 = Label(self.master, text="META TO OBFUSCATE\n(comma seperated) ")
		label6.grid(row=7, column=0, sticky=E)
		self.entry6 = Entry(self.master, text="comma separated Meta keys", width=100)
		self.entry6.grid(row=7, column=1, ipadx=3, ipady=3, padx=15, pady=5)

		label7 = Label(self.master, text="OBFUSCATION KEY\n(enter random letters) ")
		label7.grid(row=8, column=0, sticky=E)
		self.entry7 = Entry(self.master, width=100)
		self.entry7.grid(row=8, column=1, ipadx=3, ipady=3, padx=15, pady=5)

		"""button_quit = Button(self.master, text="QUIT!", command=self.button_quit_callback, bg = "red")
		button_quit.grid(row=7, column=2, ipadx=3, ipady=3, padx=15, pady=5)"""

		button_New = Button(self.master, text="Delete/Start Over", command=self.button_restart_callback)
		button_New.grid(row=5, column=2, ipadx=3, ipady=3, padx=15, pady=5)

		button_go = Button(self.master, text="Get Events", command=self.go, bg="green")
		button_go.grid(row=2, column=2, ipadx=3, ipady=3, padx=15, pady=5)

		button_Esper = Button(self.master, text="Open Esper Tool", command=self.button_web_callback)
		button_Esper.grid(row=3, column=2, ipadx=3, ipady=3, padx=15, pady=5)

		button_open = Button(self.master, text="Open File with Events", command=self.button_openfile_callback)
		button_open.grid(row=4, column=2, ipadx=3, ipady=3, padx=15, pady=5)

		link = Label(self.master, text="Help?", fg="blue", cursor="hand2", font="bold")
		link.grid(row=0, column=0, sticky=N+W)
		link.bind("<Button-1>", self.readme)

		message = Label(self.master, textvariable=self.statusText)
		message.grid(row=0, column=0, columnspan=3)
		message.configure(font="bold")

		message1 = Label(self.master, textvariable=self.statusText1)
		message1.grid(row=9, column=0, sticky=N+E+S+W, columnspan=3)
		message1.configure(fg="red", font="bold")

		message2 = Label(self.master, textvariable=self.statusText2)
		message2.grid(row=6, column=1, sticky=N+E+S+W)

	def fnobfuscate(self, s, mask):
		"""OBFUSCATE META VALUES."""
		nmask = [ord(c) for c in mask]
		lmask = len(mask)
		return ''.join([chr(ord(c) ^ nmask[i % lmask]) for i, c in enumerate(s)])

	def go(self):
		"""BUTTON TO RUN THE APP."""
		self.service = self.entry.get()
		self.query = self.entry2.get()
		self.username = self.entry3.get()
		self.password = self.entry4.get()
		self.output = self.entry5.get()
		self.bgTask = threading.Thread(target=self.apicallworker, args=[])
		self.bgTask.daemon = True
		self.bgTask.start()

	def apicallworker(self):
		"""PULL EVENTS WITH API."""
		import urllib.request, urllib.error, urllib.parse
		self.statusText1.set('Building Query.')
		if len(self.entry6.get()) <= 1:
			obfuscate = 0
		else:
			obfuscate = self.entry6.get()
			key = self.entry7.get()

		if len(self.service) == 0:
			self.statusText1.set('SERVICE MUST BE SET!')
			return

		rex = re.match(r"(?P<proto>https?)://(?P<service>[^:]+):(?P<port>\d+)", self.service.lower())
		if rex is not None:
			PROTOCOL = rex.group('proto')
			SERVER = rex.group('service')
			PORT = rex.group('port')
		else:
			self.statusText1.set('ERROR WITH SERVICE: ' + self.service.lower() + ' SERVICE MUST BE FORMATTED LIKE: http(s)://ip:port')
			return

		if len(self.query) == 0:
			self.statusText1.set('QUERY MUST BE SET!')
			return
		elif 'time' in self.query:
			myquery = 'select * where ' + self.query
		else:
			self.statusText1.set('Your Query is Missing Time Range')
			return

		if len(self.username) == 0:
			self.statusText1.set('Enter a username')
			return

		if len(self.password) < 2:
			self.statusText1.set('Enter a password')
			return

		if len(self.output) > 0:
			folder = 'events'
			self.out_dir = os.path.join(folder)
			if not os.path.exists(os.path.join(self.out_dir)):
				os.makedirs(os.path.join(self.out_dir))
			self.outputfile = time.strftime(self.output + "_" + "%Y%m%d-%H%M" + ".txt")
			file = open(os.path.join(self.out_dir, self.outputfile), "w+")
			path1 = os.path.join(self.out_dir, self.outputfile)
		else:
			folder = 'events'
			self.out_dir = os.path.join(folder)
			if not os.path.exists(os.path.join(self.out_dir)):
				os.makedirs(os.path.join(self.out_dir))
			self.outputfile = time.strftime("nw2esper_" + "%Y%m%d-%H%M" + ".txt")
			file = open(os.path.join(self.out_dir, self.outputfile), "w+")
			path1 = os.path.join(self.out_dir, self.outputfile)

		if obfuscate:
			metaToobfuscate = obfuscate
			obfuscate = 1
			if len(key) > 0:
				OfKey = key
			else:
				self.statusText1.set('You have to provide a key to obfuscate the results\n')
				return
		else:
			obfuscate = 0

		self.statusText1.set('Building Query...')
		url_password = urllib.request.HTTPPasswordMgrWithDefaultRealm()
		url_password.add_password(None, PROTOCOL + "://" + SERVER + ':' + PORT, self.username, self.password)
		handler = urllib.request.HTTPBasicAuthHandler(url_password)
		opener = urllib.request.build_opener(handler)
		myquery = urllib.parse.quote(myquery)
		urlquery = PROTOCOL + "://" + SERVER + ':' + PORT + '/sdk?msg=query&query=' + myquery + '&force-content-type=application/json'
		LastTime = 0
		mySchemaList = {}
		mySchema = 'CREATE SCHEMA Event('
		myCurrentGroup = 0
		eventsCount = -1

		try:
			self.statusText1.set('Loading Events.')
			site = opener.open(urlquery)
			self.statusText1.set('Loading Events..')
			site = str(site.read(), errors='replace')
			self.statusText1.set('Loading Events...')
			events = json.loads(site)
			self.statusText1.set('Loading Events....')

			if len(events) > 1:
				pass
			else:
				file.close()
				os.remove(path1)
				self.output = 'F'
				path1 = ''
				self.statusText1.set('Your query returned no results!')
				return

			self.statusText1.set('Reformating Events for Esper Tool')
			for event in events:
				try:
					event['string']
				except KeyError:
					self.statusText1.set('Reformating Events for Esper Tool...')
					for MetaData in event['results']['fields']:
						if myCurrentGroup != MetaData['group']:
							myCurrentGroup = MetaData['group']
							if eventsCount == -1:
								eventsCount = 0
							else:
								myEvent = myEvent[:len(myEvent) - 2]
								myEvent = myEvent + '}'
								file.write(myEvent + '\n')

							eventsCount = eventsCount + 1
							myEvent = 'Event={'
						if MetaData['type'] == "time":
							CurrentTime = MetaData['value']
							if LastTime == 0:
								LastTime = CurrentTime
							if CurrentTime != LastTime:
								TimeDelta = CurrentTime - LastTime
								LastTime = CurrentTime
								myEvent = 't=t.plus(' + str(TimeDelta) + ' seconds) \n' + myEvent
						if obfuscate == 1:
							if MetaData['type'].lower() in metaToobfuscate.lower():
								MetaData['value'] = self.fnobfuscate(MetaData['value'], OfKey).encode("hex")
						MetaData['type'] = MetaData['type'].replace('.', '_')
						mySchemaList[MetaData['type']] = MetaData['format']
						if MetaData['format'] == 65:
							separator = '\''
						elif MetaData['format'] == 128:
							separator = "'"
						else:
							separator = ''

						myEvent = myEvent + MetaData['type'] + '=' + separator + str(MetaData['value']) + separator + ', '

			myEvent = myEvent[:len(myEvent) - 2]
			myEvent = myEvent + '}'
			file.write(myEvent + '\n')

			self.statusText1.set('Creating Schema.')

			for tempschema, tempvalue in mySchemaList.items():
				self.statusText1.set('Creating Schema...')
				mySchema = mySchema + tempschema
				if tempvalue == 2:
					typevar = ' short'
				elif tempvalue == 4:
					typevar = ' integer'
				elif tempvalue == 5:
					typevar = ' integer'
				elif tempvalue == 6:
					typevar = ' long'
				elif tempvalue == 8:
					typevar = ' long'
				elif tempvalue == 32:
					typevar = ' long'
				elif tempvalue == 65:
					typevar = ' string'
				elif tempvalue == 128:
					typevar = ' string'

				mySchema = mySchema + ' ' + typevar + ', '

			mySchema = mySchema[:len(mySchema) - 2] + ');'
			file.write('\n' + mySchema + '\n')
			file.close()
			self.success = True
			self.statusText1.set('Completed Successfully!!! ''Event Count: ' + str(eventsCount))
			return path1, self.outputfile, self.success

		except urllib.error.URLError:
			file.close()
			os.remove(path1)
			self.outputfile = 'F'
			path1 = ''
			self.success = False
			self.statusText1.set('FAILED!!! ''error while trying query! \n Check Username/password ')
			return

	def button_web_callback(self):
		"""OPEN THE ESPER TRY OUT PAGE."""
		webbrowser.open('https://esper-epl-tryout.appspot.com/epltryout/mainform.html', new=2)
		return

	def readme(self, event):
		"""LINK TO README ON GITLAB."""
		webbrowser.open('https://github.com/trevormiller6/nw2esper', new=2)
		return

	def button_openfile_callback(self):
		"""OPEN EVENTS FILE THAT GETS CREATED BY APP."""
		try:
			path1 = os.path.join(self.out_dir, self.outputfile)
			if len(self.outputfile) > 1:
				if platform.system() == "Windows":
					os.startfile(path1)
					return
				elif platform.system() == "Darwin":
					subprocess.Popen(["open", path1])
					return
				else:
					subprocess.Popen(["xdg-open", path1])
					return
			else:
				self.statusText1.set('No File to Open.')
				return
		except:
			self.statusText1.set('No File to Open.')
			return

	def button_restart_callback(self):
		"""CLEAR FORM TO PULL NEW EVENTS."""
		try:
			if self.success:
				if len(self.outputfile) > 1:
					result = tkMessageBox.askquestion("Delete", "Do you want to keep the file with events?", icon='warning')
					if result == 'no':
						shutil.rmtree(self.out_dir)
						self.statusText1.set('')
						self.entry2.delete(0, END)
						self.entry5.delete(0, END)
						self.entry6.delete(0, END)
						self.entry7.delete(0, END)
					else:
						self.statusText1.set('')
						self.entry2.delete(0, END)
						self.entry5.delete(0, END)
						self.entry6.delete(0, END)
						self.entry7.delete(0, END)
				else:
					return
			else:
				return
		except:
			self.statusText1.set('No Need, You havent done a query yet...')
			return

	def button_quit_callback(self):
		"""BUTTON TO QUIT THE APP."""
		try:
			if self.out_dir:
				if len(self.outputfile) > 1:
					result = tkMessageBox.askquestion("QUIT", "Do you want to keep the file with events?", icon='warning')
					if result == 'no':
						try:
							shutil.rmtree(self.out_dir)
							root.destroy()
						except:
							root.destroy()
					else:
						root.destroy()
				else:
					root.destroy()
			else:
				root.destroy()
		except:
			root.destroy()


def on_closing():
	"""EXIT CLEANLY USING THE "X" IN THE GUI."""
	frame.button_quit_callback()


root = Tk()
root.title("  Nw2esper  ")
frame = GUI(root)
root.protocol("WM_DELETE_WINDOW", on_closing)
root.mainloop()
