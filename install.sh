brew install tesseract
conda create -n data_logger python=3.10.9 anaconda

conda activate data_logger
pip install -r dependencies.txt
conda deactivate