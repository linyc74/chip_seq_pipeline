from chip_seq_pipeline import ChipSeqPipeline
from .setup import TestCase


class TestChipSeqPipeline(TestCase):

    def setUp(self):
        self.set_up(py_path=__file__)

    def tearDown(self):
        self.tear_down()

    def test_main(self):
        ChipSeqPipeline(self.settings).main(
            ref_fa=f'{self.indir}/chr22.fa',
            treatment_fq1=f'{self.indir}/test_ATO_0_KEAP1_S4_R1_001.fastq.gz',
            treatment_fq2=f'{self.indir}/test_ATO_0_KEAP1_S4_R2_001.fastq.gz',
            control_fq1=f'{self.indir}/test_ATO_0_Input_S1_R1_001.fastq.gz',
            control_fq2=f'{self.indir}/test_ATO_0_Input_S1_R2_001.fastq.gz',
            gtf=f'{self.indir}/X.gtf',

            base_quality_cutoff=20,
            min_read_length=20,
            max_read_length=150,

            read_aligner='bowtie2',
            bowtie2_mode='sensitive',
            discard_bam=False,

            effective_genome_size='hs',
            fdr=0.05
        )
