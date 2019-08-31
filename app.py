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
#========mainTreeView======================
billsTV = ttk.Treeview(height=15, columns=('Rate','Quantity','Cost'))

#==========update tree View
updateTV = ttk.Treeview(height=15, columns=('Name','Rate','type','Store_Type'))

#============= add item Variables==========
storeOptions=['Frozen','Fresh']
addItemNameVar=StringVar()
addItemRateVar=StringVar()
addItemTypeVar=StringVar()
addstoredVar=StringVar()
addstoredVar.set(storeOptions[0])

itemLists= list()
totalCost=0.0
totalCostVar=StringVar()
totalCostVar.set("Total Cost = {}".format(totalCost))

updateItemId=""
#=============funtion to generate bill=====================
def generate_bill():
    global itemVariable
    global quantityVar
    global itemRate
    global costVar
    global itemLists
    global totalCost
    global totalCostVar
    itemName = itemVariable.get()
    quantity=quantityVar.get()
    cost = costVar.get()
    conn = pymysql.connect(host="localhost", user="root", passwd="", db="billing system")
    cursor = conn.cursor()
    
    query="insert into bill (name,quantity, rate, cost) values('{}','{}','{}','{}')".format(itemName,quantity,itemRate,cost)
    cursor.execute(query)
    conn.commit()
    conn.close()
    listDict = {"name":itemName, "rate":itemRate,"quantity":quantity, "cost":cost}
    itemLists.append(listDict)
    totalCost+=float(cost)
    quantityVar.set("0")
    costVar.set("0")
    updateListView()
    totalCostVar.set("Total Cost = {}".format(totalCost))
def OnDoubleClick(event):
    global addItemNameVar
    global addItemRateVar
    global addItemTypeVar
    global addstoredVar
    global updateItemId
    item = updateTV.selection()
    updateItemId= updateTV.item(item,"text")
    item_detail= updateTV.item(item,"values")
    item_index=storeOptions.index(item_detail[3])
    addItemTypeVar.set(item_detail[2])
    addItemRateVar.set(item_detail[1])
    addItemNameVar.set(item_detail[0])
    addstoredVar.set(storeOptions[item_index])



def updateListView():
    records = billsTV.get_children()

    for element in records:
        billsTV.delete(element)

    for row in itemLists:
        billsTV.insert('', 'end',text=row['name'],values=(row["rate"],row["quantity"],row["cost"]))
def getItemLists():
    records=updateTV.get_children()

    for element in records:
        updateTV.delete(element)
    
    conn = pymysql.connect(host="localhost", user="root", passwd="", db="billing system")
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    query="select * from itemlist"
    cursor.execute(query)
    data = cursor.fetchall()
    for row in data:
        updateTV.insert('','end',text=row['nameid'],values=(row['name'],row['rate'],row['type'],row['storetype']))
    updateTV.bind("<Double-1>",OnDoubleClick)

    conn.close()