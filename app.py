from fastapi import FastAPI
from starlette.responses import StreamingResponse, FileResponse
import uvicorn
import keyboard
import asyncio

app = FastAPI()
count = 0


def countUp():
    global count
    count += 1


def countDown():
    global count
    count -= 1


def resetCount():
    global count
    count = 0


keyboard.add_hotkey("enter", countUp)
keyboard.add_hotkey("delete", countDown)
keyboard.add_hotkey("home", resetCount)


async def event_generator():
    global count
    while True:
        yield f"data: {count}\n\n"
        await asyncio.sleep(1. / 60)


@app.get("/")
async def root():
    return FileResponse("index.html")


@app.get("/count")
async def returnCount():
    return StreamingResponse(event_generator(), media_type="text/event-stream")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)
