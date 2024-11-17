import asyncio
import logging
import random
import os
from dotenv import load_dotenv
from livekit import rtc, api

# Load environment variables
load_dotenv()

WIDTH = 640
HEIGHT = 480

async def main():
    # Retrieve environment variables
    livekit_url = os.getenv("LIVEKIT_URL")
    api_key = os.getenv("LIVEKIT_API_KEY")
    api_secret = os.getenv("LIVEKIT_API_SECRET")
    room_name = os.getenv("ROOM_NAME")
    participant_identity = os.getenv("PARTICIPANT_IDENTITY")

    # Create a VideoGrants with room join permission
    grant = api.VideoGrants(room_join=True, room=room_name)

    # Generate the access token
    token = (
        api.AccessToken(api_key, api_secret)
        .with_identity(participant_identity)
        .with_grants(grant)
        .to_jwt()
    )

    # Initialize the room
    room = rtc.Room()

    # Connect to the room using the URL and token
    await room.connect(livekit_url, token)
    logging.info(f"Connected to room: {room_name}")

    # Create a video source and track
    source = rtc.VideoSource(WIDTH, HEIGHT)
    track = rtc.LocalVideoTrack.create_video_track("single-color", source)
    options = rtc.TrackPublishOptions(source=rtc.TrackSource.SOURCE_CAMERA)
    publication = await room.local_participant.publish_track(track, options)
    logging.info(f"Published track with SID: {publication.sid}")

    async def _draw_color():
        argb_frame = bytearray(WIDTH * HEIGHT * 4)
        while True:
            await asyncio.sleep(0.1)  # 100ms

            # Create a new random color
            r, g, b = [random.randint(0, 255) for _ in range(3)]
            color = bytes([r, g, b, 255])

            # Fill the frame with the new random color
            argb_frame[:] = color * WIDTH * HEIGHT
            frame = rtc.VideoFrame(WIDTH, HEIGHT, rtc.VideoBufferType.RGBA, argb_frame)
            source.capture_frame(frame)

    await _draw_color()

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())

