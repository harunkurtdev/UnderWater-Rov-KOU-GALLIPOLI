import asyncio
import  websockets

async def message():
    while True:
        json=[]
        async with websockets.connect("ws://127.0.0.1:5554") as socket:

            msg0=input("mesage ilet  ")
            json.append(msg0)
            msg1 = input("mesage ilet  ")
            json.append(msg1)
            giden_mesaj="0:"+json[0]+"-"+"1:"+json[1]
            await socket.send(giden_mesaj)
            #print(await socket.recv())

asyncio.get_event_loop().run_until_complete(message())
asyncio.get_event_loop().run_forever()