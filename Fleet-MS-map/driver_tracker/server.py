import uvicorn

if __name__ == "__main__":
    uvicorn.run("driver_tracker.asgi:application", reload=True, port=7000)
