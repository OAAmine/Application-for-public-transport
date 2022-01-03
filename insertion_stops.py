f = open("paris/network_nodes.csv", 'r')
next(f)
for line in f:
    items = line.rstrip("\n").split(";")
    temp = "\'" + str(items[1]) + "," + str(items[2]) + "\'"
    items[3] = items[3].replace("'", "''")
    items[3] = items[3].replace("é", "e")
    items[3] = items[3].replace("è", "e")
    items[3] = items[3].replace("ê", "e")
    items[3] = items[3].replace("à", "a")
    items[3] = items[3].replace("â", "a")
    items[3] = items[3].replace("ô", "o")
    items[3] = items[3].replace("ù", "u")
    items[3] = items[3].replace("î", "i")
    items[3] = items[3].replace("ç", "c")
    
    print(f"INSERT INTO stops VALUES ( {items[0]}, \'{items[3]}\', {temp}", end='')
    print(");")

#==> paris/network_nodes.csv <==
#stop_I;lat;lon;name