# Camera Motion Receiver - Blender Add-on

A Blender 3.3+ add-on that receives camera motion data via WebSocket and applies it to the active camera in the current scene.

## Features

- 🎯 **WebSocket Server**: Starts a WebSocket server on localhost:8765 when enabled
- 📡 **Real-time Data**: Receives JSON camera motion data in real-time
- 🎥 **Camera Control**: Moves and rotates the active camera based on received data
- 🛡️ **Error Handling**: Graceful error handling for malformed data or missing cameras
- 🎮 **UI Controls**: Manual start/stop controls from Blender's UI
- 🔄 **Auto Cleanup**: Automatically shuts down the server when the add-on is disabled

## Installation

1. **Download the add-on files** to a folder named `camera_motion_receiver`
2. **Zip the folder** to create `camera_motion_receiver.zip`
3. **Install in Blender**:
   - Open Blender
   - Go to Edit > Preferences > Add-ons
   - Click "Install..." and select the zip file
   - Enable the add-on by checking the box

## Usage

### Basic Usage

1. **Enable the add-on** in Blender's Preferences
2. **Open the Camera Motion panel** in the 3D Viewport sidebar (N-key)
3. **Start the server** using the "Start Server" button
4. **Send camera data** to localhost:8765 using the JSON format below

### JSON Data Format

The add-on expects JSON data in this format:

```json
{
    "X": 0.0,
    "Y": 0.0,
    "Z": 0.0,
    "ROT_X": 0.0,
    "ROT_Y": 0.0,
    "ROT_Z": 0.0
}
```

**Parameters:**
- `X`, `Y`, `Z`: Camera position in Blender units
- `ROT_X`, `ROT_Y`, `ROT_Z`: Camera rotation in radians

### Testing

### Desktop Testing

Use the included `test_client.py` to test the add-on:

```bash
python test_client.py
```

The test client provides options to:
- Send animated camera motion
- Send a sequence of test positions
- Send individual camera positions

### Phone Testing

Test the add-on with your phone as a remote control:

1. **Start the phone server:**
   ```bash
   python3 phone_server.py
   ```

2. **On your phone:**
   - Open your web browser
   - Go to the URL shown by the phone server
   - Make sure your phone is on the same WiFi network

3. **Connect and test:**
   - Enter your computer's IP address and port 8765
   - Use the sliders to control the camera
   - Try the "Auto Motion" feature

See `PHONE_TESTING_GUIDE.md` for detailed instructions.

## UI Panel

The add-on adds a panel to the 3D Viewport sidebar with:

- **Server Status**: Shows if the WebSocket server is running
- **Start/Stop Controls**: Manual server control buttons
- **Camera Information**: Displays current camera name, position, and rotation
- **Error Messages**: Shows warnings if no camera exists

## Technical Details

### Architecture

```
camera_motion_receiver/
├── __init__.py              # Main add-on file with UI and registration
├── websocket_server.py      # WebSocket server implementation
├── camera_controller.py     # Camera manipulation utilities
├── test_client.py           # Desktop test client
├── phone_test.html          # Phone web interface
├── phone_server.py          # HTTP server for phone testing
├── install.py               # Installation helper script
├── PHONE_TESTING_GUIDE.md  # Phone testing instructions
└── README.md               # This file
```

### Dependencies

The add-on uses only Python standard library modules available in Blender:
- `socket` for network communication
- `threading` for background server operation
- `json` for data parsing
- `bpy` for Blender integration

### Server Implementation

The add-on includes a fallback simple socket server if the WebSocket library is not available. The server:

1. **Listens on localhost:8765**
2. **Accepts JSON data** with camera motion information
3. **Validates the data** format and values
4. **Applies camera motion** in Blender's main thread
5. **Updates the viewport** to reflect changes

## Troubleshooting

### Common Issues

**"No active camera in scene"**
- Solution: The add-on will automatically create a camera if none exists

**"Failed to start server"**
- Check if port 8765 is already in use
- Try restarting Blender
- Check the system console for error messages

**"Invalid JSON data"**
- Ensure your JSON format matches the required structure
- Check that all values are numeric
- Verify the data is properly encoded as UTF-8

**"Connection refused"**
- Make sure the add-on is enabled and the server is running
- Check that you're connecting to localhost:8765
- Verify no firewall is blocking the connection

### Debug Information

The add-on provides debug output in Blender's system console:
- Server start/stop messages
- Received camera data
- Error messages for invalid data
- Camera position updates

## Development

### Adding New Features

1. **Modify `camera_controller.py`** for new camera operations
2. **Update `websocket_server.py`** for new data formats
3. **Extend `__init__.py`** for new UI elements
4. **Test with `test_client.py`** for validation

### Custom Data Formats

To support different data formats, modify the `on_message` function in `websocket_server.py`:

```python
def on_message(websocket, message):
    data = json.loads(message)
    # Add your custom parsing logic here
    # Then call camera_controller.apply_camera_motion(data)
```

## License

This add-on is provided as-is for educational and development purposes.

## Version History

- **v1.0.0**: Initial release with WebSocket server and camera control
- Basic UI panel with server controls
- JSON data format support
- Test client for development

## Contributing

Feel free to submit issues, feature requests, or pull requests to improve the add-on.

## Support

For issues or questions:
1. Check the troubleshooting section above
2. Review the debug output in Blender's system console
3. Test with the included test client
4. Verify your JSON data format matches the requirements
