from typing import Optional
from .mapping import Mapping
from .trimming import Trimming
from .template import Processor
from .peak_calling import PeakCalling


class ChipSeqPipeline(Processor):

    ref_fa: str
    treatment_fq1: str
    treatment_fq2: str
    control_fq1: Optional[str]
    control_fq2: Optional[str]
    gtf: str

    base_quality_cutoff: int
    min_read_length: int
    max_read_length: int

    read_aligner: str
    bowtie2_mode: str
    discard_bam: bool

    peak_caller: str

    treatment_bam: str
    control_bam: Optional[str]

    def main(
            self,
            ref_fa: str,
            treatment_fq1: str,
            treatment_fq2: str,
            control_fq1: str,
            control_fq2: str,
            gtf: str,

            base_quality_cutoff: int,
            min_read_length: int,
            max_read_length: int,

            read_aligner: str,
            bowtie2_mode: str,
            discard_bam: bool,

            peak_caller: str):

        self.ref_fa = ref_fa
        self.treatment_fq1 = treatment_fq1
        self.treatment_fq2 = treatment_fq2
        self.control_fq1 = control_fq1
        self.control_fq2 = control_fq2
        self.gtf = gtf

        self.base_quality_cutoff = base_quality_cutoff
        self.min_read_length = min_read_length
        self.max_read_length = max_read_length

        self.read_aligner = read_aligner
        self.bowtie2_mode = bowtie2_mode
        self.discard_bam = discard_bam

        self.peak_caller = peak_caller

        self.trimming()
        self.mapping()
        self.peak_calling()
        self.peak_annotation()

    def trimming(self):
        self.treatment_fq1, self.treatment_fq2, self.control_fq1, self.control_fq2 = Trimming(self.settings).main(
            treatment_fq1=self.treatment_fq1,
            treatment_fq2=self.treatment_fq2,
            control_fq1=self.control_fq1,
            control_fq2=self.control_fq2,
            base_quality_cutoff=self.base_quality_cutoff,
            min_read_length=self.min_read_length,
            max_read_length=self.max_read_length)

    def mapping(self):
        self.treatment_bam, self.control_bam = Mapping(self.settings).main(
            ref_fa=self.ref_fa,
            treatment_fq1=self.treatment_fq1,
            treatment_fq2=self.treatment_fq2,
            control_fq1=self.control_fq1,
            control_fq2=self.control_fq2,
            read_aligner=self.read_aligner,
            bowtie2_mode=self.bowtie2_mode,
            discard_bam=self.discard_bam)

    def peak_calling(self):
        PeakCalling(self.settings).main(
            treatment_bam=self.treatment_bam,
            control_bam=self.control_bam,
            peak_caller=self.peak_caller)

    def peak_annotation(self):
        pass
