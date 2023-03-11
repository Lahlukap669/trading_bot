def calculate(rate, days, money):
    moneysum = money
    for i in range(days):
        if(i%4==0):
            continue
        moneysum+=moneysum*(rate/100)
    return moneysum

money=int(input("Vnesi vsoto vloženega denarja"))
rate=int(input("Vnesi odstotek zaslužka dnevno"))
days=int(input("Vnesi število dni prižganega bota"))

print("Glede na vloženih", money, ", dnevnim zaslužkom", rate, "% in botom zagnanim", days, "dni je zaslužek ", calculate(rate, days, money))
