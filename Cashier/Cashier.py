def enterProducts(): #Here we got the Cashier to input all the products bought one by one. We stored all that info in a dictionary called "buyingData" and returned it back
    buyingData = {}
    enterDetails=True
    while enterDetails:
        details=input('Press A to add product and Q to quit:')
        if details=="A":
            product=input("Enter product:")
            quantity=int(input("Enter quantity:"))
            buyingData.update({product:quantity})
        elif details=="Q":
            enterDetails=False
        else:
            print("Please select a correct option")
    return buyingData

def getPrice(product,quantity): #The job of this function is to give the subtotal of a single product as per its price and quantity mentioned.
    priceData={
    'Biscuit': 30,
    'Chicken': 250,
    'Egg': 10,
    'Fish': 200,
    'Coke': 50,
    'Bread': 30,
    'Apple': 350,
    'Onion': 55
    }
    subtotal=priceData[product]*quantity
    print(product + ':₹' + str(priceData[product]) + 'x' + str(quantity) + '=' + str(subtotal))
    return subtotal

def getDiscount(billAmount,membership): #Here, as per the total bill amount we decide the discount is applicable or not.
    discount=0
    if billAmount>=25:
        if membership=='Gold':
            billAmount=billAmount*0.95
            discount=5
        elif membership=='Silver':
            billAmount=billAmount*0.97
            discount=3
        elif membership=='Bronze':
            billAmount=billAmount*0.99
            discount=1
        print(str(discount) +"% off for "+ membership +' '+'membership on total amount: ₹'+str(billAmount))
    else:
        print('No discount on amount less than ₹25')
    return billAmount

def makeBill(buyingData,membership): #loop starts: Call getPrice until subtotal is added for all products within buyingData,end buy calling getDiscount.
    billAmount=0
    for key, value in buyingData.items():
        billAmount+=getPrice(key,value)
    billAmount=getDiscount(billAmount,membership)
    print('The discounted amount is ₹'+str(billAmount))

buyingData=enterProducts()
membership=input('Enter customer membership:')
makeBill(buyingData,membership)