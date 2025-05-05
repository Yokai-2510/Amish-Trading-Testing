import upstox_client
from rejson import Client, Path

REDIS_HOST = "localhost"
REDIS_PORT = 6379
REDIS_DB = 0
REDIS_PASSWORD = None
NIFTY_KEY = "NSE_INDEX|Nifty 50"

def get_access_token(redis_client):
    token = redis_client.jsonget("trading_setup", Path(".global_config.credentials.access_token"))
    if not token:
        raise ValueError("Access token not found")
    return token.strip()

def main():
    redis_client = Client(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB, password=REDIS_PASSWORD, decode_responses=True)
    access_token = get_access_token(redis_client)
    print(f"Connecting with token: {access_token[:10]}...")

    configuration = upstox_client.Configuration()
    configuration.access_token = access_token

    streamer = upstox_client.MarketDataStreamerV3(upstox_client.ApiClient(configuration))

    def on_open():
        streamer.subscribe([NIFTY_KEY], "full")
        print("Connected and subscribed to NIFTY 50")

    def on_message(message):
        print(f"Received: {message}")

    def on_error(error):
        print(f"Error: {error}")

    def on_close(ws=None, code=None, reason=None):
        print(f"Disconnected: {reason or 'No reason'}")

    streamer.on("open", on_open)
    streamer.on("message", on_message)
    streamer.on("error", on_error)
    streamer.on("close", on_close)

    streamer.connect()

if __name__ == "__main__":
    main()