import socketio
import asyncio

sio = socketio.AsyncClient()

async def main():
    await sio.connect('http://localhost:5000')
    print("mysid",sio.sid)
    await sio.wait()
@sio.event
async def connect():
    print("connected")
    await sio.emit("login",{"login":"lg","password":"psw"})
    print("msg sent")
@sio.event
async def login_response(id):
    print("my id is", id)




if __name__ == "__main__":
    asyncio.run(main())
    pass