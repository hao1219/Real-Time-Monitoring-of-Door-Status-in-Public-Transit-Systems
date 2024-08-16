# Real-Time-Monitoring-of-Door-Status-in-Public-Transit-Systems

The frame count for the door opening and closing process can be determined.

## Directory
```
R12942102/
├── data_handler/
│   ├── dataset/
│   │   ├── 01.mp4
│   │   ├── 02.mp4
│   │   └── 03.mp4
│   ├── generate_frame.py
│   ├── generate_labels.py
│   └── train_val_test.py
├── Tests/
│   ├── 01.mp4
│   ├── 03.mp4
│   ├── 05.mp4
│   ├── 07.mp4
│   └── 09.mp4
├── yolov5/
│   ├── best.pt
├── dataset.yaml
├── directory_tree.md
├── generate_result.py
├── README.md
├── requirements.txt
├── run.sh*
└── thresholding.py
```

## Requirments
```bash
pip install -r requirements.txt 
```
## Training model (optional)
Ｔhis part is for generating traing data and implementing training process
```bash
- chmod +x run.sh
- ./run.sh
```

## Generate output.json (optional)
To generate the result, run the following command in your terminal:
```bash
python python generate_result.py
```
The output will be under R12942102 folder
