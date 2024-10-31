conda create -n a001 -f my_env.yml -y
conda init
echo "conda activate a001" >> ~/.bashrc

python main.py
