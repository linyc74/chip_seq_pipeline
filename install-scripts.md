Create conda environment and install packages

```shell
conda create -n chip-seq python=3
conda activate chip-seq

pip install pandas

conda install -c bioconda \
  macs2=2.2.7.1 \
  bwa=0.7.17 \
  trim-galore=0.6.2 \
  samtools=1.16 \
  bowtie2=2.5.1
```

### HOMER

From the [HOMER download page](http://homer.salk.edu/homer/download.html),
download [configureHomer.pl](http://homer.salk.edu/homer/configureHomer.pl).
Place the file in the directory you would like to install HOMER, e.g. `~/opt/HOMER-4.7`

```shell
cd ~/opt/HOMER-4.7
perl configureHomer.pl -install
```

Download hg38 (GRCh38) genome for annotation

```shell
perl configureHomer.pl -install hg38
```

In `~/.bashrc` add to `PATH` variable
```shell
export PATH=$PATH:$HOME/opt/HOMER-4.7/bin
```
