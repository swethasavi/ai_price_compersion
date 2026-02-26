#!/bin/bash
# render-build.sh

echo "--> Installing dependencies"
pip install -r requirements.txt

echo "--> Re-training model for environment compatibility"
python train_model.py

echo "--> Build completed successfully!"