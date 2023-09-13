# drag-and-drop
This project is a Python-based drag and drop interaction system utilizing computer vision techniques. You can interact with digital elements and move them on your screen using hand gestures.

![Hand Indexes](hand_indexes.png)

## Table of Contents

- [Demo](#demo)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)

## Demo
Soon a quick demo would be here. Thanks for your patience!

## Features
- **Real-time Hand Tracking:** The project employs `mediapipe` for accurate hand tracking, allowing users to control the computer interface with their hands.
- **Interactive Elements:** Create interactive elements on the screen that respond to hand movements.
- **Multiple Objects:** Support for multiple draggable objects on the screen simultaneously.
- **Customizable:** Easily customize the size, appearance and behavior of draggable objects.
- **Easy Integration:** Integrate this system into your own projects to enable intuitive user interactions.

## Installation
### Getting Started:

1. Clone the repository to your local machine:
``` 
git clone <respository-url>
```
2. Install the requires dependencies:
```
pip install cv2 cvzone mediapipe numpy
```
3. Run the project and start experimenting with drag and drop interactions.

## Usage
Here is a quick explanation of how to use the application correctly:
1. Launch the application and a pop-up window should appear with your front camera. Remember you should give the application permission to use your camera.
2. Place any hand within the camera's view. This app can detect your two hands but only the one with the green frame, is the one that can control things.
3. Your **index finger** and **middle finger** would be your cursor. The object detect your fingers when you are on their area. When your finger tips are closed you can drag the object anywhere you want, if you open your fingers, you drop the object.
4. Experiment with dragging and dropping objects to explore project's capabilities.

## Contributing
Contributions to this project are welcome! Whether you're interested in fixing bugs, adding new features, or improving the documentation, your help is appreciated. 

Please contact me:
- [Github](https://github.com/leogzz0)
- [Linkedin](https://www.linkedin.com/in/leogzz0/)

## License
This project is licensed under the [MIT License](https://github.com/leogzz0/drag-and-drop/blob/main/LICENSE.md). Feel free to use, modify, and distribute this project in accordance with the terms of the license.
