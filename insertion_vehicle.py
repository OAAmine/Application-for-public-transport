f = open("paris/Paris-routeI-routeName-routeType.csv", 'r')
next(f)
for line in f:
    items = line.rstrip("\n").split(";")
    # handling of the possible non-ASCII characters
    items[1] = items[1].replace("'", "''")
    items[1] = items[1].replace("é", "e")
    items[1] = items[1].replace("è", "e")
    items[1] = items[1].replace("ê", "e")
    items[1] = items[1].replace("à", "a")
    items[1] = items[1].replace("â", "a")
    items[1] = items[1].replace("ô", "o")
    items[1] = items[1].replace("ù", "u")
    items[1] = items[1].replace("î", "i")
    items[1] = items[1].replace("ç", "c")
    
    print(f"INSERT INTO vehicle VALUES ( {items[0]}, \'{items[1]}\', {items[2]}", end='')
    print(");")

#==> paris/Paris-routeI-routeName-routeType.csv <==
#route_I;route_name;route_type