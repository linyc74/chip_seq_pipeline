from chip_seq_pipeline import ChipSeqPipeline
from .setup import TestCase


class TestChipSeqPipeline(TestCase):

    def setUp(self):
        self.set_up(py_path=__file__)

    def tearDown(self):
        self.tear_down()

    def test_main(self):
        ChipSeqPipeline(self.settings).main(
            ref_fa=f'{self.indir}/',
            treatment_fq1=f'{self.indir}/',
            treatment_fq2=f'{self.indir}/',
            control_fq1=f'{self.indir}/',
            control_fq2=f'{self.indir}/',
            gtf=f'{self.indir}/',

            base_quality_cutoff=20,
            min_read_length=20,
            max_read_length=150,

            read_aligner='bowtie2',
            bowtie2_mode='sensitive',
            discard_bam=False,

            peak_caller='MACS',
            effective_genome_size='hs',
            fdr=0.05
        )
