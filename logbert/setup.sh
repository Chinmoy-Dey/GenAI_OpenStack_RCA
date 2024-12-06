echo "Removing existing repos ..."
rm -rf logbert loghub logparser

echo "Cloning new repos ..."
git clone https://github.com/HelenGuohx/logbert.git
git clone https://github.com/logpai/loghub.git
git clone https://github.com/logpai/logparser.git
git clone https://github.com/nailo2c/deeplog.git

echo "Installing dependencies ..."
pip install -r requirements.txt

echo "copy logs to data .."
rm -f data/*
find loghub/ -name OpenStack_2k.log* | xargs -0 -d "\n" cp -t  data/

cd deeplog/example
python preprocess.py --input_path ../../data/OpenStack_2k.log --output_path ../../data/preprocessed_logs.txt
cd -

echo "Split the dataset into train and test sets .."
python utils/preprocess.py

echo "Train the model ...it will take a while ..."
python train.py

echo "Evaluate the model .."
python evaluate.py

echo "Test the model now .."

echo "Removing existing repos ..."
rm -rf logbert loghub logparser
