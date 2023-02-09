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
        index = Bowtie2Indexer(self.settings).main(ref_fa=self.ref_fa)

        self.treatment_bam = Bowtie2Mapper(self.settings).main(
            index=index,
            fq1=self.treatment_fq1,
            fq2=self.treatment_fq2,
            mode=self.bowtie2_mode,
            discard_bam=self.discard_bam,
            sample_name=self.TREATMENT)

        if self.control_fq1 is None:
            self.control_bam = None
        else:
            self.control_bam = Bowtie2Mapper(self.settings).main(
                index=index,
                fq1=self.control_fq1,
                fq2=self.control_fq2,
                mode=self.bowtie2_mode,
                discard_bam=self.discard_bam,
                sample_name=self.CONTROL)

    def run_bwa(self):
        index = BWAIndexer(self.settings).main(ref_fa=self.ref_fa)

        self.treatment_bam = BWAMapper(self.settings).main(
            index=index,
            fq1=self.treatment_fq1,
            fq2=self.treatment_fq2,
            discard_bam=self.discard_bam,
            sample_name=self.TREATMENT)

        if self.control_fq1 is None:
            self.control_bam = None
        else:
            self.control_bam = BWAMapper(self.settings).main(
                index=index,
                fq1=self.control_fq1,
                fq2=self.control_fq2,
                discard_bam=self.discard_bam,
                sample_name=self.CONTROL)


class Bowtie2Indexer(Processor):

    ref_fa: str
    index: str

    def main(self, ref_fa: str) -> str:

        self.ref_fa = ref_fa

        self.index = f'{self.workdir}/bowtie2-index'
        log = f'{self.outdir}/bowtie2-build.log'
        self.call(f'bowtie2-build {self.ref_fa} {self.index} 1> {log} 2> {log}')

        return self.index


class BWAIndexer(Processor):

    ref_fa: str
    index: str

    def main(self, ref_fa: str) -> str:
        self.ref_fa = ref_fa

        self.index = f'{self.workdir}/bwa-index'
        log = f'{self.outdir}/bwa-index.log'
        cmd = self.CMD_LINEBREAK.join([
            'bwa index',
            f'-p {self.index}',
            self.ref_fa,
            f'2> {log}',
        ])
        self.call(cmd)

        return self.index


class TemplateMapper(Processor):

    index: str
    fq1: str
    fq2: str
    discard_bam: bool
    sample_name: str

    index: str
    sam: str
    bam: str
    sorted_bam: str
    mapping_stats_txt: str

    def run_workflow(self):
        self.set_filenames()
        self.mapping()
        self.sam_to_bam()
        self.sort_bam()
        self.mapping_stats()
        self.move_if_keep_bam()

    def set_filenames(self):
        self.sam = f'{self.workdir}/mapped-{self.sample_name}.sam'
        self.bam = f'{self.workdir}/mapped-{self.sample_name}.bam'
        self.sorted_bam = f'{self.workdir}/sorted-{self.sample_name}.bam'
        self.mapping_stats_txt = f'{self.outdir}/mapping-stats-{self.sample_name}.txt'

    def mapping(self):
        pass

    def sam_to_bam(self):
        self.call(f'samtools view -b -h {self.sam} > {self.bam}')

    def sort_bam(self):
        self.call(f'samtools sort {self.bam} > {self.sorted_bam}')

    def mapping_stats(self):
        self.call(f'samtools stats {self.sorted_bam} > {self.mapping_stats_txt}')

    def move_if_keep_bam(self):
        keep_bam = not self.discard_bam
        if keep_bam:
            dst = f'{self.outdir}/{basename(self.sorted_bam)}'
            self.call(f'mv {self.sorted_bam} {dst}')
            self.sorted_bam = dst


class Bowtie2Mapper(TemplateMapper):

    mode: str

    def main(
            self,
            index: str,
            fq1: str,
            fq2: str,
            mode: str,
            discard_bam: bool,
            sample_name: str) -> str:

        self.index = index
        self.fq1 = fq1
        self.fq2 = fq2
        self.mode = mode
        self.discard_bam = discard_bam
        self.sample_name = sample_name

        self.run_workflow()

        return self.sorted_bam

    def mapping(self):
        log = f'{self.outdir}/bowtie2-{self.sample_name}.log'
        cmd = f'''bowtie2 \\
-x {self.index} \\
-1 {self.fq1} \\
-2 {self.fq2} \\
-S {self.sam} \\
--{self.mode} \\
--no-unal \\
--threads {self.threads} \\
1> {log} \\
2> {log}'''
        self.call(cmd)


class BWAMapper(TemplateMapper):

    def main(
            self,
            index: str,
            fq1: str,
            fq2: str,
            discard_bam: bool,
            sample_name: str) -> str:

        self.index = index
        self.fq1 = fq1
        self.fq2 = fq2
        self.discard_bam = discard_bam
        self.sample_name = sample_name

        self.run_workflow()

        return self.sorted_bam

    def mapping(self):
        log = f'{self.outdir}/bwa-mem-{self.sample_name}.log'
        args = [
            'bwa mem',
            f'-t {self.threads}',
            f'-o {self.sam}',
            self.index,
            self.fq1,
            self.fq2,
        ]

        args += [f'2> {log}']

        self.call(self.CMD_LINEBREAK.join(args))
