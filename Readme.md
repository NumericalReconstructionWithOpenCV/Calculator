## Project Setting
- Python `2.7.13`
- Pycharm `Version 2016.1.5 (build 145.2073.10) November 18th, 2016`
- OpenCV Python `3.2.0.6`

## Pip
`sudo pip install unittest2`

`sudo pip install opencv-python>=3.2.0.6`

## Project Structure
```
.
├── Core
│   ├── ColorDetect.py
│   ├── FindCorner.py
│   ├── FindCorner.pyc
│   ├── GetContour.py
│   ├── GetContour.pyc
│   ├── ImageMatrixMove.py
│   ├── ImageMatrixMove.pyc
│   ├── ObjectDetect.py
│   ├── ObjectDetect.pyc
│   ├── ShapeDetectAndFindCorner.py
│   ├── ShapeDetectAndFindCorner.pyc
│   ├── __init__.py
│   └── __init__.pyc
├── ProgramMain.py
├── Readme.md
├── Setting
│   ├── DefineManager.py
│   ├── DefineManager.pyc
│   ├── __init__.py
│   └── __init__.pyc
├── Tests
│   ├── testcase0
│   │   ├── End.png
│   │   ├── afterImage.png
│   │   └── beforeImage.png
│   ├── testcase1
│   │   ├── after.jpg
│   │   ├── before.jpg
│   │   └── result.jpg
│   ├── testcase2
│   │   ├── after.JPG
│   │   ├── before.JPG
│   │   ├── result_absdiff.jpg
│   │   └── result_canny.jpg
│   ├── testcase3
│   │   ├── after.jpg
│   │   ├── before.JPG
│   │   └── result.jpg
│   ├── testcase4
│   │   ├── after.JPG
│   │   ├── before.JPG
│   │   ├── result_absdiff.jpg
│   │   ├── result_diff2.jpg
│   │   └── result_mask.jpg
│   ├── testcase5
│   │   ├── BeforeWithBlur.jpg
│   │   ├── BeforeWithoutBlur.jpg
│   │   ├── ContourImage.png
│   │   ├── Morphology.png
│   │   ├── WithBlur.jpg
│   │   ├── WithoutBlur.jpg
│   │   ├── after.jpg
│   │   ├── afterCut.jpg
│   │   ├── before.jpg
│   │   ├── beforeCut.jpg
│   │   ├── result_absdiff.jpg
│   │   ├── result_absdiff_Gray.jpg
│   │   ├── result_absdiff_bak.jpg
│   │   ├── result_canny.jpg
│   │   ├── result_diff2.jpg
│   │   └── result_mask.jpg
│   ├── testcase6
│   │   ├── after.jpg
│   │   ├── before.jpg
│   │   ├── result_absdiff.jpg
│   │   ├── result_diff2.jpg
│   │   ├── result_mask.jpg
│   │   └── ?\204\213?\205??\206??\204\207?\205??\206?
│   │       ├── after.jpg
│   │       └── before.jpg
│   └── testcase7
│       ├── after.JPG
│       ├── before.JPG
│       ├── result_absdiff.jpg
│       ├── result_corner.jpg
│       ├── result_diff2.jpg
│       ├── result_mask.jpg
│       └── ?\204\213?\205??\206??\204\207?\205??\206?
│           ├── IMG_0096.JPG
│           ├── IMG_0097.JPG
│           ├── IMG_0099.JPG
│           ├── IMG_0100.JPG
│           ├── IMG_0101.JPG
│           ├── IMG_0102.JPG
│           ├── IMG_0103.JPG
│           ├── IMG_0104.JPG
│           ├── IMG_0105.JPG
│           ├── IMG_0106.JPG
│           └── IMG_0107.JPG
└── Utils
    ├── CustomOpenCV.py
    ├── CustomOpenCV.pyc
    ├── FileIO.py
    ├── FileIO.pyc
    ├── FilteringNoiseAndLighting.py
    ├── LogManager.py
    ├── LogManager.pyc
    ├── __init__.py
    └── __init__.pyc

14 directories, 86 files
```