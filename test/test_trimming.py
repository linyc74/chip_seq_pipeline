from chip_seq_pipeline.trimming import Trimming
from .setup import TestCase


class TestTrimming(TestCase):

    def setUp(self):
        self.set_up(py_path=__file__)

    def tearDown(self):
        self.tear_down()

    def test_paired_end(self):
        trimmed_fq1, trimmed_fq2 = Trimming(self.settings).main(
            fq1=f'{self.indir}/tumor.1.fq.gz',
            fq2=f'{self.indir}/tumor.2.fq.gz',
            base_quality_cutoff=20,
            min_read_length=20,
            max_read_length=-1,
        )
        for expected, actual in [
            (f'{self.workdir}/tumor.1_val_1.fq.gz', trimmed_fq1),
            (f'{self.workdir}/tumor.2_val_2.fq.gz', trimmed_fq2),
        ]:
            self.assertFileExists(expected, actual)

    def test_single_end(self):
        trimmed_fq1, trimmed_fq2 = Trimming(self.settings).main(
            fq1=f'{self.indir}/tumor.1.fq.gz',
            fq2=None,
            base_quality_cutoff=20,
            min_read_length=20,
            max_read_length=-1,
        )
        self.assertFileExists(f'{self.workdir}/tumor.1_trimmed.fq.gz', trimmed_fq1)
        self.assertIsNone(trimmed_fq2)
