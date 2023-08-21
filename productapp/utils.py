
def average_rate(rates):
    count = 0
    total = 0
    for i in rates:
        count += i.rate
        total += 1
    if count != 0:
        return round(count / total)
    else:
        return "No rating yet"


def calculate_discounted_price(product_price, sale_percentage):
    return product_price * (1 - sale_percentage / 100)
