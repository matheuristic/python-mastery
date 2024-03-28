def portfolio_cost(filename):
    cost = 0.
    with open(filename, 'r') as f:
        for line in f:
            try:
                ticker, qty, price = line.split()  # destructuring assignment
                qty = int(qty)
                price = float(price)
                cost += qty * price
            except ValueError as e:
                line_clean = line.replace('\n', '\\n')
                print(f"Couldn't parse: '{line_clean}'")
                print(f"Reason: {str(e)}")
    return cost


if __name__ == '__main__':
    print(portfolio_cost('Data/portfolio.dat'))
    #print(portfolio_cost('Data/portfolio3.dat'))
