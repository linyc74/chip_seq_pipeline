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

### HOMER Dependencies

HOMER is very old (~2005) that it requires outdated 3rd party packages.
Although it says it does not require Ghostscript and seqlogo to run,
actually both are required to generate sequence logo in the HTML output.
Here's the instruction page for 3rd party dependencies: http://homer.ucsd.edu/homer/introduction/install.html

Ghostscript for `findMotifsGenome.pl`.

```shell
cd ~/opt
wget https://github.com/ArtifexSoftware/ghostpdl-downloads/releases/download/gs1000/ghostscript-10.0.0-linux-x86_64.tgz
tar -xzf ghostscript-10.0.0-linux-x86_64.tgz
```

Create an executable `gs`.

```shell
cd ~/opt/ghostscript-10.0.0-linux-x86_64
ln -s gs-1000-linux-x86_64 gs
```

Add `PATH` in the `~/.bashrc` file.

```shell
export PATH=$PATH:$HOME/opt/ghostscript-10.0.0-linux-x86_64
```

Install `seqlogo` for `findMotifsGenome.pl`.
Install [WebLogo](http://weblogo.berkeley.edu/) version 2.8.2 which contains `seqlogo`.
WebLogo 3 does NOT work.

```shell
cd ~/opt
wget http://weblogo.berkeley.edu/release/weblogo.2.8.2.tar.gz
tar -xzf weblogo.2.8.2.tar.gz
```

Add `PATH` in the `~/.bashrc` file.

```shell
export PATH=$PATH:$HOME/opt/weblogo
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
