from chip_seq_pipeline.mark_duplicates import MarkDuplicates
from .setup import TestCase


class TestGATKMarkDuplicates(TestCase):

    def setUp(self):
        self.set_up(py_path=__file__)

    def tearDown(self):
        self.tear_down()

    def test_main(self):
        t, c = MarkDuplicates(self.settings).main(
            treatment_bam=f'{self.indir}/sorted-treatment.bam',
            control_bam=f'{self.indir}/sorted-control.bam'
        )
        self.assertFileExists(f'{self.workdir}/sorted-treatment-mark-duplicates.bam', t)
        self.assertFileExists(f'{self.workdir}/sorted-control-mark-duplicates.bam', c)
