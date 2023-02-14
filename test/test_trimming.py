from chip_seq_pipeline.trimming import Trimming
from .setup import TestCase


class TestTrimming(TestCase):

    def setUp(self):
        self.set_up(py_path=__file__)

    def tearDown(self):
        self.tear_down()

    def test_main(self):
        treatment_fq1, treatment_fq2, control_fq1, control_fq2 = Trimming(self.settings).main(
            treatment_fq1=f'{self.indir}/test_ATO_0_Input_S1_R1_001.fastq.gz',
            treatment_fq2=f'{self.indir}/test_ATO_0_Input_S1_R2_001.fastq.gz',
            control_fq1=f'{self.indir}/test_ATO_0_KEAP1_S4_R1_001.fastq.gz',
            control_fq2=f'{self.indir}/test_ATO_0_KEAP1_S4_R2_001.fastq.gz',
            base_quality_cutoff=20,
            min_read_length=20
        )
        for expected, actual in [
            (f'{self.workdir}/test_ATO_0_Input_S1_R1_001_val_1.fq.gz', treatment_fq1),
            (f'{self.workdir}/test_ATO_0_Input_S1_R2_001_val_2.fq.gz', treatment_fq2),
            (f'{self.workdir}/test_ATO_0_KEAP1_S4_R1_001_val_1.fq.gz', control_fq1),
            (f'{self.workdir}/test_ATO_0_KEAP1_S4_R2_001_val_2.fq.gz', control_fq2),
        ]:
            self.assertFileExists(expected, actual)
