#!/bin/bash
#SBATCH --job-name=rayx_job
#SBATCH --output=jobs/%j.out
#SBATCH --error=jobs/%j.err
#SBATCH --time=01:00:00
#SBATCH --cpus-per-task=4
#SBATCH --mem=8GB
#SBATCH --partition=std

# activate environment if needed
module load python

# activate virtual environment
source .venv/bin/activate 

# run rayx and give rml file to $1 and output to $2
echo "Running RAYX"

python run_rayx.py $1 $2

echo "RAYX finished"

deactivate