# Locomotion Tracker

A project developed by Olimpia Rosales and Andrés Gómez for gait analysis data acquisition with support for multiple video formats

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to ***install the requirements***.

```bash
pip install opencv-contrib-python numpy
```
Next, clone this repository to your PC and you're done

## Usage

First, you have to copy the video you want to analyze to the root folder of the repo.

Next step is to run this command from your terminal:
```bash
python main.py
```
Once it runs, the program will ask you the name of the video, you have to type it with the extension, **I.e: example.mp4**

## Results
Once it finishes, you'll end up with a .csv document with the coordinates for every joint and a folder with all the frames of the video in the video in the original resolution

## License
This project is licensed under the GNU License - see the [LICENSE.md](LICENSE.md) file for details
