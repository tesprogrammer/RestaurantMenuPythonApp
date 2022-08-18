import xml.etree.ElementTree as ET
import re  # import regex
from tkinter import *
from tkinter import ttk

################## PARSE XML ###############################################
tree = ET.parse('menu.xml')

root = tree.getroot()
menuitems = root.findall('./MenuItem/Item')
for num, value in enumerate(menuitems):
    menuitems[num] = value.text
menuvalue = root.findall('./MenuItem/Menu')
for num, value in enumerate(menuvalue):
    menuvalue[num] = value.text
menuprice = root.findall('./MenuItem/Price')
for num, value in enumerate(menuprice):
    menuprice[num] = float(value.text)

# zips menu items into a list
itemandprice = list(zip(menuitems, menuvalue, menuprice))

AllItemsPrices = {}
MenuItemsPrice0 = {}
MenuItemsPrice1 = {}
MenuItemsPrice2 = {}
MenuItemsPrice3 = {}

for value in itemandprice:
    AllItemsPrices[value[0]] = value[2]
    if value[1] == '0':
        MenuItemsPrice0[value[0]] = value[2]
    elif value[1] == '1':
        MenuItemsPrice1[value[0]] = value[2]
    elif value[1] == '2':
        MenuItemsPrice2[value[0]] = value[2]
    elif value[1] == '3':
        MenuItemsPrice3[value[0]] = value[2]

##################### SET UP TKINTER ############################################
root = Tk()
root.geometry('740x530')
root.title("Shelly's Diner")

tabFrame = Frame(root, highlightbackground="lightgray", highlightthickness=1)
tabFrame.grid(row=0, column=0, rowspan=1, sticky='w')
tabControl = ttk.Notebook(tabFrame)

tab1 = Frame(tabControl)
tab2 = Frame(tabControl)
tab3 = Frame(tabControl)
tab4 = Frame(tabControl)

tabControl.add(tab1, text='Entre\'')
tabControl.add(tab2, text='Sides')
tabControl.add(tab3, text='Drinks')
tabControl.add(tab4, text='Desert')
tabControl.pack(expand=1, fill="both")

total = 0
tax = 0
total1 = 0
total2 = 0
total3 = 0
total4 = 0
totalDisp = Label()

################## CREATE CLASS TO TRACK TOTAL AND TAX #############################
# Class creates total and tax from menu items
# Credit: https://stackoverflow.com/questions/69576329/calculating-totals-from-entries-in-gui
class Counter:
    def __init__(self):
        self.total = DoubleVar()
        self.total.set(0)
        self.tax = DoubleVar()
        self.listitems = [(StringVar(), StringVar()) for i in range(len(AllItemsPrices))]
        self.index = 0

    def add(self, price):
        self.total.set("{:.2f}".format(self.total.get() + price))
        self.tax.set("{:.2f}".format(self.total.get() * .08))  # tax
        return self.total

    def reset(self):
        self.total.set(0)
        self.tax.set(0)
        for i in self.listitems:
            i[0].set("")
            i[1].set("")
        self.index = 0

    def addtolist(self, product, price):
        self.listitems[self.index][0].set(product)
        self.listitems[self.index][1].set(price)
        self.index += 1


Total = Counter()

products1 = list(AllItemsPrices)
itemList = {}


################ CREATE FUNCTION TO TRACK CHECKED ITEMS #################################################
# Credit: https://www.tutorialspoint.com/how-do-i-get-an-event-callback-when-a-tkinter-entry-widget-is-modified
def callback():
    print("================")
    Total.reset()
    for item1 in itemList:
        if itemList[item1].get() == 1:
            print("Item: " + item1)
            print(AllItemsPrices[item1])
            Total.add(AllItemsPrices[item1])
            Total.addtolist(item1, AllItemsPrices[item1])
    print("Total.Total " + str(Total.total.get()))


#################################################################
# MENU ITEMS for ENTRE'S

Label(tab1).grid(column=0, row=0)


for i in range(0, len(MenuItemsPrice0)):
    prod1 = products1[i]
    # print(prod1)
    var = IntVar()
    itemList[prod1] = var
    cb = Checkbutton(tab1, text=prod1,
                     variable=var, onvalue=1, offvalue=0, height=1, anchor=W, width=37, command=callback)
    cb.grid()

#################################################################
# MENU ITEMS for SIDES

Label(tab2).grid(column=0, row=0)
products = list(MenuItemsPrice1)

for i in range(0, len(MenuItemsPrice1)):
    prod2 = products[i]
    # print(prod2)
    var = IntVar()
    itemList[prod2] = var
    cb = Checkbutton(tab2, text=prod2,
                     variable=var, onvalue=1, offvalue=0, height=1, anchor=W, width=37, command=callback)
    cb.grid()
#################################################################
# MENU ITEMS for DRINKS

Label(tab3).grid(column=0, row=0)
products = list(MenuItemsPrice2)

for i in range(0, len(MenuItemsPrice2)):
    prod3 = products[i]
    # print(prod3)
    var = IntVar()
    itemList[prod3] = var
    cb = Checkbutton(tab3, text=prod3,
                     variable=var, onvalue=1, offvalue=0, height=1, anchor=W, width=37, command=callback)
    cb.grid()
#################################################################
# MENU ITEMS for DESERTS

Label(tab4).grid(column=0, row=0)
products = list(MenuItemsPrice3)

for i in range(0, len(MenuItemsPrice3)):
    prod4 = products[i]
    # print(prod4)
    var = IntVar()
    itemList[prod4] = var
    cb = Checkbutton(tab4, text=prod4,
                     variable=var, onvalue=1, offvalue=0, height=1, anchor=W, width=37, command=callback)
    cb.grid()


####################### COUNTER TABLE  ###########################################
# Credit: https://blog.teclado.com/tkinter-scrollable-frames/
class ScrollableFrameB(ttk.Frame):
    def __init__(self, container, *args, **kwargs):
        super().__init__(container, *args, **kwargs)
        canvas = Canvas(self, width=380, height=260)
        scrollbar = ttk.Scrollbar(self, orient="vertical", command=canvas.yview)
        self.scrollable_frame = ttk.Frame(canvas)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )

        canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")

        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")


products = Total.listitems
total_rows = len(products)
total_columns = 2


# Table class
# Credit: https://stackoverflow.com/questions/22645041/tkinter-how-to-use-scrollbar-in-a-popup-top-level-window-that-opens-when-a-butt
class Table:
    def __init__(self, scrollableframe):
        for i in range(total_rows):
            for j in range(total_columns):
                self.entry = Entry(scrollableframe.scrollable_frame, textvariable=products[i][j],
                                   state='disabled', disabledforeground='black', bg='white',
                                   disabledbackground='white', font='black')

                self.entry.grid(row=i + 1, column=j)
                # self.entry.insert(END, products[i][j])


tableFrame = Frame(root)
tableFrame.grid(row=5, column=0, rowspan=1, columnspan=1, sticky='nw')

scrollableframe = ScrollableFrameB(tableFrame)
scrollableframe.grid(row=8, column=0, columnspan=2, sticky='nw', rowspan=2)

MenuItem = StringVar()
MenuItem.set("Menu Item")
totalValue = Entry(tableFrame, disabledforeground='black', disabledbackground='lightgray', textvariable=MenuItem,
                   state='disabled')
totalValue.grid(row=0, column=0)

MenuItem = StringVar()
MenuItem.set("Price")
totalValue = Entry(tableFrame, disabledforeground='black', disabledbackground='lightgray', textvariable=MenuItem,
                   state='disabled')
totalValue.grid(row=0, column=1)

Table(scrollableframe)
######################## PICTURE FRAME ##########################################
pictureFrame = Frame()
pictureFrame.grid(row=5, column=3, columnspan=1, sticky='nw')
img = PhotoImage(file='restaurantimage.png')
Label(pictureFrame, image=img).pack()
#################################################################
# TOTAL FRAME
priceFrame = LabelFrame(root, text="Pay This Amount")
priceFrame.grid(row=0, column=3, columnspan=1, rowspan=1, sticky='news')

totallabela = Label(priceFrame, text="Total: ")
totallabela.grid(row=0, column=0, padx=30)
totalValue = Entry(priceFrame, disabledforeground='black', bg='white', textvariable=Total.total, state='disabled')
totalValue.grid(row=0, column=1)

taxlabel = Label(priceFrame, text="Tax: ")
taxlabel.grid(row=1, column=0)
taxValue = Entry(priceFrame, disabledforeground='black', bg='white', textvariable=Total.tax, state='disabled')
taxValue.grid(row=1, column=1)

root.mainloop()
