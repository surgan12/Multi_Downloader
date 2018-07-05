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
from zipfile import ZipFile
import gzip 
import shutil

x_pointer=[0]
y_pointer=[0]
class CreateToolTip(object):
    '''
    create a tooltip for a given widget
    '''
    def __init__(self, widget, text='widget info'):
        self.widget = widget
        self.text = text
        self.widget.bind("<Enter>", self.enter)
        self.widget.bind("<Leave>", self.close)
    def enter(self, event=None):
        x = y = 0
        x, y, cx, cy = self.widget.bbox("insert")
        x += self.widget.winfo_rootx() + 25
        y += self.widget.winfo_rooty() + 20
        # creates a toplevel window
        self.tw = tkinter.Toplevel(self.widget)
        # Leaves only the label and removes the app window
        self.tw.wm_overrideredirect(True)
        self.tw.wm_geometry("+%d+%d" % (x, y))
        label = tkinter.Label(self.tw, text=self.text, justify='left',
                       background='white', relief='solid', borderwidth=1,
                       font=("italics", "8", "normal"))
        label.pack(ipadx=1)
    def close(self, event=None):
        if self.tw:
            self.tw.destroy()


def internet_on(net_Var):
	while (True):
		for timeout in [1,5,10]:
			try:
				response=uri.urlopen('http://google.com',timeout=timeout)
				network.configure(text="ONLINE")


			except uri.URLError as err: pass
    	
    	network.configure(text="OFFLINE")
    	time.sleep(10000)

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


def threaded_download(start,end,file,downloaded_status,url,size,time_taken):
	get=time.clock()
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
		time_taken[0]+=time.clock()-get
	
	except uri.HTTPError,e:
		status.insert(END,'\n')
		status.insert(END,file+': HTTPError'+str(e.code))

	except uri.URLError,e:
		status.insert(END,'\n')

		status.insert(END,file+': HTTPError'+str(e,code))

    	
def creating_thread(start,end,file,downloaded_status,threads,url,size,time_taken):
	t1=threading.Thread(target=threaded_download,args=(start,end,file,downloaded_status,url,size,time_taken))
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
	time_taken=[0]
	url=url_enter.get()
	if not os.path.isdir(drect) and len(drect)!=0:
		status.insert(END,'\n')
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
				creating_thread(start,end,filename,downloaded_status,threads,url,size,time_taken)
		
			for t in threads:
				t.join()  	
	
			
			#global count
			#count=count+1
			count=done.size()+1
			done.insert(count,str(count)+'. '+filename+' ETA: '+str(time_taken[0])+'s')	
		except uri.URLError,e:
			status.insert(END,'\n')
			status.insert(END,filename +': HTTPError'+str(e.code))
		except uri.HTTPError,e:
			status.insert(END,'\n')
			status.insert(END,filename +': HTTPError'+str(e.code))
def tick():
    global time1
    # get the current local time from the PC
    time2 = time.strftime('%H:%M:%S')
    # if time string has changed, update it
    if time2 != time1:
        time1 = time2
        clock.config(text=time2)
        # calls itself every 200 milliseconds
        # to update the time display as needed
        # could use >200 ms, but display gets jerky
    clock.after(200, tick)	

def popup(event):
	x_pointer[0]=window.winfo_pointerx()-window.winfo_rootx()
	y_pointer[0]=window.winfo_pointery()-window.winfo_rooty()
	menu.tk_popup(event.x_root,event.y_root)

def CurSelet(event):
    widget = event.widget
    selection=widget.curselection()
    picked = widget.get(selection)
    picked=picked.strip()
    picked=picked.split()
    Menu_var.set(picked[1])
    f=int(picked[0][0])
    List_var.set(f-1)	
    
def delete(Menu_var):
	file=Menu_var.get()
	os.remove(file)
	status.insert(END,'\n')
	status.insert(END,file+" Deleted ")
	remove_from_list(List_var)
	
def compress(Menu_var):
	file=Menu_var.get()
	orignal=file
	file=file.split('.')
	file=file[0]+'.gz'
	with open(orignal,'rb')as inp:
		with open(file,'wb')as output:
			with gzip.GzipFile(file,'wb',fileobj=output)as output:
				shutil.copyfileobj(inp,output)
	status.insert(END,'\n')
	status.insert(END,orignal+" gzipped as "+file+'\n')

def remove_from_list(List_var):
	done.delete(List_var.get())
	list_size=done.size()
	for i in range(list_size):
		text=done.get(i)
		text=text.strip()
		text=text[1:]
		text='{}'.format(str(i+1))+str(text)
		done.delete(i)
		done.insert(i,text)
def clear_status():
	status.delete('1.0',END)

def help_rename(new,path,ent,lab):
	text=done.get(List_var.get())
	text=text.strip()
	text=text.split()
	text[1]=new
	o=""
	for t in text:
		o=o+t+" "
	done.delete(List_var.get())
	done.insert(List_var.get(),o)
	window.unbind('<Return>')
	ent.place_forget()
	lab.place_forget()

	command="mv "+str(path)+" "+str(new)
	os.popen(command)
	
def rename(path):
	window.unbind('<Return>')
	path=path.get()
	name=tkinter.Entry(window)
	name.place(x=x_pointer[0],y=y_pointer[0])
	new=tkinter.Label(text="RENAME")
	new.configure(bg="light yellow")
	new.place(x=x_pointer[0]+120,y=y_pointer[0]+1)
	window.bind('<Return>', lambda x :help_rename(name.get(),path,name,new))

#creating a window
window=tkinter.Tk()
window.title("Downloader")
window.geometry("800x600")
window.configure(bg="LemonChiffon3")
img = tkinter.PhotoImage(file = 'down.ico')
window.tk.call('wm', 'iconphoto', window._w, img)

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
window.bind('<Return>',lambda x:download_request(url_enter,number))
go.place(x=685,y=45)
go.configure(bg="light yellow",foreground="black")
go.configure(font="bold")
go.configure(highlightbackground="black")
#textbox for getting the status of downloaded items 
status=tkinter.Text(window,height=600,width=40)
status.place(x=0,y=100)	
status.configure(bg="light yellow",fg="black")

#textbox for downloaded files 
done=tkinter.Listbox(window,height=600,width=35)
done.place(x=300,y=100)
done.bind("<Button-3>",popup)
done.bind('<<ListboxSelect>>',CurSelet)

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

time1=' '

if(internet_on):
	status.insert(END,"Network status :Connected \n")
else:
	status.insert(END,"Check Network Connection \n")

#inserting a clock and running in background
clock = Label(window, font=('times', 15, 'bold'), bg='white')
clock.place(x=10,y=5)
clock_thread=threading.Thread(target=tick(),args=())
clock_thread.start()

Downloads=Label(window,text="Downloads",bg='light yellow')
Downloads.place(x=340,y=80)

Menu_var=tkinter.StringVar()
List_var=tkinter.IntVar()

#Right click menu for the listitems in the downloads section

menu=tkinter.Menu(window,tearoff=0)
menu.add_command(label="Compress",command=lambda:compress(Menu_var))
menu.add_separator()
menu.add_command(label="Delete",command=lambda:delete(Menu_var))
menu.add_separator()
menu.add_command(label="Remove From The List ",command=lambda:remove_from_list(List_var))
menu.add_separator()
menu.add_command(label="Rename",command=lambda: rename(Menu_var))
menu.bind("<FocusOut>",menu.unpost())

menu.configure(bg="white")

#clear 
path_2='clear.png'
clear = Image.open(path_2)
[wid,hei]=clear.size
clear=clear.resize((20,20),Image.ANTIALIAS)
img_c = ImageTk.PhotoImage(clear)
b_c=tkinter.Button(window,command=clear_status)
b_c.config(image=img_c)	
b_c.place(x=0,y=75)

b_c_tooltip=CreateToolTip(b_c,"Clearing Below Content")
#checking network status
net_Var=tkinter.StringVar()

network=tkinter.Label(window,text="Connection:",font="BOLD")
t1=threading.Thread(target=internet_on,args=(net_Var,))
t1.start()
network.configure(bg="light yellow")
network.place(x=590,y=550)
window.mainloop()

