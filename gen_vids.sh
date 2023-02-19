#!/bin/bash

#SBATCH --gres=gpu:1
#SBATCH --partition=seas_gpu
#SBATCH -t 0-20:00

#SBATCH --mem-per-gpu=40GB

#SBATCH -o vid_gen.sh.log-%j

module load Anaconda3/2020.11
module load ffmpeg/4.0.2-fasrc01

echo "commencing video generation""
python timestamp_vid_gen.py

echo "video generation over"



