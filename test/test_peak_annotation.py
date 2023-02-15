import os.path
import shutil
from chip_seq_pipeline.peak_annotation import PeakAnnotation
from .setup import TestCase


class TestPeakAnnotation(TestCase):

    def setUp(self):
        self.set_up(py_path=__file__)

    def tearDown(self):
        self.tear_down()

    def test_main(self):
        for d in ['homer', 'macs2']:
            src = f'{self.indir}/{d}'
            dst = f'{self.outdir}/{d}'
            if os.path.exists(dst):
                shutil.rmtree(dst)
            shutil.copytree(src, dst)

        peak_files = [
            f'{self.outdir}/homer/factor-peaks.txt',
            f'{self.outdir}/homer/histone-regions.txt',
            f'{self.outdir}/macs2/broad_peaks.broadPeak',
            f'{self.outdir}/macs2/narrow_peaks.narrowPeak',
        ]

        PeakAnnotation(self.settings).main(
            peak_files=peak_files,
            genome_version='hg38'
        )
