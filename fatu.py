from tkinter import *
from tkinter import ttk
from tkinter import messagebox

import pymysql

window = Tk()
window.geometry("900x600")
window.title("Lion System")
window.configure(background='lightblue')

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



usernameVar = StringVar()
passwordVar = StringVar()


options=[]
rateDict={}
itemVariable=StringVar()
# itemVariable.set(options[0])
quantityVar = StringVar()
quantityVar.trace('w',quantityFieldListener)
itemRate=2
rateVar = StringVar()
rateVar.set("%.2f"%itemRate)
costVar=StringVar()
costVar.trace('w', costFieldListener)

billsTV = ttk.Treeview(height=15, columns=('Rate','Quantity','Cost'))

updateTV = ttk.Treeview(height=15, columns=('name','rate','type','storetype'))




storeOptions=['Pelicula3D','Impressão','Capa Trans']
addItemNameVar=StringVar()
addItemRateVar=StringVar()
addItemTypeVar=StringVar()
addstoredVar=StringVar()
addstoredVar.set(storeOptions[0])

itemLists = list()
totalCost = 0.0
totalCostVar = StringVar()
totalCostVar.set("Valor Total = {}".format(totalCost))

updateItemId=""

def generate_bill():
    global itemVariable
    global quantityVar
    global itemRate
    global costVar
    global itemLists
    global totalCost
    global totalCostVar

    itemName = itemVariable.get()
    quantity =quantityVar.get()
    cost = costVar.get()

    conn = pymysql.connect(host="localhost", user="root", passwd="", db="billservice")
    cursor = conn.cursor()

    query = "insert into bill (name,quatity,rate,cost) value('{}','{}','{}','{}')".format(itemName, quantity,itemRate,cost)
    cursor.execute(query)
    conn.commit()
    conn.close()

    listDict = {"name":itemName,"rate":itemRate,"quatity":quantity,"cost":cost}
    itemLists.append(listDict)
    totalCost += float(cost)
    print(itemLists)

    quantityVar.set("0")
    costVar.set("0")
    upDateListView()
    totalCostVar.set("Valor Total = {}".format(totalCost))

def onDoubleClick(event):
    global addItemNameVar
    global addItemRateVar
    global addItemTypeVar
    global addstoredVar
    global updateItemId
    item = updateTV.selection()
    updateItemId = updateTV.item(item,"text")
    item_detail = updateTV.item(item,"values")
    item_index = storeOptions.index(item_detail[3])
    addItemTypeVar.set(item_detail[2])
    addItemRateVar.set(item_detail[1])
    addItemNameVar.set(item_detail[0])
    addstoredVar.set(storeOptions[item_index])

def upDateListView():
    records = billsTV.get_children()
    for element in records:
        billsTV.delete(element)

   
    for row in itemLists:
        billsTV.insert('','end', text=row['name'], values=(row["rate"],row["quatity"],row["cost"]))

def getItemLists():
    recods = updateTV.get_children()
    for element in recods:
        updateTV.delete(element)

    conn = pymysql.connect(host="localhost", user="root", passwd="", db="billservice")
    cursor = conn.cursor(pymysql.cursors.DictCursor)

    query = "select * from itemlist"
    cursor.execute(query)
    data = cursor.fetchall()
    for row in data:
        updateTV.insert('','end',text=row['nameid'],values=(row['name'],row['rate'],row['type'],row['storetype']))
    updateTV.bind("<Double-1>",onDoubleClick)    
    conn.close()

def print_bill():
    global itemLists
    global totalCost
    print("=========================Recibo============================\n")
    print("{:<20}{:<10}{:<15}{:<10}".format("Nome","Valor","Quantidade","Custo"))
    print("-------------------------------------------------------------")
    for item in itemLists:
        print("{:<20}{:<10}{:<15}{:<10}".format(item["name"],item["rate"],item["quatity"],item["cost"]))
    print("-----------------------------------------------------------")
    print("{:<20}{:<10}{:<15}{:<10}".format("Valor Total:"," "," ",totalCost))
    print("==================Obrigado Pela preferencia================")
    itemLists = []
    totalCost=0.0
    upDateListView()
    totalCostVar.set("Valor Total = {}".format(totalCost))


def iExit():
    window.destroy()

def moveToUpdate():
    remove_all_widgets()
    updateItemWindow()

def  moveToBills():
    remove_all_widgets()
    ViewAllBill()

def readAllData():
    global options
    global rateDict
    global itemVariable
    global itemRate
    global rateVar
    options=[]
    rateDict={}
    conn = pymysql.connect(host="localhost", user="root", passwd="", db="billservice")
    cursor = conn.cursor(pymysql.cursors.DictCursor)

    query = "select * from itemlist"
    cursor.execute(query)
    data = cursor.fetchall()
    count=0
    for row in data:
        count+=1
        options.append(row['nameid'])
        rateDict[row['nameid']]=row['rate']
        itemVariable.set(options[0])
        itemRate=str(rateDict[options[0]])#int
    conn.close()
    rateVar.set(itemRate)#"%.2f"%
    if count ==0:
        remove_all_widgets()
        itemAddWindow()
    else:
        remove_all_widgets()
        mainwindow()
        
def optionMenuListener(event):
    global itemVariable
    global rateDict
    global itemRate

    item = itemVariable.get()
    itemRate=float(rateDict[item])
    rateVar.set("%.2f"%itemRate)

def remove_all_widgets():
    global window
    for widget in window.winfo_children():
        widget.grid_remove()

def updateBillsData():
    records = billsTV.get_children()
    for element in records:
        billsTV.delete(element)

   
    conn = pymysql.connect(host="localhost", user="root", passwd="", db="billservice")
    cursor = conn.cursor(pymysql.cursors.DictCursor)

    query = "select * from bill"
    cursor.execute(query)
    data = cursor.fetchall()

    for row in data:
        billsTV.insert('','end', text=row['name'], values=(row["rate"],row["quatity"],row["cost"]))
    conn.close()



def adminLogin():
    global usernameVar
    global passwordVar

    username = usernameVar.get()
    password = passwordVar.get()

    conn = pymysql.connect(host="localhost", user="root", passwd="", db="billservice")
    cursor = conn.cursor()

    query = "select * from users where username='{}' and password='{}'".format(username, password)
    cursor.execute(query)
    data = cursor.fetchall()
    admin = False
    for row in data:
        admin = True
    conn.close()
    if admin:
        remove_all_widgets()
        itemAddWindow()
    else:
        messagebox.showerror("Digite Corretamente", "Usuario e Senha Erradas")

def addItemListener():
    remove_all_widgets()
    itemAddWindow()
    
# def goBack():
#     remove_all_widgets()
#     mainwindow()

def addItem():
    global addItemNameVar
    global addItemRateVar
    global addItemTypeVar
    global addstoredVar
    name = addItemNameVar.get()
    rate = addItemRateVar.get()
    Type = addItemTypeVar.get()
    storeType= addstoredVar.get()
    nameId=name.replace(" ","_")
    conn = pymysql.connect(host="localhost", user="root", passwd="", db="billservice")
    cursor = conn.cursor()
    query = "insert into itemlist (name,nameid,rate,type,storetype) value('{}','{}','{}','{}','{}')".format(name, nameId, rate,Type,storeType)
    cursor.execute(query)
    conn.commit()
    conn.close()
    addItemNameVar.set("")
    addItemRateVar.set("")
    addItemTypeVar.set("")

def updateItem():
    global addItemNameVar
    global addItemRateVar
    global addItemTypeVar
    global addstoredVar
    global updateItemId

    name = addItemNameVar.get()
    rate = addItemRateVar.get()
    Type = addItemTypeVar.get()
    storeType= addstoredVar.get()
    conn = pymysql.connect(host="localhost", user="root", passwd="", db="billservice")
    cursor = conn.cursor()
    query = "update itemlist set name='{}',rate='{}',type='{}',storetype='{}' where nameid='{}'".format(name,rate,Type,storeType,updateItemId)
    cursor.execute(query)
    conn.commit()
    conn.close()


    addItemNameVar.set("")
    addItemRateVar.set("")
    addItemTypeVar.set("")
    getItemLists()

def loginWindow():
    window.geometry("500x350")

    titleLabel = Label(window,text="Sistema Nota  Fiscal",font=("times new roman",35),bg="lightblue",fg="green")
    titleLabel.grid(row=0,column=0,columnspan=4, padx=(40,0),pady=(10,0))

    loginLabel = Label(window,text="Login",font="Arial 30",bg="lightblue")
    loginLabel.grid(row=1, column=2,padx=(50,0),columnspan=2, pady=10)

    usernameLabel = Label(window, text="Username :", font=("bold", 15),bg="lightblue")
    usernameLabel.grid(row=2, column=2,padx=20,pady=5)

    passwordLabel = Label(window, text="Senha :" , font=("bold", 15),bg="lightblue")
    passwordLabel.grid(row=3, column=2,padx=20,pady=5)

    usernameEntry= Entry(window, textvariable=usernameVar)
    usernameEntry.grid(row=2, column=3,padx=20,pady=5)

    passwordEntry = Entry (window, textvariable=passwordVar,show="*")
    passwordEntry.grid(row=3,column=3,padx=20,pady=5)

    loginButton=Button(window, text="Login",bg="orange" ,fg="white" ,font=("arial", 17),width=23, height=2, command=lambda:adminLogin())
    loginButton.grid(row=4, column=2, columnspan=2)


def mainwindow():
    window.geometry("820x605")

    titleLabel = Label(window,text="Sistema Nota  Fiscal",font=("times new roman",35),bg="lightblue",fg="green")
    titleLabel.grid(row=0,column=1,columnspan=3,pady=(10,0))

    addNewItem = Button(window, text="Add Prod", font=("bold", 10),width=15, bg="orange" ,fg="white",height=2, command=lambda: addItemListener())
    addNewItem.grid(row=1, column=0, padx=(10,0),pady=(10,0))
    updateItem = Button(window, text="Atualizar", bg="orange" , font=("bold", 10),fg="white",width=15, height=2,command=lambda: moveToUpdate())
    updateItem.grid(row=1, column=1, padx=(10,0), pady=(10,0))

    showallEntry= Button(window, text="Lista De Notas", width=15, height=2, font=("bold", 10),bg="orange" ,fg="white",command=lambda:moveToBills())
    showallEntry.grid(row=1, column=2, padx=(10,0), pady=(10,0))

    logoutBtn = Button(window, text = "Sair",width=15, height=2, font=("bold", 10),bg="orange" ,fg="white",command=lambda:iExit())
    logoutBtn.grid(row=1, column=4,pady=(10,0))

    itemLabel = Label(window, text="Selecionar",bg="lightblue")
    itemLabel.grid(row=2, column=0, padx=(5,0),pady=(10,0))

    itemDropDown=OptionMenu(window,itemVariable,*options, command=optionMenuListener)
    itemDropDown.grid(row=2, column=1,padx=(10,0), pady=(10,0))

    rateLabel= Label(window, text="Preco",bg="lightblue")
    rateLabel.grid(row=2, column=2, padx=(10,0), pady=(10,0))

    rateValue = Label(window,bg="lightblue", textvariable=rateVar)
    rateValue.grid(row=2, column=3, padx=(10,0), pady=(10,0))

    quantityLabel = Label(window,bg="lightblue", text="Quantidade")
    quantityLabel.grid(row=3, column=0,padx=(5,0),pady=(10,0))
    quantityEntry=Entry(window, textvariable=quantityVar)
    quantityEntry.grid(row=3, column=1,padx=(5,0),pady=(10,0))

    costLabel= Label(window,bg="lightblue", text="Valor")
    costLabel.grid(row=3, column=2, padx=(10,0), pady=(10,0))

    costEntry=Entry(window, textvariable=costVar)
    costEntry.grid(row=3, column=3, padx=(10,0), pady=(10,0))

    buttonBill = Button(window, text="Add Para Lista", font=("bold", 10), width =15,bg="orange" ,fg="white", command=lambda:generate_bill())
    buttonBill.grid(row=3, column=4,padx=(5,0),pady=(10,0))

    billLabel=Label(window, text="Lista De Produtos", font="Arial 25",bg="lightblue")
    billLabel.grid(row=4, column=2)

    billsTV.grid(row=5, column=0, columnspan=5,padx=(5))

    scrollBar = Scrollbar(window, orient="vertical",command=billsTV.yview)
    scrollBar.grid(row=5, column=4, sticky="NSE")

    billsTV.configure(yscrollcommand=scrollBar.set)

    billsTV.heading('#0',text="Prod Nome")
    billsTV.heading('#1',text="Taxa")
    billsTV.heading('#2',text="Quantidade")
    billsTV.heading('#3',text="Custo")

    totalCostLabel=Label(window, textvariable=totalCostVar,bg="orange")
    totalCostLabel.grid(row=6, column=1)

    generateBill = Button(window, text="Gerar Nota",font=("bold",10),width=15, bg="orange" ,fg="white",command=lambda:print_bill())
    generateBill.grid(row=6, column=4)

    upDateListView()

def itemAddWindow():
    window.geometry("500x200")
    backButton = Button(window, text="Voltar" , bg="orange" ,fg="white", command=lambda:readAllData())
    backButton.grid(row=0, column=1)
    titleLabel = Label(window,text="Sistema Nota  Fiscal",font=("times new roman",35),bg="lightblue",fg="green")
    titleLabel.grid(row=0,column=2,columnspan=4,pady=(10,0))

    itemNameLabel= Label(window, text="Nome",bg="lightblue")
    itemNameLabel.grid(row=1, column=1, pady=(10,0))

    itemNameEntry= Entry(window, textvariable=addItemNameVar)
    itemNameEntry.grid(row=1, column=2, pady=(10,0))

    itemRateLabel= Label(window, text="Preco",bg="lightblue")
    itemRateLabel.grid(row=1, column=3, pady=(10,0))
    
    itemRateEntry= Entry(window, textvariable=addItemRateVar)
    itemRateEntry.grid(row=1, column=4, pady=(10,0))
    

    itemtypeLabel= Label(window, text="Tipo Prod",bg="lightblue")
    itemtypeLabel.grid(row=2, column=1, pady=(10,0))
    itemTypeEntry= Entry(window, textvariable=addItemTypeVar)
    itemTypeEntry.grid(row=2, column=2, pady=(10,0))

    storeTypeLabel= Label(window, text="Tipo Stoque",bg="lightblue")
    storeTypeLabel.grid(row=2, column=3, pady=(10,0))
    storeEntry= OptionMenu(window, addstoredVar,*storeOptions)
    storeEntry.grid(row=2, column=4, pady=(10,0))

    AddItemButton = Button(window, text="Add Prod", bg="orange" ,fg="white", width=20, height=2, command=lambda:addItem())
    AddItemButton.grid(row=3, column=3,pady=(10,0))

def updateItemWindow():
    window.geometry("1050x550")
    backButton = Button(window, text="Voltar" , bg="orange" ,fg="white", command=lambda:readAllData())
    backButton.grid(row=0, column=1)
    titleLabel = Label(window,text="Sistema Nota  Fiscal",font=("times new roman",35),bg="lightblue",fg="green")
    titleLabel.grid(row=0,column=2,columnspan=4,pady=(10,0))

    itemNameLabel= Label(window, text="Nome",bg="lightblue")
    itemNameLabel.grid(row=1, column=1, pady=(10,0))

    itemNameEntry= Entry(window, textvariable=addItemNameVar)
    itemNameEntry.grid(row=1, column=2, pady=(10,0))

    itemRateLabel= Label(window, text="Preco",bg="lightblue")
    itemRateLabel.grid(row=1, column=3, pady=(10,0))
    
    itemRateEntry= Entry(window, textvariable=addItemRateVar)
    itemRateEntry.grid(row=1, column=4, pady=(10,0))
    

    itemtypeLabel= Label(window, text="Tipo Prod",bg="lightblue")
    itemtypeLabel.grid(row=2, column=1, pady=(10,0))
    itemTypeEntry= Entry(window, textvariable=addItemTypeVar)
    itemTypeEntry.grid(row=2, column=2, pady=(10,0))

    storeTypeLabel= Label(window, text="Tipo Stoque",bg="lightblue")
    storeTypeLabel.grid(row=2, column=3, pady=(10,0))
    storeEntry= OptionMenu(window, addstoredVar,*storeOptions)
    storeEntry.grid(row=2, column=4, pady=(10,0))

    AddItemButton = Button(window, text="Atualizar", bg="orange" ,fg="white", width=20, height=2, command=lambda:updateItem())
    AddItemButton.grid(row=3, column=3,pady=(10,0))

    updateTV.grid(row=4, column=0, columnspan=5,padx=(9))

    scrollBar = Scrollbar(window, orient="vertical",command=billsTV.yview)
    scrollBar.grid(row=4, column=5, sticky="NSE")

    updateTV.configure(yscrollcommand=scrollBar.set)


    updateTV.heading('#0',text="Prod Id")
    updateTV.heading('#1',text="Prod Nome")
    updateTV.heading('#2',text="Preço")
    updateTV.heading('#3',text="Tipo")
    updateTV.heading('#4',text="Tipo do estoque")

    getItemLists()

def ViewAllBill():
    window.geometry("830x500")
    backButton = Button(window, text="Voltar" , bg="orange" ,fg="white", command=lambda:readAllData())
    backButton.grid(row=0, column=1)

    titleLabel = Label(window,text="Sistema Nota  Fiscal",font=("times new roman",35),bg="lightblue",fg="green")
    titleLabel.grid(row=1,column=0,columnspan=4,pady=(10,0))

    billLabel=Label(window, text="Lista De Produtos", font="Arial 25",bg="lightblue")
    billLabel.grid(row=4, column=2)

    billsTV.grid(row=5, column=0, columnspan=5,padx=(5))

    scrollBar = Scrollbar(window, orient="vertical",command=billsTV.yview)
    scrollBar.grid(row=5, column=4, sticky="NSE")

    billsTV.configure(yscrollcommand=scrollBar.set)

    billsTV.heading('#0',text="Prod Nome")
    billsTV.heading('#1',text="Preço")
    billsTV.heading('#2',text="Quantidade")
    billsTV.heading('#3',text="Valor Total")

    updateBillsData()
 
loginWindow()
window.mainloop()