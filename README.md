# HandWaveHaven
 Hand Gesture based Home Automation System

This project enables home automation using hand gestures. It detects hand gestures indicating the number of fingers pointed up and performs various actions accordingly.

## Project Overview

The system detects the following hand gestures based on the number of fingers pointing up:

- Gesture 0: Switch Off Devices
- Gesture 1: Switch On Lights
- Gesture 2: Control Volume
- Gesture 3: Get Temperature Values
- Gesture 4: Face Recognition

## Installation

To run this project, you need to have the following Python packages installed:

- cv2
- mediapipe
- Arduino
- gTTS

You can install these packages using pip:

```bash
pip install -r requirements.txt
```

## Usage

To interact with the system, run the `FingerCounter.py` file. You can find the file [here](https://github.com/anand3eight/HandWaveHaven/blob/main/HandTracker/FingerCounter.py).

## Configuration

This project is configured to work on MacBooks by default. However, it can be adapted for other systems with minimal changes.

## Contributing

Contributions to this project are welcome! Feel free to fork the repository, make changes, and submit pull requests.
