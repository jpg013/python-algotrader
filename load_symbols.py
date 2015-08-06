from algotrader.database import database

if __name__ == "__main__":
    files = ["./nasdaqlisted.txt", "./otherlisted.txt"]

    for file in files:
        handle = open(file)
        for line in handle:
            splits = line.split("|")
            symbol = splits[0]
            if symbol.find("$") != -1:
                continue
            if symbol.find(".") != -1:
                continue
            symbol = {"symbol": symbol}
            database.saveSymbol(symbol)
