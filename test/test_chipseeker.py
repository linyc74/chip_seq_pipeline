import shutil
from os.path import exists
from chip_seq_pipeline.chipseeker import ChIPseeker
from .setup import TestCase


class TestChIPseeker(TestCase):

    def setUp(self):
        self.set_up(py_path=__file__)

    def tearDown(self):
        self.tear_down()

    def test_main(self):
        self.__move_test_files_to_outdir()

        ChIPseeker(self.settings).main(
            peak_files=[
                f'{self.outdir}/homer/factor-peaks.txt',
                f'{self.outdir}/homer/histone-regions.txt',
                f'{self.outdir}/homer/empty.txt',
                f'{self.outdir}/macs2/broad_peaks.broadPeak',
                f'{self.outdir}/macs2/narrow_peaks.narrowPeak',
                f'{self.outdir}/macs2/empty.txt',
            ]
        )

    def __move_test_files_to_outdir(self):
        for d in ['homer', 'macs2']:
            src = f'{self.indir}/{d}'
            dst = f'{self.outdir}/{d}'
            if exists(dst):
                shutil.rmtree(dst)
            shutil.copytree(src, dst)
