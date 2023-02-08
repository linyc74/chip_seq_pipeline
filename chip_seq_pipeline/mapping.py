from os.path import basename
from typing import Optional, Tuple
from .template import Processor


class Mapping(Processor):

    TREATMENT = 'treatment'
    CONTROL = 'control'

    ref_fa: str
    treatment_fq1: str
    treatment_fq2: str
    control_fq1: Optional[str]
    control_fq2: Optional[str]
    read_aligner: str
    bowtie2_mode: str
    discard_bam: bool

    treatment_bam: str
    control_bam: Optional[str]

    def main(
            self,
            ref_fa: str,
            treatment_fq1: str,
            treatment_fq2: str,
            control_fq1: Optional[str],
            control_fq2: Optional[str],
            read_aligner: str,
            bowtie2_mode: str,
            discard_bam: bool) -> Tuple[str, Optional[str]]:

        self.ref_fa = ref_fa
        self.treatment_fq1 = treatment_fq1
        self.treatment_fq2 = treatment_fq2
        self.control_fq1 = control_fq1
        self.control_fq2 = control_fq2
        self.read_aligner = read_aligner.lower()
        self.bowtie2_mode = bowtie2_mode.lower()
        self.discard_bam = discard_bam

        assert self.read_aligner in ['bowtie2', 'bwa']

        if self.read_aligner == 'bowtie2':
            self.run_bowtie2()
        else:
            self.run_bwa()

        return self.treatment_bam, self.control_bam

    def run_bowtie2(self):
        self.treatment_bam = Bowtie2(self.settings).main(
            ref_fa=self.ref_fa,
            fq1=self.treatment_fq1,
            fq2=self.treatment_fq2,
            mode=self.bowtie2_mode,
            discard_bam=self.discard_bam,
            sample_name=self.TREATMENT)

        if self.control_fq1 is None:
            self.control_bam = None
        else:
            self.control_bam = Bowtie2(self.settings).main(
                ref_fa=self.ref_fa,
                fq1=self.control_fq1,
                fq2=self.control_fq2,
                mode=self.bowtie2_mode,
                discard_bam=self.discard_bam,
                sample_name=self.CONTROL)

    def run_bwa(self):
        self.treatment_bam = BWA(self.settings).main(
            ref_fa=self.ref_fa,
            fq1=self.treatment_fq1,
            fq2=self.treatment_fq2,
            discard_bam=self.discard_bam,
            sample_name=self.TREATMENT)

        if self.control_fq1 is None:
            self.control_bam = None
        else:
            self.control_bam = BWA(self.settings).main(
                ref_fa=self.ref_fa,
                fq1=self.control_fq1,
                fq2=self.control_fq2,
                discard_bam=self.discard_bam,
                sample_name=self.CONTROL)


class Base(Processor):

    ref_fa: str
    fq1: str
    fq2: str
    discard_bam: bool
    sample_name: str

    idx: str
    sam: str
    bam: str
    sorted_bam: str

    def run_workflow(self):
        self.indexing()
        self.mapping()
        self.sam_to_bam()
        self.sort_bam()
        self.mapping_stats()
        self.move_if_keep_bam()

    def indexing(self):
        pass

    def mapping(self):
        pass

    def sam_to_bam(self):
        self.bam = f'{self.workdir}/{self.sample_name}-mapped.bam'
        self.call(f'samtools view -b -h {self.sam} > {self.bam}')

    def sort_bam(self):
        self.sorted_bam = f'{self.workdir}/{self.sample_name}-sorted.bam'
        self.call(f'samtools sort {self.bam} > {self.sorted_bam}')

    def mapping_stats(self):
        txt = f'{self.outdir}/{self.sample_name}-mapping-stats.txt'
        self.call(f'samtools stats {self.sorted_bam} > {txt}')

    def move_if_keep_bam(self):
        keep_bam = not self.discard_bam
        if keep_bam:
            dst = f'{self.outdir}/{basename(self.sorted_bam)}'
            self.call(f'mv {self.sorted_bam} {dst}')
            self.sorted_bam = dst


class Bowtie2(Base):

    mode: str

    def main(
            self,
            ref_fa: str,
            fq1: str,
            fq2: str,
            mode: str,
            discard_bam: bool,
            sample_name: str) -> str:

        self.ref_fa = ref_fa
        self.fq1 = fq1
        self.fq2 = fq2
        self.mode = mode
        self.discard_bam = discard_bam
        self.sample_name = sample_name

        self.run_workflow()

        return self.sorted_bam

    def indexing(self):
        self.idx = f'{self.workdir}/{self.sample_name}-bowtie2-index'
        log = f'{self.outdir}/{self.sample_name}-bowtie2-build.log'
        self.call(f'bowtie2-build {self.ref_fa} {self.idx} 1> {log} 2> {log}')

    def mapping(self):
        log = f'{self.outdir}/{self.sample_name}-bowtie2.log'
        self.sam = f'{self.workdir}/{self.sample_name}-mapped.sam'
        cmd = f'''bowtie2 \\
-x {self.idx} \\
-1 {self.fq1} \\
-2 {self.fq2} \\
-S {self.sam} \\
--{self.mode} \\
--no-unal \\
--threads {self.threads} \\
1> {log} \\
2> {log}'''
        self.call(cmd)


class BWA(Base):

    def main(
            self,
            ref_fa: str,
            fq1: str,
            fq2: str,
            discard_bam: bool,
            sample_name: str) -> str:

        self.ref_fa = ref_fa
        self.fq1 = fq1
        self.fq2 = fq2
        self.discard_bam = discard_bam
        self.sample_name = sample_name

        self.run_workflow()

        return self.sorted_bam

    def indexing(self):
        self.idx = f'{self.workdir}/{self.sample_name}-bwa-index'
        log = f'{self.outdir}/{self.sample_name}-bwa-index.log'
        cmd = self.CMD_LINEBREAK.join([
            'bwa index',
            f'-p {self.idx}',
            self.ref_fa,
            f'2> {log}',
        ])
        self.call(cmd)

    def mapping(self):
        self.sam = f'{self.workdir}/{self.sample_name}-mapped.sam'
        log = f'{self.outdir}/{self.sample_name}-bwa-mem.log'
        args = [
            'bwa mem',
            f'-t {self.threads}',
            f'-o {self.sam}',
            self.idx,
            self.fq1,
            self.fq2,
        ]

        args += [f'2> {log}']

        self.call(self.CMD_LINEBREAK.join(args))
