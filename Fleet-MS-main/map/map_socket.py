import socketio
import os
from utils.mongo_connection import sim_collection

REDIS_URL = os.environ.get("REDIS_URL", "redis://127.0.0.1:6379")

mgr = socketio.AsyncRedisManager(REDIS_URL)
sio = socketio.AsyncServer(
    async_mode="asgi", client_manager=mgr, cors_allowed_origins="*"
)


# establishes a connection with the client
@sio.event
async def connect(sid, env):
    if env:
        print("connect", f"Connected with auth as {sid}")
    else:
        # raise ConnectionRefusedError("No auth")
        pass


# listening to a 'message' event from the client
@sio.event
async def print_message(sid, data):
    await sio.emit("new_message")
    return "welcome back from server"

@sio.event
async def disconnect(sid):
    print("SocketIO disconnect")


@sio.event
def get_sim_status(sid):
    sim_status = False
    sim = sim_collection.find_one({})
    if sim :
        sim_status = sim.get("sim_status")
    return sim_status