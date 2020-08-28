from pymavlink import mavutil

master = mavutil.mavlink_connection('udpin:0.0.0.0:14550')
master.wait_heartbeat()

#print("{} messages recieved \n".format(len(master.messages.keys())))

#master.messages returns a dictionary, with message types as keys and message data as values
#printing out the keys prints all the message types that are being recieved
print(master.messages.keys())
print("\n")

#to get info of a particular message (or) to recieve real time values of a message
#use the message type as key to the dictionary to get the real time values (eg 'BATTERY_STATUS')
#print(master.messages['BATTERY_STATUS'])