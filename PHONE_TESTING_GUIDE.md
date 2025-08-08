# 📱 Phone Testing Guide

This guide will help you test the Camera Motion Receiver add-on using your phone as a remote control.

## 🚀 Quick Start

### Method 1: Using the Phone Server (Recommended)

1. **Start the phone server:**
   ```bash
   python3 phone_server.py
   ```

2. **On your phone:**
   - Open your web browser
   - Go to the URL shown by the phone server (e.g., `http://192.168.1.100:8000/phone_test.html`)
   - Make sure your phone is on the same WiFi network as your computer

3. **In the phone app:**
   - Enter your computer's IP address (shown by the phone server)
   - Enter port: `8765`
   - Click "Connect"

4. **In Blender:**
   - Enable the Camera Motion Receiver add-on
   - The WebSocket server should start automatically

5. **Test the connection:**
   - Use the sliders to move the camera
   - Try the "Auto Motion" feature
   - Watch the camera move in Blender!

### Method 2: Manual Setup

1. **Find your computer's IP address:**
   ```bash
   # On macOS/Linux
   ifconfig | grep "inet " | grep -v 127.0.0.1
   
   # On Windows
   ipconfig | findstr "IPv4"
   ```

2. **Start the WebSocket server in Blender:**
   - Enable the add-on
   - Or manually start it from the UI panel

3. **On your phone:**
   - Open the `phone_test.html` file in your browser
   - Enter your computer's IP address
   - Enter port: `8765`
   - Click "Connect"

## 🔧 Network Setup

### Same Network Required
Both your computer and phone must be on the same WiFi network.

### Firewall Settings
Make sure port 8765 is not blocked by your firewall:

**macOS:**
- System Preferences → Security & Privacy → Firewall
- Add Python/Blender to allowed applications

**Windows:**
- Windows Defender Firewall → Allow an app through firewall
- Add Python/Blender to allowed applications

**Linux:**
```bash
sudo ufw allow 8765
```

### Finding Your IP Address

**macOS/Linux:**
```bash
ifconfig | grep "inet " | grep -v 127.0.0.1
```

**Windows:**
```bash
ipconfig | findstr "IPv4"
```

## 📱 Phone App Features

The phone test app includes:

- **Connection Settings:** Enter server IP and port
- **Position Controls:** X, Y, Z position sliders
- **Rotation Controls:** X, Y, Z rotation sliders (in radians)
- **Action Buttons:**
  - Send Camera Data: Send current slider values
  - Reset Camera: Move camera to origin (0,0,0)
  - Start Auto Motion: Automatic circular motion
  - Stop Auto Motion: Stop automatic motion
- **Activity Log:** Shows connection status and sent data

## 🎯 Testing Scenarios

### Basic Testing
1. Connect your phone to the server
2. Use the position sliders to move the camera
3. Use the rotation sliders to rotate the camera
4. Watch the camera move in Blender

### Auto Motion Testing
1. Click "Start Auto Motion"
2. Watch the camera move in a circular pattern
3. Click "Stop Auto Motion" to stop

### Reset Testing
1. Move the camera to a random position
2. Click "Reset Camera"
3. Verify the camera returns to origin (0,0,0)

### Network Testing
1. Try connecting from different devices
2. Test with multiple phones simultaneously
3. Verify the camera responds to all connected devices

## 🔍 Troubleshooting

### Connection Issues

**"Connection refused"**
- Make sure the WebSocket server is running in Blender
- Check that port 8765 is not blocked by firewall
- Verify both devices are on the same network

**"Cannot connect to server"**
- Check your computer's IP address
- Make sure the phone and computer are on the same WiFi
- Try using the computer's IP instead of localhost

**"WebSocket connection failed"**
- The add-on might be using the simple socket server
- Try restarting Blender and the add-on
- Check the Blender system console for error messages

### Camera Issues

**"No active camera in scene"**
- The add-on will automatically create a camera
- Check the Blender system console for messages

**"Camera not moving"**
- Check the activity log in the phone app
- Verify data is being sent successfully
- Check the Blender system console for error messages

### Performance Issues

**"Laggy camera movement"**
- Reduce the update frequency
- Close other applications using the network
- Check your WiFi signal strength

**"High CPU usage"**
- The auto motion feature can be CPU intensive
- Stop auto motion when not testing
- Close other applications

## 📊 Debug Information

### Blender Console
Check Blender's system console for:
- Server start/stop messages
- Received camera data
- Error messages
- Connection information

### Phone App Log
The phone app shows:
- Connection status
- Sent data
- Error messages
- Server responses

### Network Debugging
```bash
# Test if port 8765 is open
telnet YOUR_IP_ADDRESS 8765

# Check if the server is listening
netstat -an | grep 8765

# Test WebSocket connection
wscat -c ws://YOUR_IP_ADDRESS:8765
```

## 🎮 Advanced Usage

### Custom Data Format
The phone app sends JSON data in this format:
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

### Multiple Devices
You can connect multiple phones simultaneously:
- Each device will control the same camera
- The last received data will be applied
- All devices will see the same camera movement

### Custom Controls
Modify the phone app to add:
- Touch controls for direct manipulation
- Accelerometer/gyroscope input
- Custom motion patterns
- Camera presets

## 🚀 Next Steps

Once you've successfully tested the basic functionality:

1. **Create custom motion patterns**
2. **Add touch controls for direct manipulation**
3. **Integrate with motion sensors (accelerometer/gyroscope)**
4. **Add camera presets and keyframes**
5. **Create a native mobile app**
6. **Add support for multiple cameras**

## 📞 Support

If you encounter issues:

1. Check the troubleshooting section above
2. Review the debug information in Blender's console
3. Test with the included `test_client.py` first
4. Verify your network setup
5. Check that all required files are present

The phone testing feature provides a great way to test the add-on's real-time capabilities and can be extended for more advanced use cases.
