from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import pymysql

window = Tk()

window.geometry("600x500")
window.title("Lion System")

def quantityFildListener(a,b,c):
    global quantityVar
    global costVar
    global itemRate
    quantity = quantityVar.get()

    if quantity !="":
        try:
            quantity=float(quantity)
            cost =quantity*itemRate
            quantityVar.set("%.2f"%quantity)
            costVar.set("%.2f"%cost)
        except ValueError:
            quantity=quantity[:-1]
            quantityVar.set(quantity)
    else:
        quantity=0
        quantityVar.set("%.2f"%quantity)

def costFildListener(a,b,c):
    global quantityVar
    global costVar
    global itemRate
    cost = costVar.get()

    if quantity !="":
        try:
            cost=float(cost)
            quantity = cost/itemRate
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


options = ["celular", "capa", "pelicula"] 
rateDict = {}
itemVariable = StringVar()
itemVariable.set(options[0])

billsTV = ttk.Treeview(height=15, columns=('Prod Nome', 'Quantidade', 'Valor'))
storOptions = ['Celular', 'Capa Transparent','case de IPhone','Prod.TI']

quantityVar = StringVar()
quantityVar.trace('w',quantityFildListener)

itemRate = 2
rateVar = StringVar()
rateVar.set("%.2f"%itemRate)
costVar = StringVar()
quantityVar.trace("w",costFildListener)

addItemNameVar = StringVar()
addItemRateVar = StringVar()
addItemTypeVar = StringVar()
addIstorVar = StringVar()
addItemTypeVar.set(storOptions[0])

def readAllData():
    global options
    global rateDict
    global itemVariable
    global itemRate
    global rateVar

    options = []
    rateDict = {}

    conn = pymysql.connect(host="localhost", user="root", password="",db="billservice")
    cursor = conn.cursor(pymysql.cursors.DictCursor)

    query = "select * from itemlist"
    cursor.execute(query)
    data = cursor.fetchall()

    count = 0
    for row in data:
        count+=1
        options.append(row['nameid'])
        rateDict[row['nameid']] =row['rate']
        itemVariable.set(options[0])
        itemRate =int(rateDict[options[0]])
    conn.close()
    rateVar.set(itemRate)
    if count==0:
        remove_all_widgetes()
        addItem()
    else:
        remove_all_widgetes()
        mainwindow()

def remove_all_widgetes():
    global window
    for Widget in  window.winfo_children():
        Widget.grid_remove()

def Login():
    global usernameVar
    global passwordVar
    
    username = usernameVar.get()
    password = passwordVar.get()

    conn = pymysql.connect(host="localhost", user="root", password="",db="billservice")
    cursor = conn.cursor()

    query = "select * from users where username='{}' and password='{}'".format(username,password)
    cursor.execute(query)
    data = cursor.fetchall()
    admin = False
    for row in data:
        admin = True
    conn.close()
    if admin:
        readAllData()
    else:
        messagebox.showerror("Usuario invalido", "Usuario ou Senha errados")

def additemListener():
    remove_all_widgetes()
    addItem()


    
def goBack():
    remove_all_widgetes()
    mainwindow()

def addItem():
    global addItemNameVar
    global addItemNameVar
    global addItemTypeVar
    global addIstorVar

    name = addItemNameVar.get()
    rate = addItemRateVar.get()
    Type = addItemTypeVar.get()
    storeType = addItemTypeVar.get()
    nameID = name.replace("","_")  

    conn = pymysql.connect(host="localhost", user="root", password="",db="billservice")
    cursor = conn.cursor()

    query = "insert into intemlist(name,nameid,rate,type,storetype)values('{}','{}','{}','{}','{}','{}',)".format(name,nameID,rate,Type,storeType)
    conn.execute(query)
    conn.commit()
    conn.close()
    addItemNameVar.set("")
    addItemRateVar.set("")
    addIstorVar.set("")
    

# -------------------------------------------------------------------------------------
def adminLogin():
    titleLabel = Label(window, text="Lion System", font="arial 30",fg="red")
    titleLabel.grid(row=0, column=0, columnspan=3,  padx=50, pady=10)

    loginLabel = Label(window, text="Administrador Login", font="arial 20")
    loginLabel.grid(row=1, column=2, padx=(50,00), columnspan=2, pady=10)

    usernameLabel = Label(window, text="Usuario:", font="arial 8" )
    usernameLabel.grid(row=2, column=2, padx=20, pady=5) 

    passwordLabel = Label(window, text="Senha:", font="arial 8" )
    passwordLabel.grid(row=3, column=2, padx=20, pady=5) 

    usernameEntry = Entry(window, textvariable=usernameVar)
    usernameEntry.grid(row=2,column=3, padx=20, pady=5)

    passwordEntry = Entry(window, textvariable=passwordVar, show="*")
    passwordEntry.grid(row=3, column=3, padx=20, pady=5)

    loginButton = Button(window, text="Login", width=8,height=0 ,font="arial 9",command=lambda:Login())
    loginButton.grid(row=4, column=2, columnspan=2)

# -----------------------------------------------------------------------------------------

def mainwindow():
    window.geometry("830x600")

    titleLabel = Label(window, text="Faturamento", font="arial 30",fg="green")
    titleLabel.grid(row=0, column=1, columnspan=3,  padx=50, pady=10)

    addButton = Button(window, text="Add Itens", width=8,height=0 ,font="arial 9",command=lambda:additemListener())
    addButton.grid(row=2, column=0, padx=(5,0), pady=(10,0))

    logoutBtn = Button(window, text="Sair", width=8,height=0 ,font="arial 9")
    logoutBtn.grid(row=2, column=4,  padx=(5,0), pady=(10,0))

    itemLbel = Label(window, text="Selecionar Item:" ,font="arial 9")
    itemLbel.grid(row=4, column=0, padx=(10,0), pady=10)

    itemDropDown= OptionMenu(window, itemVariable, *options)
    itemDropDown.grid(row=4, column=0, padx=(180,0), pady=10)

    #-----------------------------------------------
    rateLabel = Label(window, text="Taxa", font="arial 9")
    rateLabel.grid(row=1, column=2, padx=(10,0), pady=(10,0)) 

    rateValue = Label(window, textvariable=rateVar)
    rateValue.grid(row=1, column=3, padx=(10,0), pady=(10,0))
    #--------------------------------------------------
    costLabel = Label(window, text="Valor", font="arial 9")
    costLabel.grid(row=3, column=2, padx=(10,0), pady=(10,0)) 

    costEntry = Entry(window, textvariable=costVar)
    costEntry.grid(row=3,column=3,padx=(10,0), pady=(10,0))
    #-------------------------------------------------------------
    
    quantityLabel = Label(window, text="Quantidade:", font="arial 9")
    quantityLabel.grid(row=2, column=2, padx=(5,0), pady=(10,0)) 

    quantityEntry = Entry(window, textvariable=quantityVar)
    quantityEntry.grid(row=2,column=3,padx=(5,0), pady=(10,0))

    buttonBill = Button(window, text="Gerar Nota", font="arial 9")
    buttonBill.grid(row=4, column=4, pady=(10,0))

    # ==============================treeviw==========================================
    billLabel = Label(window, text="Produtos Listados", font="arial 25")
    billLabel.grid(row=4, column=2)

    billsTV.grid(row=5,column=0,columnspan=5, padx=(20,0), pady=(10,0))

    scrollBar = Scrollbar(window,orient="vertical", command=billsTV.yview)
    scrollBar.grid(row=5,column=4,sticky="NSE")

    billsTV.configure(yscrollcommand=scrollBar.set)

    billsTV.heading('#0',text="Nome Do Produto")
    billsTV.heading('#1',text="Taxa")
    billsTV.heading('#2',text="Quantidade")
    billsTV.heading('#3',text="Valor")
    
# ---------------------------------------------------------------------------------------------------------------- 

def addItem():
    window.geometry("900x600")

    backButton = Button(window, text="Voltar", font="arial 9", command=lambda:goBack())
    backButton.grid(row=0, column=0,padx=(5,0))

    titleLabel = Label(window, text="Faturamento",width=40, font="arial 30",fg="red")
    titleLabel.grid(row=0, column=1, columnspan=5, pady=(10,0))

    itemNomeLabel = Label(window, text="Nome", font="arial 8")
    itemNomeLabel.grid(row=1, column=1, pady=(10,0))

    itemNomeEntry = Entry(window,  textvariable=addItemNameVar)
    itemNomeEntry.grid(row=1, column=2, pady=(10,0))
#----------------------------------------------------------------------------------
    itemRateLabel = Label(window, text="Taxa Produto", font="arial 8")
    itemRateLabel.grid(row=1, column=3, pady=(10,0))

    itemRateEntry = Entry(window,textvariable=addItemRateVar )
    itemRateEntry.grid(row=1, column=4, pady=(10,0))
# -------------------------------------------------------------------
    itemTypeLabel = Label(window, text="Tipo Produto", font="arial 8")
    itemTypeLabel.grid(row=2, column=1, pady=(10,0))

    itemTypeEntry = OptionMenu(window, addItemTypeVar,*storOptions)
    itemTypeEntry.grid(row=2, column=2, pady=(10,0))
#-----------------------------------------------------------------------------------------
    storeTypeLabel = Label(window, text="Produto", font="arial 8")
    storeTypeLabel.grid(row=2, column=3, pady=(10,0))

    storeTypeEntry = Entry(window, textvariable=addIstorVar)
    storeTypeEntry.grid(row=2, column=4, pady=(10,0))

    addItemButton = Button(window, text="Add Item",width=20, height=0, font="arial 9")
    addItemButton.grid(row=3, column=3, pady=(10,0))

adminLogin()
window.mainloop()