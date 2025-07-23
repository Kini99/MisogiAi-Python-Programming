price1=int(input("Enter price of item 1: "))
quantity1=int(input("Enter quantity of item 1: "))
price2=int(input("Enter price of item 2: "))
quantity2=int(input("Enter quantity of item 2: "))
price3=int(input("Enter price of item 3: "))
quantity3=int(input("Enter quantity of item 3: "))
subtotal = {price1 * quantity1 + price2 * quantity2 + price3 * quantity3}
tax={price1 * quantity1 + price2 * quantity2 + price3 * quantity3}*8.5/100

print(f"""
Item 1: {price1} x {quantity1} = {price1 * quantity1}
Item 2: {price2} x {quantity2} = {price2 * quantity2}
Item 3: {price3} x {quantity3} = {price3 * quantity3}
Subtotal: {subtotal}
Tax (8.5%): {tax}
Total:{subtotal+tax}
""")