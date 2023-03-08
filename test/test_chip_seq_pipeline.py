from chip_seq_pipeline import ChipSeqPipeline
from .setup import TestCase


class TestChipSeqPipeline(TestCase):

    def setUp(self):
        self.set_up(py_path=__file__)

    def tearDown(self):
        self.tear_down()

    def test_treatment_control(self):
        ChipSeqPipeline(self.settings).main(
            ref_fa=f'{self.indir}/chr22.fa',
            treatment_fq1=f'{self.indir}/test_ATO_0_KEAP1_S4_R1_001.fastq.gz',
            treatment_fq2=f'{self.indir}/test_ATO_0_KEAP1_S4_R2_001.fastq.gz',
            control_fq1=f'{self.indir}/test_ATO_0_Input_S1_R1_001.fastq.gz',
            control_fq2=f'{self.indir}/test_ATO_0_Input_S1_R2_001.fastq.gz',

            base_quality_cutoff=20,
            min_read_length=20,

            read_aligner='bowtie2',
            bowtie2_mode='sensitive',
            discard_bam=False,

            skip_mark_duplicates=False,

            macs_effective_genome_size='hs',
            macs_fdr=0.05,

            genome_version='hg38',
            motif_finding_fragment_size=20
        )

    def test_treatment_only(self):
        ChipSeqPipeline(self.settings).main(
            ref_fa=f'{self.indir}/chr22.fa',
            treatment_fq1=f'{self.indir}/test_ATO_0_KEAP1_S4_R1_001.fastq.gz',
            treatment_fq2=f'{self.indir}/test_ATO_0_KEAP1_S4_R2_001.fastq.gz',
            control_fq1=None,
            control_fq2=None,

            base_quality_cutoff=20,
            min_read_length=20,

            read_aligner='bowtie2',
            bowtie2_mode='sensitive',
            discard_bam=False,

            skip_mark_duplicates=False,

            macs_effective_genome_size='hs',
            macs_fdr=0.05,

            genome_version='hg38',
            motif_finding_fragment_size=20
        )
