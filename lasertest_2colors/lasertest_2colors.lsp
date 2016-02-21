#PBS -l walltime=48:00:00
#PBS -l nodes=1:ppn=48
#PBS -N lasertest2d
#PBS -S /bin/bash
#PBS -j oe
#PBS -m ae
#PBS -M ngirmang.1@osu.edu

#module load intel-compilers-11.1
#module load openmpi-1.4.3-intel    #this is needed for mpirun to work
module load openmpi-1.4.3-gnu

#This outputs the name of the root node to the directory where you submitted this PBS job
echo $HOSTNAME > $PBS_O_WORKDIR/hostname.txt   
cat $PBS_NODEFILE | uniq > $PBS_O_WORKDIR/cat_nodefile.txt

#mkdir /tmp/${USER}_${PBS_JOBID}

#DOTLSPFILE=hotwater.lsp
cd $PBS_O_WORKDIR

#cd /tmp/${USER}_${PBS_JOBID}

#cp $PBS_O_WORKDIR/lsp .
#cp $PBS_O_WORKDIR/sine*.dat .
#cp $PBS_O_WORKDIR/${DOTLSPFILE} .

#mpirun -np 48 -hostfile $PBS_NODEFILE ./lsp12_ramsusii_newlaser_2d lasertest2d.lsp >log.txt
#mpirun -np 48 -hostfile $PBS_NODEFILE ./lsp12_ramsusii_oldlaser_2d lasertest2d.lsp >log.txt
mpirun -np 48 -hostfile $PBS_NODEFILE ./lsp10_ramsusii_2d lasertest2d.lsp >log.txt
#mpirun -np 48 ./lsp2d_glenn hotwater.lsp > log.txt



