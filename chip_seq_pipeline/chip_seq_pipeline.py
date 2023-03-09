import os
from typing import Optional, List
from .mapping import Mapping
from .trimming import Trimming
from .template import Processor
from .bam2bigwig import Bam2BigWig
from .chipseeker import ChIPseeker
from .peak_calling import PeakCalling
from .motif_finding import MotifFinding
from .peak_annotation import PeakAnnotation
from .mark_duplicates import MarkDuplicates


class ChipSeqPipeline(Processor):

    ref_fa: str
    treatment_fq1: str
    treatment_fq2: str
    control_fq1: Optional[str]
    control_fq2: Optional[str]

    base_quality_cutoff: int
    min_read_length: int

    read_aligner: str
    bowtie2_mode: str
    discard_bam: bool

    skip_mark_duplicates: bool

    macs_effective_genome_size: str
    macs_fdr: float

    genome_version: str
    motif_finding_fragment_size: int

    treatment_bam: str
    control_bam: Optional[str]
    peak_files: List[str]

    def main(
            self,
            ref_fa: str,
            treatment_fq1: str,
            treatment_fq2: str,
            control_fq1: Optional[str],
            control_fq2: Optional[str],

            base_quality_cutoff: int,
            min_read_length: int,

            read_aligner: str,
            bowtie2_mode: str,
            discard_bam: bool,

            skip_mark_duplicates: bool,

            macs_effective_genome_size: str,
            macs_fdr: float,

            genome_version: str,
            motif_finding_fragment_size: int):

        self.ref_fa = ref_fa
        self.treatment_fq1 = treatment_fq1
        self.treatment_fq2 = treatment_fq2
        self.control_fq1 = control_fq1
        self.control_fq2 = control_fq2

        self.base_quality_cutoff = base_quality_cutoff
        self.min_read_length = min_read_length

        self.read_aligner = read_aligner
        self.bowtie2_mode = bowtie2_mode
        self.discard_bam = discard_bam

        self.skip_mark_duplicates = skip_mark_duplicates

        self.macs_effective_genome_size = macs_effective_genome_size
        self.macs_fdr = macs_fdr

        self.genome_version = genome_version
        self.motif_finding_fragment_size = motif_finding_fragment_size

        self.trimming()
        self.mapping()
        self.mark_duplicates()
        self.bam2bigwig()
        self.peak_calling()
        self.peak_annotation()
        self.motif_finding()
        self.chipseeker()
        self.clean_up()

    def trimming(self):
        self.treatment_fq1, self.treatment_fq2, self.control_fq1, self.control_fq2 = Trimming(self.settings).main(
            treatment_fq1=self.treatment_fq1,
            treatment_fq2=self.treatment_fq2,
            control_fq1=self.control_fq1,
            control_fq2=self.control_fq2,
            base_quality_cutoff=self.base_quality_cutoff,
            min_read_length=self.min_read_length)

    def mapping(self):
        self.treatment_bam, self.control_bam = Mapping(self.settings).main(
            ref_fa=self.ref_fa,
            treatment_fq1=self.treatment_fq1,
            treatment_fq2=self.treatment_fq2,
            control_fq1=self.control_fq1,
            control_fq2=self.control_fq2,
            read_aligner=self.read_aligner,
            bowtie2_mode=self.bowtie2_mode)

    def mark_duplicates(self):
        if not self.skip_mark_duplicates:
            self.treatment_bam, self.control_bam = MarkDuplicates(self.settings).main(
                treatment_bam=self.treatment_bam,
                control_bam=self.control_bam)

    def bam2bigwig(self):
        Bam2BigWig(self.settings).main(
            treatment_bam=self.treatment_bam,
            control_bam=self.control_bam)

    def peak_calling(self):
        self.peak_files = PeakCalling(self.settings).main(
            treatment_bam=self.treatment_bam,
            control_bam=self.control_bam,
            macs_effective_genome_size=self.macs_effective_genome_size,
            macs_fdr=self.macs_fdr)

    def peak_annotation(self):
        PeakAnnotation(self.settings).main(
            peak_files=self.peak_files,
            genome_version=self.genome_version)

    def motif_finding(self):
        MotifFinding(self.settings).main(
            peak_files=self.peak_files,
            genome_version=self.genome_version,
            fragment_size=self.motif_finding_fragment_size)

    def chipseeker(self):
        ChIPseeker(self.settings).main(
            peak_files=self.peak_files)

    def clean_up(self):
        CleanUp(self.settings).main(
            bams=[self.treatment_bam, self.control_bam],
            discard_bam=self.discard_bam)


class CleanUp(Processor):

    bams: List[Optional[str]]
    discard_bam: bool

    def main(self, bams: List[Optional[str]], discard_bam: bool):
        self.bams = bams
        self.discard_bam = discard_bam
        self.move_if_keep_bams()
        self.collect_log_files()
        self.remove_workdir()

    def move_if_keep_bams(self):
        keep_bams = not self.discard_bam
        if keep_bams:
            for bam in self.bams:
                if bam is not None:
                    dst = f'{self.outdir}/{os.path.basename(bam)}'
                    self.call(f'mv {bam} {dst}')

    def collect_log_files(self):
        os.makedirs(f'{self.outdir}/log', exist_ok=True)
        cmd = f'mv {self.outdir}/*.log {self.outdir}/log/'
        self.call(cmd)

    def remove_workdir(self):
        if not self.debug:
            self.call(f'rm -r {self.workdir}')
