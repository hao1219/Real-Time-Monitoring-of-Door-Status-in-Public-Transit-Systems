#!/bin/bash

# 检查并克隆 YOLOv5 仓库
if [ ! -d "yolov5" ]; then
    echo "Cloning YOLOv5 repository..."
    git clone https://github.com/ultralytics/yolov5 || { echo "Error: Cloning YOLOv5 repository failed!"; exit 1; }
else
    echo "YOLOv5 repository already exists."
fi

# 进入 yolov5 目录并安装依赖
cd yolov5 || { echo "Error: yolov5 directory not found!"; exit 1; }
echo "Installing YOLOv5 dependencies..."
pip install -r requirements.txt || { echo "Error: Installing YOLOv5 dependencies failed!"; exit 1; }

# 返回上一级目录并进入 data_handler 目录
cd ../data_handler || { echo "Error: data_handler directory not found!"; exit 1; }

# 定义脚本的路径
GENERATE_FRAME_SCRIPT="generate_frame.py"
GENERATE_LABELS_SCRIPT="generate_labels.py"
TRAIN_VAL_TEST_SCRIPT="train_val_test.py"

# 检查脚本是否存在
if [ ! -f "$GENERATE_FRAME_SCRIPT" ]; then
    echo "Error: $GENERATE_FRAME_SCRIPT not found!"
    exit 1
fi

if [ ! -f "$GENERATE_LABELS_SCRIPT" ]; then
    echo "Error: $GENERATE_LABELS_SCRIPT not found!"
    exit 1
fi

if [ ! -f "$TRAIN_VAL_TEST_SCRIPT" ]; then
    echo "Error: $TRAIN_VAL_TEST_SCRIPT not found!"
    exit 1
fi

# 依次执行脚本
echo "Running $GENERATE_FRAME_SCRIPT..."
python "$GENERATE_FRAME_SCRIPT"
if [ $? -ne 0 ]; then
    echo "Error: $GENERATE_FRAME_SCRIPT failed!"
    exit 1
fi

echo "Running $GENERATE_LABELS_SCRIPT..."
python "$GENERATE_LABELS_SCRIPT"
if [ $? -ne 0 ]; then
    echo "Error: $GENERATE_LABELS_SCRIPT failed!"
    exit 1
fi

echo "Running $TRAIN_VAL_TEST_SCRIPT..."
python "$TRAIN_VAL_TEST_SCRIPT"
if [ $? -ne 0 ]; then
    echo "Error: $TRAIN_VAL_TEST_SCRIPT failed!"
    exit 1
fi

# 返回上一级目录并进入 yolov5 目录
cd ../yolov5 || { echo "Error: yolov5 directory not found!"; exit 1; }

# 执行 YOLOv5 训练
echo "Running YOLOv5 training..."
python train.py --img 640 --batch 12 --epochs 50 --data ../dataset.yaml --weights yolov5x.pt
if [ $? -ne 0 ]; then
    echo "Error: YOLOv5 training failed!"
    exit 1
fi

echo "All scripts executed successfully and YOLOv5 training completed."
