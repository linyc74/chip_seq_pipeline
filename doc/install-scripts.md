Create conda environment and install packages

```shell
conda create -n chip-seq python=3
conda activate chip-seq

pip install pandas deeptools

conda install -c bioconda macs2 bwa trim-galore samtools bowtie2 gatk4
```

### HOMER

From the [HOMER download page](http://homer.ucsd.edu/homer/download.html),
download [configureHomer.pl](http://homer.ucsd.edu/homer/configureHomer.pl).
Place the file in the directory you would like to install HOMER, e.g. `~/opt/HOMER`

```shell
cd ~/opt/HOMER
perl configureHomer.pl -install
```

Download hg38 (GRCh38) genome for annotation

```shell
perl configureHomer.pl -install hg38
```

In `~/.bashrc` add to `PATH` variable

```shell
export PATH=$PATH:$HOME/opt/HOMER/bin
```

### HOMER Dependencies

Older versions of HOMER (e.g. 4.7) requires outdated 3rd party packages.
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

Update R to version 4.2.2.

```shell
conda activate chip-seq
conda install -c conda-forge r-base=4.2.2  # must be version 4.2.2
```

There could be a few libraries required for ChIPseeker compilation.
Here are some that I encountered, but different machines could vary.

```shell
# Linux
conda install -c conda-forge r-curl
conda install -c conda-forge r-rcppeigen

# Mac
conda install -c conda-forge r-devtools
conda install -c conda-forge r-textshaping
```

Package config (`.pc`) files like `fontconfig.pc`, `freetype2.pc`, `libcurl.pc`
need to be accessible through the `PKG_CONFIG_PATH` environment variable.
These files are required for ChIPseeker compilation.

```shell
export PKG_CONFIG_PATH=$HOME/anaconda3/envs/chip-seq/lib/pkgconfig
```

Enter the R console.

```shell
R
```

In the R console, install `ChIPseeker`.

```R
if (!require("BiocManager", quietly = TRUE))
    install.packages("BiocManager")

# upgrade bioconductor to version 3.16, which depends on R 4.2.2
BiocManager::install(version="3.16")

BiocManager::install("ChIPseeker")
```
