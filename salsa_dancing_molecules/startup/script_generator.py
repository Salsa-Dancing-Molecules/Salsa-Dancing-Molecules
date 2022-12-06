"""Module for creating Sbatch script."""
import os


def create_sbatch(job, use_devel, time, nodes, cores, work_path):
    """Create an sbatch script and save it to a file to be executed.

    Args:
        job: string - the name of the job.
        use_devel: bool - if true, type of job is 'devel'.
        time: string - max time for job.
        nodes: string - number of nodes to be used.
        cores: string - number of cores to be used.
        work_path: string - path to workspace directory.
    """
    reservation = ""
    if use_devel:
        reservation = "#SBATCH --reservation devel\n"
    script = ("#!/bin/bash\n" +
              "#\n" +
              "#SBATCH -J " + job + "\n" +
              "#SBATCH -A LiU-compute-2022-29\n" +
              reservation +
              "#SBATCH -t " + time + "\n" +
              "#SBATCH -N " + nodes + "\n" +
              "#SBATCH -n " + cores + "\n" +
              "#SBATCH --exclusive\n"
              "#\n" +
              "export NSC_MODULE_SILENT=1\n" +
              "export OPENBLAS_NUM_THREADS=1\n" +
              "export MKL_NUM_THREADS=1\n" +
              "export NUMEXPR_NUM_THREADS=1\n" +
              "export OMP_NUM_THREADS=1\n\n" +
              "source activate salsa_dancing_molecules\n" +
              "salsa-dancing-molecules -h\n" +
              "# salsa-dancing-molecules worker " + work_path +
              "\n")
    base_name = "./run_workers"
    if os.path.exists(base_name+".q"):
        i = 1
        while (i < 99999):
            if not os.path.exists(base_name+"_"+str(i)+".q"):
                with open(base_name + "_" + str(i) + ".q", "w") as f:
                    f.write(script)
                    break
            i += 1
        if i >= 100000:
            print("Too many sbatch scripts in directory.")
    else:
        with open(base_name + ".q", "w") as f:
            f.write(script)
