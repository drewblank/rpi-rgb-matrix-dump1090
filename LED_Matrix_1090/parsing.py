
flight_number = 'AAL4567'
altitude = 35000
speed = 150 
longitude = 42.4234
latitude = 86.2345


airline = flight_number[0:3]

if(airline == 'AAL'):
    print(airline)
elif(airline == 'UAL'):
    print(airline)
elif(airline == 'DAL'):
    print(airline)
elif(airline == 'SWA'):
    print(airline)
elif(airline == 'FDX'):
    print(airline)
elif(airline == 'UPS'):
    print(airline) 
else:
    print('Private Flight')
