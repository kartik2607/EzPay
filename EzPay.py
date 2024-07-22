try:
    import sys
    import mysql.connector
    from tkinter import *
    from tkinter import messagebox
    import datetime
    import matplotlib.pyplot as py
    import numpy as np
except:
    print("\n\tERROR IN IMPORTING MODULES!")
    print("\tPlease make sure you have the following modules installed:\n")
    print("\t1) mysql.connector\n\t2) tkinter\n\t3) datetime")
    exit()
    
mydb=mysql.connector.connect(host='localhost',user='root',passwd='1234')
myc=mydb.cursor()
myc.execute('create database if not exists ezpay')
myc.execute('use ezpay')
root=Tk()
root.title('Welcome to EzPay')
img = PhotoImage(file = r"Precious Stones.png")
myaccount = PhotoImage(file = r"myaccount.png")
root.iconphoto(False,img)
root.configure(bg='tomato')
root.geometry('550x450')

myc.execute("create table if not exists user(Id int,Fname char(20), Lname char(20), Email char(30), Balance char(12), Passwd char(30),dattime varchar(40))")
myc.execute('create table if not exists transaction(Id int,dattime varchar(40),TransactionType varchar(40),amount int,receivername char(20),ttype varchar(20))')
myc.execute("create table if not exists number(AC int)")

def update_emails():
    global emails
    emails=[]
    myc.execute("select Email from user")
    for i in myc:
            emails.append(i[0])
            
def update_names():
    global names
    names=[]
    myc.execute("select Fname from user")
    for i in myc:
        names.append(i[0])   

def update_paw():
    global paw
    myc.execute("select Passwd from user where Id={}".format(Id))
    for i in myc:
        paw=i[0]
        
def update_info():
    global g,info
    g,info=[],[]
    myc.execute("select Passwd,balance,Fname from user where Email='{}'".format(em))
    for i in myc:
        g.append(i)
        info.append(i)
    
def signup():
    global Id
    update_emails()

    if e1.get()=='' or e2.get()=='' or e3.get()=='' or e4.get()=='' or e5.get()=='':
        messagebox.showerror('Error','Please enter your credentials completely!')
        e5.delete(0,END)       
        e6.delete(0,END)
        cb.deselect()
        b1.config(state='disabled')
    elif e3.get() in emails:
        messagebox.showerror('Error','This Email Address has already been used, please use another one.')
    elif e5.get()!=e6.get():
        messagebox.showerror('Error','Passwords do not match, please enter again!')
        e5.delete(0,END)
        e6.delete(0,END)
    else:
        accnumber=[]
        c=datetime.datetime.now()
        myc.execute('select AC from number')
        for i in myc:
            accnumber.append(i[0])
        if accnumber==[]:
            Id=1
            myc.execute('insert into number values({})'.format(Id))
        else:
            Id=accnumber[0]+1
            myc.execute('update number set AC=AC+1')
        mydb.commit()
        
        myc.execute("insert into user values({},'{}','{}','{}','{}','{}','{}')".format(Id,e1.get(),e2.get(),e3.get(),e4.get(),e5.get(),str(c)))
        myc.execute("insert into transaction values({},'{}','{}',{},'Acc Set-Up','Others')".format(Id,str(c),'Credit',int(e4.get())))
        
        mydb.commit()
        clentry()
        endwin(su)
        messagebox.showinfo('From EzPay','Sign up successful. Please log in to continue')
    
def login():
    global Id,g,em,paw,info
    if e1.get()=='' or e2.get()=='':
        messagebox.showerror('Error','Please enter your credentials completely!')
    elif e1.get() not in emails:
        messagebox.showerror('Error','There is no account registered with this Email ID.\n\nTry using another ID or create an account by clicking on sign up on the previous page.')
        e1.delete(0,END)
        e2.delete(0,END)
    else:
        g=[]
        info=[]
        em=e1.get()
        paw=e2.get()
        update_info()
        if paw==g[0][0]:
            myc.execute("select Id from user where Email='{}'".format(em))
            for i in myc:
                Id=i[0]
            
            endwin(log)
            open_interface()    
        else:
            messagebox.showerror('Error','Incorrect Password!')
            e2.delete(0,END)
           
def bactivate():
    if v1.get()==1:
        b1.config(state='normal')
    else:
        b1.config(state='disabled')

def pay():
    match=[]
    update_names()
    update_info()
    try:

        if e10.get()=='' or e20.get()=='' or e30.get()=='' or e40.get()=='':
            messagebox.showerror('Error','Enter the details completely')


        elif (e10.get() not in names) or (e20.get() not in emails):
            messagebox.showerror('Error','There is no account registered with this Email ID or Name.\n\nTry using another ID/Name')
            e10.delete(0,END)
            e20.delete(0,END)
        
        elif e40.get()!= paw:
            messagebox.showerror('Error','Wrong password.\nPlease enter again')
            e40.delete(0,END)
            
        
        elif int(e30.get())>int(info[0][1]):
            messagebox.showerror('Error','Insufficient balance in your account')
            e30.delete(0,END)
        
        elif e10.get()==info[0][2]:
            messagebox.showerror('Error','You can not transfer money to your own account')
            e10.delete(0,END)
            e20.delete(0,END)
            
        elif int(e30.get())<=0:
                messagebox.showerror('Error','Amount to be paid cannot be zero or a negative number!')
                e30.delete(0,END)
            
        else:
            myc.execute('select Fname from user where Email="{}"'.format(e20.get()))
            for j in myc:
                match.append(j[0])
            if e10.get() not in match:
                messagebox.showerror('Error','Email ID and Name does not match')
                e10.delete(0,END)
                e20.delete(0,END)
            else:
                myc.execute('select balance from user where Email="{}"'.format(em))
                a=myc.fetchall()
                a=int(a[0][0])
                myc.execute('select balance from user where Email="{}"'.format(e20.get()))
                b=myc.fetchall()
                b=int(b[0][0])
                a=str(int(a)-int(e30.get()))
                b=str(int(b)+int(e30.get()))
                myc.execute('update user set balance="{}" where Email="{}"'.format(a,em))
                mydb.commit()
                myc.execute('update user set balance="{}" where Email="{}"'.format(b,e20.get()))
                mydb.commit()
                c=datetime.datetime.now()
                myc.execute('select Id from user where Email="{}"'.format(e20.get()))
                i=myc.fetchall()
                i=int(i[0][0])
                myc.execute('select Id from user where Email="{}"'.format(em))
                i1=myc.fetchall()
                i1=int(i1[0][0])

                
                myc.execute('insert into transaction values({},"{}","{}",{},"Receiver","{}")'.format(i,str(c),'Credit',int(e30.get()),pvar.get()))
                mydb.commit()
                
                myc.execute('insert into transaction values({},"{}","{}",{},"{}","{}")'.format(i1,str(c),'Debit',int(e30.get()),e10.get(),pvar.get()))
                mydb.commit()
                messagebox.showinfo('From Ezpay','Transfer successful')
                pw.destroy()
                for i in mw.winfo_children(): 
                    if isinstance(i, Button):
                        i.config(state='normal')
    except:
        messagebox.showerror('Miscellaneous Error','You have a fundamental error in one of the options\n\nPlease make sure you enter only positive integers in the Amount section!')
        e30.delete(0,END)      
                
def clentry():
    e1.delete(0,END)
    e2.delete(0,END)
    e3.delete(0,END)
    e4.delete(0,END)
    e5.delete(0,END)
    e6.delete(0,END)
   
def createsu():
    buttonoff()
    global su,v1,b1,bb,e1,e2,e3,e4,e5,e6,cb
    v1=IntVar()
    su=Toplevel()
    su.title('Sign Up')
    su.geometry('1235x400')
    su.configure(bg='orange')
    su.iconphoto(False,img)
    
    background_label = Label(su, image=loginpic)
    background_label.place(x=0, y=0, relwidth=1, relheight=1)
    
    Label(su,text='CREATE AN ACCOUNT',font="Verdana 30 bold",bg='tomato',fg='white').place(x=417,y=15)
    l1=Label(su,text='First Name:',font="Verdana 20 bold",bg='tomato',fg='white')
    l2=Label(su,text='Last Name:',font="Verdana 20 bold",bg='tomato',fg='white')
    l3=Label(su,text='Email ID (Unique)*:',font="Verdana 20 bold",bg='tomato',fg='white')
    l4=Label(su,text='Enter starting Balance.:',font="Verdana 20 bold",bg='tomato',fg='white')
    l5=Label(su,text='Set Password:',bg='tomato',font="Verdana 20 bold",fg='white')
    l6=Label(su,text='Confirm Password:',font="Verdana 20 bold",bg='tomato',fg='white')
    e1=Entry(su,borderwidth=5,width=20)
    e2=Entry(su,borderwidth=5,width=20)
    e3=Entry(su,borderwidth=5,width=20)
    e4=Entry(su,borderwidth=5,width=20)
    e5=Entry(su,borderwidth=5,width=20,show='*')
    e6=Entry(su,borderwidth=5,width=20,show='*')
    cb=Checkbutton(su,text='*Agree to Terms and Conditions',variable=v1,command=bactivate,font="Verdana 15 bold",bg='tomato',fg='black',selectcolor='white')
    b1=Button(su,text='Sign Up',command=signup,state='disabled',font="Verdana 25 bold",bg='tomato',fg='white')
    bb=Button(su,text='← Back',command=lambda: endwin(su),font="Verdana 15 bold",bg='tomato',fg='white',height=1)

    l1.grid(row=3,column=2,padx=15,pady=10)
    l2.grid(row=3,column=4,padx=15,pady=10)
    l3.grid(row=5,column=2,padx=15,pady=10)
    l4.grid(row=5,column=4,padx=15,pady=10)
    l5.grid(row=7,column=2,padx=15,pady=10)
    l6.grid(row=8,column=2,padx=15,pady=10)
    e1.grid(row=3,column=3,padx=15,pady=10)
    e2.grid(row=3,column=5,padx=15,pady=10)
    e3.grid(row=5,column=3,padx=15,pady=10)
    e4.grid(row=5,column=5,padx=15,pady=10)
    e5.grid(row=7,column=3,padx=15,pady=10)
    e6.grid(row=8,column=3,padx=15,pady=10)
    cb.grid(row=9,column=4)
    b1.grid(row=9,column=2,padx=15,pady=10)
    bb.grid(row=0,column=0,padx=15,pady=10)
    
    su.protocol('WM_DELETE_WINDOW', lambda: endwin(su))    

def endwin(x):
    x.destroy()
    bsu.config(state='normal')
    blog.config(state='normal')
    breset.config(state='normal')
    
def createlog():
    buttonoff()
    global log,e1,e2,b1,emails
    log=Toplevel()

    C = Canvas(log, bg="blue")
    background_label = Label(log, image=loginpic)
    background_label.place(x=0, y=0, relwidth=1, relheight=1)
    log.title('Log In')
    log.geometry('1235x550')
    log.configure(bg='orange')
    Label(log,text='LOGIN TO CONTINUE',font="Verdana 30 bold",bg='tomato',fg='white').grid(row=0,column=1,columnspan=2)
    l1=Label(log,text='Email ID',font="Verdana 20 bold",bg='tomato',fg='white')
    l2=Label(log,text='Password',font="Verdana 20 bold",bg='tomato',fg='white')
    e1=Entry(log,borderwidth=5,width=35)
    e2=Entry(log,borderwidth=5,width=35,show='*')
    b1=Button(log,text='Submit',command=login,font="Verdana 20 bold",bg='brown',fg='white',height=1,width=7)
    bb=Button(log,text='← Back',command=lambda: endwin(log),font="Verdana 20 bold",bg='brown',fg='white',height=1,width=7)

    l1.grid(row=3,column=1,padx=15,pady=10)
    l2.grid(row=4,column=1,padx=15,pady=10)
    e1.grid(row=3,column=2,padx=15,pady=10)
    e2.grid(row=4,column=2,padx=15,pady=10)
    b1.grid(row=5,column=2,padx=15,pady=10)
    bb.grid(row=0,column=0,padx=15,pady=10)

    C.grid(row=0,column=0)


    emails=[]
    myc.execute("select Email from user")
    for i in myc:
        emails.append(i[0])
    log.protocol('WM_DELETE_WINDOW', lambda: endwin(log))

def open_nest():
        for i in mw.winfo_children(): 
            if isinstance(i, Button):
                i.config(state='disabled')

def close_nest(x):
        x.destroy()
        for i in mw.winfo_children(): 
            if isinstance(i, Button):
                i.config(state='normal')
    
def payb():
        open_nest()
        global e10,e20,e30,e40,names,pw,pvar,paychoices
        pw=Toplevel()
        pw.iconphoto(False,img)
        pw.title=('Pay Window')
        pw.geometry('800x200')
        pvar=StringVar(pw)
        pvar.set('Others')
        paychoices=['Friendly','Official','Business','Others']
        Label(pw,text='Enter The Details Here',font='Verdana 20 bold').grid(row=1,column=3,columnspan=2)
        l1=Label(pw,text='Enter the Account Name of Recipient:')
        l2=Label(pw,text='Enter email ID of the Account:')
        l3=Label(pw,text='Enter the amount you want to transfer:')
        l4=Label(pw,text='Enter your Password:')
        Label(pw,text='Transaction Type:').grid(row=7,column=4,padx=15,pady=10)
        paytype = OptionMenu(pw,pvar,*paychoices)
        be=Button(pw,text='Click here to pay',command=pay)
        e10=Entry(pw,borderwidth=5,width=15)
        e20=Entry(pw,borderwidth=5,width=15)
        e30=Entry(pw,borderwidth=5,width=15)
        e40=Entry(pw,borderwidth=5,width=20,show='*')
        l1.grid(row=3,column=2,padx=15,pady=10)
        l2.grid(row=3,column=4,padx=15,pady=10)
        l3.grid(row=5,column=2,padx=15,pady=10)
        l4.grid(row=5,column=4,padx=15,pady=10)
        e10.grid(row=3,column=3,padx=15,pady=10)
        e20.grid(row=3,column=5,padx=15,pady=10)
        e30.grid(row=5,column=3,padx=15,pady=10)
        e40.grid(row=5,column=5,padx=15,pady=10)
        be.grid(row=7,column=3,padx=15,pady=10)
        paytype.grid(row=7,column=5,padx=15,pady=10)
        pw.protocol('WM_DELETE_WINDOW', lambda: close_nest(pw))

def transfer():
    try:
        if e13.get()=='' or e14.get()=='':
            messagebox.showerror('Error','Enter the details completely')
        elif e14.get()!= paw:
            messagebox.showerror('Error','Wrong password.\nPlease enter again')
            e14.delete(0,END)
        elif int(e13.get())<=0:
            messagebox.showerror('Error','Amount to be added cannot be zero or a negative number!')
            e13.delete(0,END)
        else:
            c=datetime.datetime.now()
            myc.execute('select balance from user where Email="{}"'.format(em))
            a=myc.fetchall()
            a=int(a[0][0])
            a=str(int(a)+int(e13.get()))
            myc.execute('update user set balance="{}" where Email="{}"'.format(a,em))
            mydb.commit()
            myc.execute('select Id from user where Email="{}"'.format(em))
            i1=myc.fetchall()
            i1=int(i1[0][0])
            myc.execute('insert into transaction values({},"{}","{}",{},"Balance Recharge","Others")'.format(i1,str(c),'Credit',int(e13.get())))
            mydb.commit()
            messagebox.showinfo('From Ezpay','Transfer successful')
            for i in mw.winfo_children(): 
                if isinstance(i, Button):
                    i.config(state='normal')
            rc.destroy()
    except:
            messagebox.showerror('Miscellaneous Error','You have a fundamental error in one of the options\n\nPlease make sure you enter only positive integers in the Amount section!')
            e13.delete(0,END)
    update_info()    
    
def recb():
    open_nest()
    global rc,e13,e14
    rc=Toplevel()
    rc.iconphoto(False,img)
    rc.title=('Pay Window')
    Label(rc,text='Enter The Details Here',font='Verdana 20 bold').grid(row=1,column=3,columnspan=2)
    rc.geometry('700x150') 
    l3=Label(rc,text='Enter the amount you want to Add:').grid(row=3,column=2,padx=15,pady=10)
    l4=Label(rc,text='Enter your password:').grid(row=3,column=4,padx=15,pady=10)
    bw=Button(rc,text='Click to Add',command=transfer).grid(row=4,column=3,padx=15,pady=10)
    e13=Entry(rc,borderwidth=5,width=15)
    e14=Entry(rc,borderwidth=5,width=15,show='*')
    e13.grid(row=3,column=3,padx=15,pady=10)
    e14.grid(row=3,column=5,padx=15,pady=10)
    rc.protocol('WM_DELETE_WINDOW', lambda: close_nest(rc))
    
def reset():
    mbox=messagebox.askquestion ('From EzPay','Are you sure you want to DELETE ALL STORED DATA?\nThis action CANNOT be undone',icon = 'warning')
    if mbox == 'yes':
        myc.execute('drop database ezpay')
        messagebox.showinfo('From EzPay','EzPay Database deleted.\nThe app will now shut-down.')
        root.destroy()
        sys.exit()
    else:
        pass
    
def buttonoff():
    bsu.config(state='disabled')
    blog.config(state='disabled')
    breset.config(state='disabled')
    
def open_interface():
    buttonoff()
    global img
    global mw
    mw=Toplevel()
    mw.title('EzPay Homepage')
    mw.iconphoto(False,img)
    
    mw.configure(bg='orange')
    
    def closeb():
        for i in root.winfo_children(): 
            if isinstance(i, Toplevel):
                i.destroy()
        bsu.config(state='normal')
        blog.config(state='normal')
        breset.config(state='normal')
        
    mw.protocol('WM_DELETE_WINDOW', closeb)
    
    def grap():
        global gf
        cf.destroy()
        choices=['Type of Transaction','Daily Income v/s Expenditure (Last 5 days)','Daily Balance Comparision (Last 5 Days)']
        
        def draw(a):
            if a=='Type of Transaction':
                l=[]
                h=[]
                myc.execute('select ttype,count(ttype) from transaction where Id={} group by ttype'.format(Id)) 
                for i in myc:
                    l.append(i[0])
                    h.append(i[1])
                
                py.pie(h,labels=l,autopct='%1.1F%%')
                py.title('% of Each Type of Transaction Done',loc='center')
                py.gcf().canvas.set_window_title('Type of Transaction')
                
            elif a=='Daily Income v/s Expenditure (Last 5 days)':
                l,h,da=[],[],[]
                c=datetime.date.today()
                for i in range(5):
                    g,k=[],[]
                    myc.execute('select TransactionType,sum(amount) from transaction where Id={} and receivername!="Acc Set-Up" and dattime like "{}%" group by TransactionType order by field(TransactionType,"Credit","Debit")'.format(Id,c))
                    for j in myc:
                        g.append(j[0])
                        k.append(j[1])
                    if g!=[]:
                        l.append(g)
                        da.append(c)
                    else:
                        l.append(['Credit','Debit'])
                        da.append(c)
                    if k!=[]:
                        h.append(k)
                    else:
                        h.append([0,0])
                        
                    c-=datetime.timedelta(days=1)
                l.reverse()
                h.reverse()
                da.reverse()
                j=0
                x=0
                for i in range(0,len(l)):
                    if l[j][0]=='Credit':
                        py.bar(x+i,h[j][0],color='b',label='Credit',width=0.8)
                        py.text(x+i,h[j][0],str(h[j][0]),horizontalalignment='center',verticalalignment='center')
                        try:
                            if l[j][1]=='Debit':
                                py.bar(x+i+0.8,h[j][1],color='g',label='Debit',width=0.8)
                                py.text(x+i+0.8,h[j][1],str(h[j][1]),horizontalalignment='center',verticalalignment='center')
                        except:
                            py.bar(x+i+0.8,0,color='g',label='Debit',width=0.8)
                            py.text(x+i+0.8,10,0,horizontalalignment='center',verticalalignment='center')
                    elif l[j][0]=='Debit':
                        py.bar(x+i+0.8,h[j][0],color='g',label='Debit',width=0.8)
                        py.text(x+i+0.8,h[j][0],str(h[j][0]),horizontalalignment='center',verticalalignment='center')
                        py.bar(x+i,0,color='b',label='Credit',width=0.8)
                        py.text(x+i,10,0,horizontalalignment='center',verticalalignment='center')
                    j+=1
                    x+=1
                x=np.arange(0,len(l)*2,2)
                py.xticks(ticks=x+0.4,labels=da)
                py.xlabel('Date of Transaction',labelpad=10)
                py.ylabel('Amount Transacted',labelpad=10)
                py.title('Daily Income v/s Expenditure (Last 5 days)',loc='center')
                py.legend(['Income','Expenditure'],loc='upper right')
                py.gcf().canvas.set_window_title('Daily Income v/s Expenditure (Last 5 days)')
                
            elif a=='Daily Balance Comparision (Last 5 Days)':
                c=datetime.date.today()
                x=np.arange(5)
                myc.execute('select balance from user where Id={}'.format(Id))
                da,g=[datetime.date.today()],[]
                for i in myc:
                    g.append(i[0])
                balance=int(g[0])
                l=[balance]
                for i in range(4):
                    myc.execute('select TransactionType,amount from transaction where Id={} and receivername!="Acc Set-Up" and dattime like "{}%"'.format(Id,c))
                    for j in myc:
                        if j[0]=='Credit':
                            balance-=j[1]
                        elif j[0]=='Debit':
                            balance+=j[1]
                    l.append(balance)
                    c-=datetime.timedelta(days=1)
                    da.append(c)
                l.reverse()
                da.reverse()
                x=np.arange(5)
                py.plot(x,l,'b',label='Daily Balance')
                py.xticks(x,da)
                py.xlabel('Date',labelpad=10)
                py.ylabel('Balance',labelpad=10)
                py.title('Daily Balance Comparision (Last 5 Days)',loc='center')
                py.gcf().canvas.set_window_title('Daily Balance Comparision (Last 5 Days)')
                        
            py.show()
            
        gf=LabelFrame(aw,text='Graph Selector Panel',padx=30,pady=50)
        gf.pack(padx=100,pady=10)
        bback=Button(gf,text='Back',command=compare)
        bback.pack()
        gvar=StringVar(gf)
        Label(gf,text='Choose the parameter:').pack()
        option = OptionMenu(gf,gvar,*choices)
        option.pack()
        button=Button(gf,text='Plot Graph',command=lambda:draw(gvar.get()))
        button.pack()
        
    def compare():
        global cf,gf
        if gf is not None:
            gf.destroy()
            gf=None
        cf=LabelFrame(aw,text='Plot personal account activity',padx=30,pady=50)
        cf.pack()
        bc1=Button(cf,text='Open graph selector panel',command=grap)
        bc1.pack()

    def analyticsb():
        open_nest()
        global aw,cf,gf
        aw=Toplevel()
        aw.title=('Analytics Window')
        aw.iconphoto(False,img)
        aw.geometry('850x300')
        cf=gf=None
        compare()    
        aw.protocol('WM_DELETE_WINDOW', lambda: close_nest(aw))
        
    def transact():
        open_nest()
        global tw,fr1
        
        tw=Toplevel()
        tw.title('Your transactions')
        tw.geometry('950x300')
        tw.iconphoto(False,img)
        bb=Button(tw,text='Exit',command=lambda: close_nest(tw)).pack()
        fr1=None
        transframe()
        tw.protocol('WM_DELETE_WINDOW', lambda: close_nest(tw))
        
    def transframe():
        global fr,et1
        if fr1 is not None:
            fr1.destroy()
        fr=LabelFrame(tw,text='Transaction Details',padx=30,pady=50)
        fr.pack(padx=100,pady=10)
        Label(fr,text='Enter your Password:').grid(row=2,column=1,padx=10,pady=10)
        et1=Entry(fr,borderwidth=5,width=15,show='*')
        bt=Button(fr,text='Submit',command=showtrans).grid(row=3,column=2,padx=15,pady=10)
        et1.grid(row=2,column=2,padx=15,pady=10)
        
    def save_d():
        if ed1.get()=='' or ed2.get()=='' or ed3.get()=='' or ed4.get()=='':
            messagebox.showerror('Error','Please enter all your details to continue')
            ed4.delete(0,END)
        elif ed3.get() in emails:
            messagebox.showerror('Error','This Email Address has already been used, please use another one.')
            ed3.delete(0,END)
        elif ed4.get()!=paw:
            ed4.delete(0,END)
            messagebox.showerror('Error','Wrong password.\nPlease enter again')
        else:
            myc.execute('update user set Fname="{}",Lname="{}",Email="{}" where Id={}'.format(ed1.get(),ed2.get(),ed3.get(),Id))
            mydb.commit()
            messagebox.showinfo('From EzPay','Account Details saved')
            cframe()
            update_emails()
        update_info()
        
    def save_p():
        if ep1.get()=='' or ep2.get()=='' or ep3.get()=='':
            messagebox.showerror('Error','Please enter all your details to continue')
        elif ep1.get()!=paw:
            ep1.delete(0,END)
            messagebox.showerror('Error','Wrong password.\nPlease enter again')
        elif ep1.get()==ep2.get():
            messagebox.showerror('Error','Please Enter a new Password')
            ep2.delete(0,END)
            ep3.delete(0,END)
        elif ep2.get()!=ep3.get():
            messagebox.showerror('Error','Passwords do not match, please enter again!')
            ep2.delete(0,END)
            ep3.delete(0,END)
        else:
            mbox=messagebox.askquestion ('Change Password','Are you sure you want to change your Password\nThis action cannot be undone',icon = 'warning')
            if mbox == 'yes':
                myc.execute('update user set Passwd="{}" where Id={}'.format(ep3.get(),Id))
                mydb.commit()
                messagebox.showinfo('From EzPay','New Password set successfully')
                cframe()
                update_paw()
            else:
                ep1.delete(0,END)
                ep2.delete(0,END)
                ep3.delete(0,END)
        update_info()
                            
    def change_paw():
        global af1,ep1,ep2,ep3
        af.destroy()
        af1=LabelFrame(ad,text='Change Password',padx=30,pady=50)
        af1.pack(padx=100,pady=10)
        Label(af1,text='Enter Current Password:').grid(row=2,column=2,padx=10,pady=10)
        Label(af1,text='Enter New Password:').grid(row=3,column=2,padx=10,pady=10)
        Label(af1,text='Confirm New Password:').grid(row=4,column=2,padx=10,pady=10)
        ep1=Entry(af1,borderwidth=5,width=15,show='*')
        ep2=Entry(af1,borderwidth=5,width=15,show='*')
        ep3=Entry(af1,borderwidth=5,width=15,show='*')
        ep1.grid(row=2,column=3,padx=10,pady=10)
        ep2.grid(row=3,column=3,padx=10,pady=10)
        ep3.grid(row=4,column=3,padx=10,pady=10)
        bd=Button(af1,text='Save Changes',command=save_p).grid(row=5,column=3,padx=15,pady=10)
        bb=Button(af1,text='Back',command=cframe).grid(row=1,column=2,padx=15,pady=10)
        
    def editacc():
        global af1,ed1,ed2,ed3,ed4
        af.destroy()
        af1=LabelFrame(ad,text='Edit Account Details',padx=30,pady=50)
        af1.pack(padx=100,pady=10)
        Label(af1,text='First Name:').grid(row=3,column=3,padx=10,pady=10)
        Label(af1,text='Last Name:').grid(row=4,column=3,padx=10,pady=10)
        Label(af1,text='Email ID:').grid(row=5,column=3,padx=10,pady=10)
        Label(af1,text='Enter Password:').grid(row=7,column=3,padx=10,pady=10)
        ed1=Entry(af1,borderwidth=5,width=15)
        ed2=Entry(af1,borderwidth=5,width=15)
        ed3=Entry(af1,borderwidth=5,width=15)
        ed4=Entry(af1,borderwidth=5,width=15,show='*')
        ed1.grid(row=3,column=4,padx=10,pady=10)
        ed2.grid(row=4,column=4,padx=10,pady=10)
        ed3.grid(row=5,column=4,padx=10,pady=10)
        ed4.grid(row=7,column=4,padx=10,pady=10)
        bd=Button(af1,text='Save Changes',command=save_d).grid(row=8,column=4,padx=15,pady=10)
        bb=Button(af1,text='Back',command=cframe).grid(row=3,column=2,padx=15,pady=10)
        
    def del_acc():
        global af1,ede1,ede2
        af.destroy()
        af1=LabelFrame(ad,text='Delete Account',padx=30,pady=50)
        af1.pack(padx=100,pady=10)
        Label(af1,text='Enter Password:').grid(row=3,column=3,padx=10,pady=10)
        Label(af1,text='Confirm Password:').grid(row=4,column=3,padx=10,pady=10)
        ede1=Entry(af1,borderwidth=5,width=15,show='*')
        ede2=Entry(af1,borderwidth=5,width=15,show='*')
        ede1.grid(row=3,column=4,padx=10,pady=10)
        ede2.grid(row=4,column=4,padx=10,pady=10)
        bde=Button(af1,text='Continue',command=save_del).grid(row=5,column=4,padx=15,pady=10)
        bbe=Button(af1,text='Back',command=cframe).grid(row=3,column=2,padx=15,pady=10)

    def save_del():
        if ede1.get()=='' or ede2.get()=='':
            messagebox.showerror('Error','Please enter all details to continue')
        elif ede1.get()!=paw:
            messagebox.showerror('Error','Wrong password.\nPlease enter again')
            ede1.delete(0,END)
            ede2.delete(0,END)
        elif ede1.get()!=ede2.get():
            messagebox.showerror('Error','Passwords do not match, please enter again!')
            ede1.delete(0,END)
            ede2.delete(0,END)
        else:
            mbox=messagebox.askquestion ('From EzPay','Are you sure you want to DELETE YOUR ACCOUNT?\nThis action CANNOT be undone',icon = 'warning')
            if mbox == 'yes':                
                myc.execute('delete from user where Id={}'.format(Id))
                myc.execute('delete from transaction where Id={}'.format(Id))
                mydb.commit()
                messagebox.showinfo('From EzPay','Account Deleted\nYou will be directed back to the homepage')
                closeb()
            else:
                ede1.delete(0,END)
                ede2.delete(0,END)
        update_info()
        
    def accd():
        open_nest()
        global ad,af1
        ad=Toplevel()
        ad.title('Account Details')
        ad.iconphoto(False,img)
        ad.geometry('600x320')
        af1=None
        cframe()
        ad.protocol('WM_DELETE_WINDOW', lambda: close_nest(ad))

    def cframe():
        global af
        if af1 is not None:
            af1.destroy()
        l=[]
        myc.execute('select * from user where Id={}'.format(Id))
        for i in myc:
            l.append(i)
        
        af=LabelFrame(ad,text='Account Details',padx=30,pady=50)
        af.pack(padx=100,pady=10)
        Label(af,text='ID:').grid(row=3,column=3,padx=10,pady=10)
        Label(af,text='First Name:').grid(row=4,column=3,padx=10,pady=10)
        Label(af,text='Last Name:').grid(row=5,column=3,padx=10,pady=10)
        Label(af,text='Email ID:').grid(row=6,column=3,padx=10,pady=10)
        Label(af,text='Balance:').grid(row=7,column=3,padx=10,pady=10)
        Label(af,text=str(l[0][0])).grid(row=3,column=4,padx=10,pady=10)
        Label(af,text=str(l[0][1])).grid(row=4,column=4,padx=10,pady=10)
        Label(af,text=str(l[0][2])).grid(row=5,column=4,padx=10,pady=10)
        Label(af,text=str(l[0][3])).grid(row=6,column=4,padx=10,pady=10)
        Label(af,text=str(l[0][4])).grid(row=7,column=4,padx=10,pady=10)
        b1=Button(af,text='Edit account Details',command=editacc)
        b1.grid(row=4,column=5,padx=15,pady=10)
        b2=Button(af,text='Change Password',command=change_paw)
        b2.grid(row=5,column=5,padx=15,pady=10)
        b3=Button(af,text='Delete Account',command=del_acc)
        b3.grid(row=6,column=5,padx=15,pady=10)
            
    def showtrans():
        disp,head=[],[]
        if et1.get()=='':
            messagebox.showerror('Error','Please Enter your Password to continue')
            et1.delete(0,END)
        elif et1.get()!=paw:
            messagebox.showerror('Error','Wrong password.\nPlease enter again')
            et1.delete(0,END)
        else:
            global fr1
            fr.destroy()
            fr1=LabelFrame(tw,text='Transaction Details',padx=30,pady=50)
            fr1.pack(padx=100,pady=10) 
            head=['Date/Time of Transaction','Credit/Debit','Amount','Receiver','Type of Transaction']
            myc.execute('select dattime,transactiontype,amount,receivername,ttype from transaction where Id={}'.format(Id))
            for i in myc:
                disp.append(i)
            total_rows = len(disp) 
            total_columns = len(disp[0])
            bbt=Button(fr1,text='Back',command=transframe)
            bbt.grid(row=0,column=0)
            for j in range(5):
                if j==0:
                    et=Entry(fr1,width=30,bg='white',fg='black')
                else:
                    et=Entry(fr1,width=20,bg='white',fg='black')
                et.grid(row=2,column=j)
                et.insert(END,head[j])
                et.config(state='readonly')
            for i in range(total_rows):
                for j in range(total_columns):
                    et=Entry(fr1,width=20,bg='white',fg='black')
                    if j==0:
                        et=Entry(fr1,width=30,bg='white',fg='black')
                    else:
                        et=Entry(fr1,width=20,bg='white',fg='black')
                    et.grid(row=i+3,column=j)
                    et.insert(END,str(disp[i][j]))
                    et.config(state='readonly')
        update_info()
            
    
    img = PhotoImage(file = r"Precious Stones.png")
    mw.iconphoto(False,img)
    heading=Label(mw, text='Welcome To EzPay',bg='red',fg='white',font="Verdana 40 bold",padx=20,pady=20,width=500)
    heading.pack(side='top')
    pic=Label(mw, image=img)
    pic.pack(side='right')
    tr=Button(mw,text='View your Transactions',command=transact,bg='red',fg='black',font='verdana 20 bold',padx=10,pady=20,width=12)
    tr.pack(fill=X,side='bottom')
    pay=Button(mw,text='Pay',command=payb, bg='red',fg='black',font="Verdana 20 bold",padx=10,pady=20,width=12)
    pay.pack(fill=X,side='left')
    recieve=Button(mw,text='Add Balance',command=recb,bg='red',fg='black',font="Verdana 20 bold",padx=10,pady=20,width=12)
    recieve.pack(fill=X, side='left')
    close=Button(mw,text='LOG OUT', command=closeb,bg='red',fg='black',font="Verdana 20 bold",padx=10,pady=20,width=12)
    close.pack(fill=X, side='left')
    graph=Button(mw,text='Analytics', command=analyticsb,bg='red',fg='black',font="Verdana 20 bold",padx=10,pady=20,width=12)
    graph.pack(side='left')
    acc=Button(mw,text='My\nAccount',command=accd,image=myaccount,compound=TOP,bg='red',fg='black',font="Verdana 14 bold",padx=50,pady=5,width=8)
    acc.place(relx = 1, x =-510, y = 115, anchor = NE)
    


A = Canvas(root, bg="blue")
loginpic = PhotoImage(file =r"Ezpay-2.png")
filename = PhotoImage(file =r"Ezpay-3.png")
blabel = Label(root, image=filename)
blabel.place(x=0, y=0, relwidth=1, relheight=1)

img1 = PhotoImage(file = r"EzPay.png")       
Label(root,image=img1).pack()


bsu=Button(root,text='Sign Up',bg='dark orange',fg='black',font="Verdana 10 bold",padx=30,pady=20,command=createsu)
blog=Button(root,text='Log In',bg='orange',fg='black',font="Verdana 10 bold",padx=30,pady=20,command=createlog)
breset=Button(root,text='Hard Reset',bg='dark orange',fg='black',font="Verdana 10 bold",padx=30,pady=20,command=reset)
bsu.pack(fill=X,side='bottom')
blog.pack(fill=X,side='bottom')
breset.pack(fill=X,side='bottom')
A.pack()
root.mainloop()
