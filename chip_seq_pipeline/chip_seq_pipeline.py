from .template import Processor


class ChipSeqPipeline(Processor):

    ref_fa: str
    fq1: str
    fq2: str
    gtf: str

    base_quality_cutoff: int
    min_read_length: int
    max_read_length: int

    read_aligner: str
    bowtie2_mode: str
    discard_bam: bool

    def main(
            self,
            ref_fa: str,
            fq1: str,
            fq2: str,
            gtf: str,

            base_quality_cutoff: int,
            min_read_length: int,
            max_read_length: int,

            read_aligner: str,
            bowtie2_mode: str,
            discard_bam: bool):

        self.ref_fa = ref_fa
        self.fq1 = fq1
        self.fq2 = fq2
        self.gtf = gtf

        self.base_quality_cutoff = base_quality_cutoff
        self.min_read_length = min_read_length
        self.max_read_length = max_read_length

        self.read_aligner = read_aligner
        self.bowtie2_mode = bowtie2_mode
        self.discard_bam = discard_bam



