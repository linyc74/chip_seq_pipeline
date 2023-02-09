import os
from os.path import basename
from functools import partial
from typing import Tuple, Optional, Callable
from .template import Processor


class Trimming(Processor):

    treatment_fq1: str
    treatment_fq2: str
    control_fq1: Optional[str]
    control_fq2: Optional[str]

    base_quality_cutoff: int
    min_read_length: int
    max_read_length: int

    trim_galore: Callable

    def main(
            self,
            treatment_fq1: str,
            treatment_fq2: str,
            control_fq1: str,
            control_fq2: str,

            base_quality_cutoff: int,
            min_read_length: int,
            max_read_length: int) -> Tuple[str, str, str, str]:

        self.treatment_fq1 = treatment_fq1
        self.treatment_fq2 = treatment_fq2
        self.control_fq1 = control_fq1
        self.control_fq2 = control_fq2

        self.base_quality_cutoff = base_quality_cutoff
        self.min_read_length = min_read_length
        self.max_read_length = max_read_length

        self.set_trim_galore_function()
        self.trim_treatment_fqs()
        self.trim_control_fqs()

        return self.treatment_fq1, self.treatment_fq2, self.control_fq1, self.control_fq2

    def set_trim_galore_function(self):
        self.trim_galore = partial(
            TrimGalore(self.settings).main,
            base_quality_cutoff=self.base_quality_cutoff,
            min_read_length=self.min_read_length,
            max_read_length=self.max_read_length)

    def trim_treatment_fqs(self):
        self.treatment_fq1, self.treatment_fq2 = self.trim_galore(
            fq1=self.treatment_fq1,
            fq2=self.treatment_fq2)

    def trim_control_fqs(self):
        if self.control_fq1 is not None:
            self.control_fq1, self.control_fq2 = self.trim_galore(
                fq1=self.control_fq1,
                fq2=self.control_fq2)


class TrimGalore(Processor):

    MAX_N = 0
    CUTADAPT_TOTAL_CORES = 2
    # According to the help message of trim_galore, 2 cores for cutadapt -> actually up to 9 cores

    fq1: str
    fq2: str
    base_quality_cutoff: int
    min_read_length: int
    max_read_length: int

    out_fq1: str
    out_fq2: str

    def main(
            self,
            fq1: str,
            fq2: str,
            base_quality_cutoff: int,
            min_read_length: int,
            max_read_length: int) -> Tuple[str, str]:

        self.fq1 = fq1
        self.fq2 = fq2
        self.base_quality_cutoff = base_quality_cutoff
        self.min_read_length = min_read_length
        self.max_read_length = max_read_length

        self.execute()
        self.set_out_fq1_fq2()
        self.move_fastqc_report()

        return self.out_fq1, self.out_fq2

    def execute(self):
        args = [
            'trim_galore',
            '--paired',
            f'--quality {self.base_quality_cutoff}',
            '--phred33',
            f'--cores {self.CUTADAPT_TOTAL_CORES}',
            f'--fastqc_args "--threads {self.threads}"',
            '--illumina',
            f'--length {self.min_read_length}',
            f'--max_n {self.MAX_N}',
            '--trim-n',
            '--gzip',
            f'--output_dir {self.workdir}'
        ]

        log = f'{self.outdir}/trim_galore.log'
        args += [
            self.fq1,
            self.fq2,
            f'1>> {log} 2>> {log}'
        ]

        self.call(self.CMD_LINEBREAK.join(args))

    def set_out_fq1_fq2(self):
        self.out_fq1 = f'{self.workdir}/{get_fq_filename(self.fq1)}_val_1.fq.gz'
        self.out_fq2 = f'{self.workdir}/{get_fq_filename(self.fq2)}_val_2.fq.gz'

    def move_fastqc_report(self):
        dstdir = f'{self.outdir}/fastqc'
        os.makedirs(dstdir, exist_ok=True)
        for suffix in [
            'fastqc.html',
            'fastqc.zip',
            'trimming_report.txt'
        ]:
            self.call(f'mv {self.workdir}/*{suffix} {dstdir}/')


def get_fq_filename(f: str) -> str:
    f = basename(f)
    for suffix in [
        '.fq',
        '.fq.gz',
        '.fastq',
        '.fastq.gz',
    ]:
        if f.endswith(suffix):
            f = f[:-len(suffix)]  # strip suffix
    return f
