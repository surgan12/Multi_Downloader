from tkinter import *
import tkinter
from tkinter import ttk
import urllib2 as uri 
import threading 
import random
import sys
import os
import time
from tkinter import END,LEFT,BOTH
from PIL import Image, ImageTk
import httplib
import urlparse

def internet_on():
    for timeout in [1,5,10,15]:
        try:
            response=urllib2.urlopen('http://google.com',timeout=timeout)
            return True
        except urllib2.URLError as err: pass
    return False

def check_valid_url(url):
	try:
		result=urlparse(url)
		return True
	except:
		return False

def get_file_name(url):
	url=url.strip()
	url=url.split('/')
	return url[-1] #last element will give the name of the file 

def threaded_download(start,end,file,downloaded_status,url,size):
	chunk={'Range':'bytes={}-{}'.format(start,end)}
	req=uri.Request(url,headers=chunk)
	try: 
    	
		get_file=uri.urlopen(req)
		with open(file,"r+b") as fp:
			fp.seek(start)			 #writing at a particular position.
			while True:
				data=get_file.read(1024)
				if not data:
					break

				fp.write(data) 	
				downloaded_status[0]+=len(data)

	except uri.HTTPError,e:
		status.insert(END,'\n')
		status.insert(END,file+': HTTPError'+str(e.code))

	except uri.URLError,e:
		status.insert(END,'\n')

		status.insert(END,file+': HTTPError'+str(e,code))

    	
def creating_thread(start,end,file,downloaded_status,threads,url,size):
	t1=threading.Thread(target=threaded_download,args=(start,end,file,downloaded_status,url,size))
	t1.start()
	threads.append(t1)

#for multiple download request at the same time
def download_request(url_enter,number):
	
	t1=threading.Thread(target=download,args=(url_enter,number))
	t1.start()

def download(url_enter,number):
	threads=[]
	number=number.get()
	downloaded_status=[0]
	drect=Directory.get()
	Directory.delete(0,'end')

	url=url_enter.get()
	if not os.path.isdir(drect) and len(drect)!=0:
		status.insert(END, url+ ": Invalid Directory \n")

	else:
		url_enter.delete(0,'end') #clearing the entry 	
		try:

			file=uri.urlopen(url)
			filename=get_file_name(url) 
			size=int(file.headers['content-length'])
			part=size/number
			path=drect
			filename=os.path.join(path,filename)
			oho=open(filename,"wb")
			oho.write('\0'*size) 	
			oho.close()
			st=time.clock()
			status.insert(END,'\n')
			status.insert(END,'Downloading {}'.format(filename))
			for i in range(0,number):
				start=part*i
				end=part+start
				creating_thread(start,end,filename,downloaded_status,threads,url,size)
		
			for t in threads:
				t.join()  	
	
			done.insert(END,'\n')
	
			stat="Downloaded {} Time taken : {} seconds".format(filename,time.clock()-st)
			done.insert(END,stat)	
		except uri.URLError,e:
			status.insert(END,'\n')
			status.insert(END,filename +': HTTPError'+str(e.code))
		except uri.HTTPError,e:
			status.insert(END,'\n')
			status.insert(END,filename +': HTTPError'+str(e.code))


#creating a window
window=tkinter.Tk()
window.title("Downloader")
window.geometry("800x600")
window.configure(bg="LemonChiffon3")
	
url=tkinter.Label(window,text="URL")
url.configure(bg="light yellow",foreground="black")
url.place(x=0,y=50)
url_enter=tkinter.Entry(window,width=80)	
url_enter.place(x=30,y=50)
url.configure(font="bold")

Dir_Label=tkinter.Label(text="DIRECTORY",font="bold")
Dir_Label.place(x=590,y=180)
Dir_Label.configure(bg="light yellow",fg="black")
Directory=tkinter.Entry(window)
Directory.place(x=590,y=200)
 
number=tkinter.IntVar() #variable for number of threads
go=tkinter.Button(window,text="Download",command=lambda:download_request(url_enter,number))
go.place(x=685,y=45)
go.configure(bg="light yellow",foreground="black")
go.configure(font="bold")
go.configure(highlightbackground="black")
#textbox for getting the status of downloaded items 
status=tkinter.Text(window,height=600,width=40)
status.place(x=0,y=100)	
status.configure(bg="light yellow",fg="black")

#textbox for downloaded files 
done=tkinter.Text(window,height=600,width=40)
done.place(x=300,y=100)


scrollbar=Scrollbar(window)
scrollbar.pack(side=RIGHT,fill=Y)


#making a label for threads
no_of_threads=tkinter.Label(window,text="NUMBER OF THREADS")
options=[1,2,3,4,5,6]


path="down.png"
image = Image.open(path)
[wid,hei]=image.size
image=image.resize((100,50),Image.ANTIALIAS)
img = ImageTk.PhotoImage(image)
panel=tkinter.Label(window,image=img)
panel.configure(highlightbackground="black")
panel.place(x=270,y=0)

number.set(1)
Option=tkinter.OptionMenu(window,number,*options)
no_of_threads.place(x=450,y=10)
no_of_threads.configure(bg="light yellow",fg="black")
no_of_threads.configure(font="bold")
Option.place(x=640,y=5)
Option.configure(bg="light yellow",fg="black",font="bold")
Option.configure(highlightbackground="black")

if(internet_on):
	status.insert(END,"Network status :Connected \n")
else:
	status.insert(END,"Check Network Connection \n")


window.mainloop()

