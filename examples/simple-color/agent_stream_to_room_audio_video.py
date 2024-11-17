import asyncio
import logging
import random
import os
import numpy as np
from dotenv import load_dotenv
from livekit import rtc, api

# Load environment variables
load_dotenv()

WIDTH = 640
HEIGHT = 480
SAMPLE_RATE = 48000
NUM_CHANNELS = 1
AMPLITUDE = 2 ** 8 - 1
SAMPLES_PER_CHANNEL = 480  # 10ms of audio at 48kHz

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

    # Create and publish video track
    video_source = rtc.VideoSource(WIDTH, HEIGHT)
    video_track = rtc.LocalVideoTrack.create_video_track("single-color", video_source)
    video_options = rtc.TrackPublishOptions(source=rtc.TrackSource.SOURCE_CAMERA)
    video_publication = await room.local_participant.publish_track(video_track, video_options)
    logging.info(f"Published video track with SID: {video_publication.sid}")

    # Create and publish audio track
    audio_source = rtc.AudioSource(SAMPLE_RATE, NUM_CHANNELS)
    audio_track = rtc.LocalAudioTrack.create_audio_track("random-tone", audio_source)
    audio_options = rtc.TrackPublishOptions(source=rtc.TrackSource.SOURCE_MICROPHONE)
    audio_publication = await room.local_participant.publish_track(audio_track, audio_options)
    logging.info(f"Published audio track with SID: {audio_publication.sid}")

    async def generate_video_frames():
        argb_frame = bytearray(WIDTH * HEIGHT * 4)
        while True:
            await asyncio.sleep(0.1)  # 100ms

            # Create a new random color
            r, g, b = [random.randint(0, 255) for _ in range(3)]
            color = bytes([r, g, b, 255])

            # Fill the frame with the new random color
            argb_frame[:] = color * WIDTH * HEIGHT
            frame = rtc.VideoFrame(WIDTH, HEIGHT, rtc.VideoBufferType.RGBA, argb_frame)
            video_source.capture_frame(frame)

    async def generate_audio_frames():
        total_samples = 0
        while True:
            await asyncio.sleep(0.01)  # 10ms

            # Generate a random frequency between 200Hz and 1000Hz
            frequency = random.uniform(200, 1000)

            # Create a sine wave for the given frequency
            time = (total_samples + np.arange(SAMPLES_PER_CHANNEL)) / SAMPLE_RATE
            sinewave = (AMPLITUDE * np.sin(2 * np.pi * frequency * time)).astype(np.int16)

            # Create an audio frame and capture it
            audio_frame = rtc.AudioFrame.create(SAMPLE_RATE, NUM_CHANNELS, SAMPLES_PER_CHANNEL)
            audio_data = np.frombuffer(audio_frame.data, dtype=np.int16)
            np.copyto(audio_data, sinewave)
            await audio_source.capture_frame(audio_frame)  # Await the coroutine

            total_samples += SAMPLES_PER_CHANNEL


    # Run both video and audio generation tasks concurrently
    await asyncio.gather(generate_video_frames(), generate_audio_frames())

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
