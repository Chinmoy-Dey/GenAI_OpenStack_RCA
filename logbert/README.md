pip install -r  requirements.txt 
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu


python utils/preprocess.py
python train.py
python evaluate.py
python test.py


