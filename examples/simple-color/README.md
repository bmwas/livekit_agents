# Simple-color

This small exmple publishes a solid color video frame.

# LiveKit Python Streaming Example

This project demonstrates how to stream video and audio to a specific room using the LiveKit Python SDK.

## Prerequisites

- Python 3.6 or later installed on your system.
- Access to a LiveKit server (either self-hosted or via LiveKit Cloud).

## Setup Instructions

1. **Clone the Repository**

   ```bash
   git clone https://github.com/yourusername/livekit-python-streaming.git
   cd livekit-python-streaming
   ```

2. **Create a Virtual Environment (Optional but Recommended)**

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Required Packages**

   ```bash
   pip install -r requirements.txt
   ```

   The `requirements.txt` file includes:

   ```
   livekit
   livekit-api
   python-dotenv
   numpy
   ```

4. **Configure Environment Variables**

   Create a `.env` file in the project's root directory with the following content:

   ```
   LIVEKIT_URL=your_livekit_server_url
   LIVEKIT_API_KEY=your_api_key
   LIVEKIT_API_SECRET=your_api_secret
   ROOM_NAME=your_room_name
   PARTICIPANT_IDENTITY=your_identity
   ```

   Replace the placeholders with your actual LiveKit server URL, API credentials, desired room name, and a unique participant identity.

5. **Run the Script**

   ```bash
   python app.py dev
   ```

   This script connects to the specified LiveKit room and publishes both video and audio tracks. The video displays a single color that changes every 100 milliseconds, and the audio generates random sine wave tones between 200Hz and 1000Hz.

6. **View the Stream**

   To view the published video and audio tracks, join the same LiveKit room using a compatible client application, such as the [LiveKit React Example App](https://github.com/livekit/livekit-react-example). Ensure the client connects to the same `LIVEKIT_URL` and `ROOM_NAME` specified in your `.env` file.

## Notes

- Ensure your LiveKit server is running and accessible.
- The room specified in `ROOM_NAME` should exist or be created as needed.
- The `PARTICIPANT_IDENTITY` should be unique for each participant.

For more information, refer to the [LiveKit Python SDK documentation](https://docs.livekit.io/python/livekit/index.html). 
