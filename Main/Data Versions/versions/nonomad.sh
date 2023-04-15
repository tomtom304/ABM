#!/bin/bash
# Name:   My First Job
 
# These are SBATCH commands (SBATCH doesnt take Shell Variables)
#SBATCH --job-name="nonomad"                  # Job Name
#SABTCH --get-user-env                           # User Environment
#SBATCH --error="job-%j.err"                     # Redirect STDERR (Error output) to this file %j is a variable for JobID
#SBATCH --output="job-%j.out"                    # Redirect STDOUT (Normal output) to this file %j is a variable for JobID
#SBATCH --mem=2G    
#SBATCH --ntasks=1                              # Requested memory for the Job (Default is 2G)
#SBATCH --export=ALL                             # Export Current Environment Variables (Default ALL)
#SBATCH -D /mt/batch/tparker                     # Put all output on batch storage (--chdir is bugged)
 
# The rest is similar to a standard shell script
WORKDIR=/mt/batch/tparker/nonomad/$SLURM_ARRAY_TASK_ID
mkdir -p "$WORKDIR" && cd "$WORKDIR" || exit -1 
srun python /mt/home/tparker/nonomad.py
 
# Remember to exit cleanly
exit 0;