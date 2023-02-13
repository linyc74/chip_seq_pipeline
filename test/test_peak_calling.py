from os.path import exists
from chip_seq_pipeline.peak_calling import PeakCalling
from .setup import TestCase


class TestPeakCalling(TestCase):

    def setUp(self):
        self.set_up(py_path=__file__)

    def tearDown(self):
        self.tear_down()

    def test_treatment_control(self):
        peak_files = PeakCalling(self.settings).main(
            treatment_bam=f'{self.indir}/sorted-treatment.bam',
            control_bam=f'{self.indir}/sorted-control.bam',
            macs_effective_genome_size='5.1e7',  # size of chr22
            macs_fdr=0.05
        )
        for f in peak_files:
            self.assertTrue(exists(f))

    def test_treatment_only(self):
        peak_files = PeakCalling(self.settings).main(
            treatment_bam=f'{self.indir}/sorted-treatment.bam',
            control_bam=None,
            macs_effective_genome_size='5.1e7',  # size of chr22
            macs_fdr=0.05
        )
        for f in peak_files:
            self.assertTrue(exists(f))
