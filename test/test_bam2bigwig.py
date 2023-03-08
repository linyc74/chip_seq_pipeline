from os.path import exists
from chip_seq_pipeline.bam2bigwig import Bam2BigWig
from .setup import TestCase


class TestBam2BigWig(TestCase):

    def setUp(self):
        self.set_up(py_path=__file__)

    def tearDown(self):
        self.tear_down()

    def test_main(self):
        Bam2BigWig(self.settings).main(
            treatment_bam=f'{self.indir}/treatment.bam',
            control_bam=f'{self.indir}/control.bam'
        )
        self.assertTrue(exists(f'{self.outdir}/treatment.bw'))
        self.assertTrue(exists(f'{self.outdir}/control.bw'))
