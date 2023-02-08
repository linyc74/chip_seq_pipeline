from chip_seq_pipeline.peak_calling import PeakCalling
from .setup import TestCase


class TestPeakCalling(TestCase):

    def setUp(self):
        self.set_up(py_path=__file__)

    def tearDown(self):
        self.tear_down()

    def test_main(self):
        PeakCalling(self.settings).main(
            treatment_bam=f'{self.indir}/treatment.bam',
            control_bam=f'{self.indir}/control.bam',
            peak_caller='macs'
        )
