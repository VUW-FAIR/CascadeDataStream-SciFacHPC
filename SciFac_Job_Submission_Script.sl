#!/bin/sh

### To submit a job to the queing system, use: qsub SciFac_Job_Submission_Script.sl

#$ -S /bin/bash
#$ -N DataStream  # Job Name as it appears in the que.
#$ -wd /srv/global/scratch/hashmimu
#$ -l s_rt=240:00:00         # Walltime
#$ -l h_slots=1              # Number of Nodes
#$ -l virtual_free=2.5G      # Memory Requirement per processor
#$ -pe smp 24                # Number of Processors
#$ -M Muhammad.Hashmi@vuw.ac.nz # Email to send job completion email

# A check to see of the GridEngine is working correctly
if [ -d /srv/local/work/$JOB_ID ]; then
        cd /srv/local/work/$JOB_ID
else
        echo "There's no job directory to change into "
        echo "Here's LOCAL WORK "
        ls -la /srv/local/work
        echo "Exiting"
        exit 1
fi


# Save the current files path and names. There is a need to specify the path of the script and
# the input_file. I am not that expert of bash scripting to include these as first arguments.
python_script="/home/scifachpc-fs01/hashmimu/big-data-analysis/CascadeDataStream_SciFac.py"
input_file="/home/scifachpc-fs01/hashmimu/big-data-analysis/input_files/sorted.csv"
python_script_basename=$(basename ${python_script} .${python_script_ext})
input_file_basename=$(basename ${input_file} .${input_file_ext})


# Make sure the input file exists and is readable
if [ ! -f "${input_file}" ]
then
	echo "${input_file}: no such file" >&2
	exit 1
elif [ ! -r "${input_file}" ]
then
	echo "${input_file}: permission denied" >&2
	exit 1
fi

# Make sure the Python Script file exists and is readable
if [ ! -f "${python_script}" ]
then
	echo "${python_script}: no such file" >&2
	exit 1
elif [ ! -r "${python_script}" ]
then
	echo "${python_script}: permission denied" >&2
	exit 1
fi

# Create a job-specific directory back on the globally visible scratch area
#mkdir -p /srv/global/scratch/hashmimu/$JOB_ID


# Load the user environment. You can also use python 2.7 by replacing "34" by "27"
module load scl-python/34


# Now we are in the job-specific directory. Copy input files here
cp ${python_script} .
cp ${input_file} .

# Run the job now
python3 ${python_script} ${input_file_basename}

# Copy the results back to the original directory
mkdir -p /home/scifachpc-fs01/hashmimu/big-data-analysis/output_files/$JOB_ID  || exit 1
rm -f ${input_file_basename}  # Remove the original input file so that it don't get copied again.
cp -r *.csv /home/scifachpc-fs01/hashmimu/big-data-analysis/output_files/$JOB_ID/  || exit 1
