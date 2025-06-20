from tkinter import *
r = Tk()
r.title('test to comleat project')
botton = Button(r,text='Stop',width = 25,command=r.destroy)
botton.pack()

Label(r,text='enter firest name ').grid(row=0)
Label(r,text='enter last name ').grid(row=1)
e1 = Entry(r)
e2 = Entry(r)
e1.grid()

r.mainloop()
