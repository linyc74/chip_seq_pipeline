from os.path import basename
from typing import Optional
from .template import Processor


class Mapping(Processor):

    ref_fa: str
    fq1: str
    fq2: Optional[str]
    read_aligner: str
    bowtie2_mode: str
    discard_bam: bool

    sorted_bam: str

    def main(
            self,
            ref_fa: str,
            fq1: str,
            fq2: Optional[str],
            read_aligner: str,
            bowtie2_mode: str,
            discard_bam: bool) -> str:

        self.ref_fa = ref_fa
        self.fq1 = fq1
        self.fq2 = fq2
        self.read_aligner = read_aligner.lower()
        self.bowtie2_mode = bowtie2_mode.lower()
        self.discard_bam = discard_bam

        assert self.read_aligner in ['bowtie2', 'bwa']

        if self.read_aligner == 'bowtie2':
            self.run_bowtie2()
        else:
            self.run_bwa()

        self.mapping_stats()
        self.move_if_keep_bam()

        return self.sorted_bam

    def run_bowtie2(self):
        self.sorted_bam = Bowtie2(self.settings).main(
            ref_fa=self.ref_fa,
            fq1=self.fq1,
            fq2=self.fq2,
            mode=self.bowtie2_mode)

    def run_bwa(self):
        self.sorted_bam = BWA(self.settings).main(
            ref_fa=self.ref_fa,
            fq1=self.fq1,
            fq2=self.fq2)

    def mapping_stats(self):
        txt = f'{self.outdir}/mapping-stats.txt'
        self.call(f'samtools stats {self.sorted_bam} > {txt}')

    def move_if_keep_bam(self):
        keep_bam = not self.discard_bam
        if keep_bam:
            dst = f'{self.outdir}/{basename(self.sorted_bam)}'
            self.call(f'mv {self.sorted_bam} {dst}')
            self.sorted_bam = dst


class BaseMapper(Processor):

    ref_fa: str
    fq1: str
    fq2: Optional[str]
    discard_bam: bool

    idx: str
    sam: str
    bam: str
    sorted_bam: str

    def sam_to_bam(self):
        self.bam = f'{self.workdir}/mapped.bam'
        self.call(f'samtools view -b -h {self.sam} > {self.bam}')

    def sort_bam(self):
        self.sorted_bam = f'{self.workdir}/sorted.bam'
        self.call(f'samtools sort {self.bam} > {self.sorted_bam}')


class Bowtie2(BaseMapper):

    mode: str

    def main(
            self,
            ref_fa: str,
            fq1: str,
            fq2: Optional[str],
            mode: str) -> str:

        self.ref_fa = ref_fa
        self.fq1 = fq1
        self.fq2 = fq2
        self.mode = mode

        self.indexing()
        if self.fq2 is None:
            self.single_end_mapping()
        else:
            self.paired_end_mapping()
        self.sam_to_bam()
        self.sort_bam()

        return self.sorted_bam

    def indexing(self):
        self.idx = f'{self.workdir}/bowtie2-index'
        log = f'{self.outdir}/bowtie2-build.log'
        self.call(f'bowtie2-build {self.ref_fa} {self.idx} 1> {log} 2> {log}')

    def single_end_mapping(self):
        log = f'{self.outdir}/bowtie2.log'
        self.sam = f'{self.workdir}/mapped.sam'
        cmd = f'''bowtie2 \\
-x {self.idx} \\
-U {self.fq1} \\
-S {self.sam} \\
--{self.mode} \\
--no-unal \\
--threads {self.threads} \\
1> {log} \\
2> {log}'''
        self.call(cmd)

    def paired_end_mapping(self):
        log = f'{self.outdir}/bowtie2.log'
        self.sam = f'{self.workdir}/mapped.sam'
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


class BWA(BaseMapper):

    def main(
            self,
            ref_fa: str,
            fq1: str,
            fq2: Optional[str]) -> str:

        self.ref_fa = ref_fa
        self.fq1 = fq1
        self.fq2 = fq2

        self.indexing()
        self.mapping()
        self.sam_to_bam()
        self.sort_bam()

        return self.sorted_bam

    def indexing(self):
        self.idx = f'{self.workdir}/bwa-index'
        log = f'{self.outdir}/bwa-index.log'
        cmd = self.CMD_LINEBREAK.join([
            'bwa index',
            f'-p {self.idx}',
            self.ref_fa,
            f'2> {log}',
        ])
        self.call(cmd)

    def mapping(self):
        self.sam = f'{self.workdir}/mapped.sam'
        log = f'{self.outdir}/bwa-mem.log'
        args = [
            'bwa mem',
            f'-t {self.threads}',
            f'-o {self.sam}',
            self.idx,
            self.fq1
        ]

        if self.fq2 is not None:
            args += [self.fq2]

        args += [f'2> {log}']

        self.call(self.CMD_LINEBREAK.join(args))
