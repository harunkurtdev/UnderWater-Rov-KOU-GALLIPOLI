import asyncio
import  websockets
import numpy as np
listemiz =[]
async def response(websocket,path):

    message=await websocket.recv()
    # message=message.split("-")
    # for i in message:
    #     listemiz.append(i.split(":"))
    #
    #     print(len(listemiz))
    # #
    # # for j in listemiz:
    # #     print(j[0])
    # #     j.remove(0)
    # #     listemiz.append(j)



    print(message)

    #print("message : {}".format(message))
    #await websocket.send("Benim mesajım")

start_server=websockets.serve(response,"127.0.0.1",port=5553)
asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()