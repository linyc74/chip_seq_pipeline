from chip_seq_pipeline.mapping import Mapping
from .setup import TestCase


class TestMapping(TestCase):

    def setUp(self):
        self.set_up(py_path=__file__)

    def tearDown(self):
        self.tear_down()

    def test_bwa(self):
        treatment_bam, control_bam = Mapping(self.settings).main(
            ref_fa=f'{self.indir}/chr22.fa',
            treatment_fq1=f'{self.indir}/small_ATO_0_KEAP1_S4_R1_001.fastq.gz',
            treatment_fq2=f'{self.indir}/small_ATO_0_KEAP1_S4_R2_001.fastq.gz',
            control_fq1=f'{self.indir}/small_ATO_0_Input_S1_R1_001.fastq.gz',
            control_fq2=f'{self.indir}/small_ATO_0_Input_S1_R2_001.fastq.gz',
            read_aligner='bwa',
            bowtie2_mode='sensitive',
            discard_bam=True
        )
        self.assertFileExists(f'{self.workdir}/treatment-sorted.bam', treatment_bam)
        self.assertFileExists(f'{self.workdir}/control-sorted.bam', control_bam)

    def test_bowtie2(self):
        treatment_bam, control_bam = Mapping(self.settings).main(
            ref_fa=f'{self.indir}/chr22.fa',
            treatment_fq1=f'{self.indir}/small_ATO_0_KEAP1_S4_R1_001.fastq.gz',
            treatment_fq2=f'{self.indir}/small_ATO_0_KEAP1_S4_R2_001.fastq.gz',
            control_fq1=None,
            control_fq2=None,
            read_aligner='bowtie2',
            bowtie2_mode='sensitive',
            discard_bam=False
        )
        self.assertFileExists(f'{self.outdir}/treatment-sorted.bam', treatment_bam)
        self.assertIsNone(control_bam)
