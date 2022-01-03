f = open("paris/network_combined.csv", 'r')
next(f)
for line in f:
    items = line.rstrip("\n").split(";")
    routes = items[5].split(",") #splitting the route_I_counts column to take the different routes and counts
    for x in routes:
        x = x.split(":") #splitting {route_I:count} (used to isolate the route_I's)
        print(f"INSERT INTO itinerary VALUES ( {x[0]}, {items[6]}, {items[3]}, {items[2]}, {items[0]}, {items[1]}", end='')
        print(");")

#==> paris/network_combined.csv <==
#from_stop_I;to_stop_I;d;duration_avg;n_vehicles;route_I_counts;route_type

# 31 ;  272 ; 496 ; 69.91304347826087 ; 460 ; 37:230,38:230 ; 1
# {37:230} , {38:230}
# De Varenne à Invalides, le trajet de distance 496 dure 69  et peut être effectué à l'aide des routes 37 et 38
