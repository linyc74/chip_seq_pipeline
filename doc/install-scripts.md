Create conda environment and install packages

```shell
conda create -n chip-seq python=3
conda activate chip-seq

pip install pandas

conda install -c bioconda macs2 bwa trim-galore samtools bowtie2 gatk4
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

### ChIPseeker

The R hosted by Anaconda can cause downstream compilation problems for the library `libcurl`.
Avoid using Anaconda's R by removing them from the conda environment.

```shell
conda activate chip-seq
conda remove libcurl r-base
```

Install dynamic libraries (`libcurl` and `libfontconfig`) that may be required for R package compilation.

```shell
sudo apt-get update
sudo apt-get install libcurl4-openssl-dev
sudo apt-get install libfontconfig1-dev
```

Install R in the global environment by following the instructions in [install-r-packages.md](./install-r-packages.md).

Enter the R console.

```shell
sudo R
```

In the R console, install `ChIPseeker`.

```R
install.packages("systemfonts")

if (!require("BiocManager", quietly = TRUE))
    install.packages("BiocManager")

BiocManager::install("ChIPseeker")
```
