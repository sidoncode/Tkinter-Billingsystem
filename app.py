from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog
import pymysql

window = Tk()
window.geometry("900x600")
window.title("Billing")
#===========field listner ==========================
def quantityFieldListener(a,b,c):
    global quantityVar
    global costVar
    global itemRate
    quantity = quantityVar.get()
    if quantity != "":
        try:
            quantity=float(quantity)
            cost = quantity*itemRate
            quantityVar.set("%.2f"%quantity)
            costVar.set("%.2f"%cost)
        except ValueError:
            quantity=quantity[:-1]
            quantityVar.set(quantity)
    else:
        quantity=0
        quantityVar.set("%.2f"%quantity)
def costFieldListener(a,b,c):
    global quantityVar
    global costVar
    global itemRate
    cost = costVar.get()
    if cost !="":
        try:
            cost = float(cost)
            quantity=cost/itemRate
            quantityVar.set("%.2f"%quantity)
            costVar.set("%.2f"%cost)
        except ValueError:
            cost=cost[:-1]
            costVar.set(cost)
    else:
        cost=0
        costVar.set(cost)
#============= global variable for  entries===========
#========login variable========
usernameVar = StringVar()
passwordVar = StringVar()

#============main window variable=======
options=[]
rateDict={}
itemVariable=StringVar()
quantityVar = StringVar()
quantityVar.trace('w',quantityFieldListener)
itemRate=2
rateVar = StringVar()
rateVar.set("%.2f"%itemRate)
costVar=StringVar()
costVar.trace('w', costFieldListener)