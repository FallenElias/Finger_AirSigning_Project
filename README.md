<h1 align="center">Airwriting Signature</h1>

<div align="center">

</div>

---

## 📝 Table of Contents

* [About](#about)
* [Project Structure](#structure)
* [Getting Started](#getting_started)
* [Usage](#usage)
* [Authors](#authors)

## 🔎 About <a name = "about"></a>

This project aims to develop a contactless and secure way to sign documents in response to the COVID-19 pandemic. It will create an application that uses computer vision techniques to identify finger-based signatures, with the objectives of accurately identifying and transcribing finger-based signatures and creating a user-friendly interface for signature creation and storage. The application will operate on both desktop and mobile devices and will be developed using existing technologies and frameworks such as OpenCV and TensorFlow. Other potential technologies that may be used include Unity, and Qt. The completed application will contribute to the field of computer vision and image processing and will provide a useful tool for individuals and organizations seeking a secure and contactless way to sign documents.

## 🔧 Project Structure <a name = "structure"></a>

```
/Finger_AirSigning_Project/
├── cameraLens.py           Initial program.
├── main.png                Hand picture.
├── README.md               Project overview and outline.
└── requirement.txt         Setup configuration of the Python package.
```

## 🏁 Getting Started <a name = "getting_started"></a>

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

In order to use this project, you will need to have the following software and libraries installed:  
* Python
* Git
* Mediapipe
* OpenCV
* NumPy
* Imutils


### Installing

To get started with this project, clone the repository to your local machine and install the required dependencies.

```bash
git clone https://github.com/FallenElias/Finger_AirSigning_Project.git
cd Finger_AirSigning_Project
pip install -r requirements.txt
```

## 🚀 Usage <a name = "usage"></a>

### CLI usage

To run the depth estimation stream, simply execute the following command:

```bash
python cameraLens.py
```

- The camera starts up
- Place your hand in the model for calibration
- CLick "Start" to confirm the calibration
- Make your signature
- When finished press "Save" to finish signing

## ⛏️ Built Using <a name = "built_using"></a>
![PyTorch](https://img.shields.io/badge/PyTorch-1.13.0-orange?style=for-the-badge&logo=pytorch&logoColor=orange) ![OpenCV](https://img.shields.io/badge/OpenCV-4.6.0-orange?style=for-the-badge&logo=opencv&logoColor=orange) ![NumPy](https://img.shields.io/badge/numpy-1.23.4-orange?style=for-the-badge&logo=numpy&logoColor=orange) ![MediaPipe](https://img.shields.io/badge/MEDIAPIPE-0.9.2.1-orange?style=for-the-badge&logo=google&logoColor=orange)

## ✍️ Authors <a name = "authors"></a>

- [Kelig Lefeuvre](https://github.com/keligggg)
- [Elias Dève](https://github.com/FallenElias)
- [Quentin Amiel](https://github.com/quentinaml)
- [Enzo Cogneville](https://github.com/lenzone91)
- [Augustin Mascarelli](https://github.com/augustinmascarelli)
- [Yona Bitton](https://github.com/yonabitton)
