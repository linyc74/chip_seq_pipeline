import argparse
import chip_seq_pipeline


__VERSION__ = '1.0.0-beta'


PURPLE = '\033[95m'
CYAN = '\033[96m'
DARKCYAN = '\033[36m'
BLUE = '\033[94m'
GREEN = '\033[92m'
YELLOW = '\033[93m'
RED = '\033[91m'
BOLD = '\033[1m'
UNDERLINE = '\033[4m'
END = '\033[0m'


PROG = 'python chip_seq_pipeline'
DESCRIPTION = f'{BOLD}ChIP-seq pipeline (version {__VERSION__}) by Yu-Cheng Lin (ylin@nycu.edu.tw){END}'
REQUIRED = [
    {
        'keys': ['-r', '--ref-fa'],
        'properties': {
            'type': str,
            'required': True,
            'help': 'path to the reference genome fasta file',
        }
    },
    {
        'keys': ['-g', '--gtf'],
        'properties': {
            'type': str,
            'required': True,
            'help': 'path to the general transfer format gtf file',
        }
    },
    {
        'keys': ['-1', '--fq1'],
        'properties': {
            'type': str,
            'required': True,
            'help': 'path to the read 1 fastq file',
        }
    },
    {
        'keys': ['-2', '--fq2'],
        'properties': {
            'type': str,
            'required': True,
            'help': 'path to the read 2 fastq file',
        }
    },
]
OPTIONAL = [
    {
        'keys': ['--base-quality-cutoff'],
        'properties': {
            'type': int,
            'required': False,
            'default': 20,
            'help': 'base quality cutoff for cutadapt trimming (default: %(default)s)',
        }
    },
    {
        'keys': ['--min-read-length'],
        'properties': {
            'type': int,
            'required': False,
            'default': 20,
            'help': 'minimum read length after trimming (default: %(default)s)',
        }
    },
    {
        'keys': ['--max-read-length'],
        'properties': {
            'type': int,
            'required': False,
            'default': -1,
            'help': 'maximum read length after trimming, defualt for no limit (default: %(default)s)',
        }
    },
    {
        'keys': ['--read-aligner'],
        'properties': {
            'type': str,
            'required': False,
            'choices': ['bowtie2', 'bwa'],
            'default': 'bowtie2',
            'help': 'read aligner (default: %(default)s)',
        }
    },
    {
        'keys': ['--bowtie2-mode'],
        'properties': {
            'type': str,
            'required': False,
            'choices': [
                'very-fast',
                'very-fast-local',
                'fast',
                'fast-local',
                'sensitive',
                'sensitive-local',
                'very-sensitive',
                'very-sensitive-local'
            ],
            'default': 'sensitive',
            'help': 'bowtie2 preset mode (default: %(default)s)',
        }
    },
    {
        'keys': ['--discard-bam'],
        'properties': {
            'action': 'store_true',
            'help': 'do not save sorted BAM files in outdir',
        }
    },
    {
        'keys': ['-o', '--outdir'],
        'properties': {
            'type': str,
            'required': False,
            'default': 'rna_seq_pipeline_outdir',
            'help': 'path to the output directory (default: %(default)s)',
        }
    },
    {
        'keys': ['-t', '--threads'],
        'properties': {
            'type': int,
            'required': False,
            'default': 4,
            'help': 'number of CPU threads (default: %(default)s)',
        }
    },
    {
        'keys': ['-d', '--debug'],
        'properties': {
            'action': 'store_true',
            'help': 'debug mode',
        }
    },
    {
        'keys': ['-h', '--help'],
        'properties': {
            'action': 'help',
            'help': 'show this help message',
        }
    },
    {
        'keys': ['-v', '--version'],
        'properties': {
            'action': 'version',
            'version': __VERSION__,
            'help': 'show version',
        }
    },
]


class EntryPoint:

    parser: argparse.ArgumentParser

    def main(self):
        self.set_parser()
        self.add_required_arguments()
        self.add_optional_arguments()
        self.run()

    def set_parser(self):
        self.parser = argparse.ArgumentParser(
            prog=PROG,
            description=DESCRIPTION,
            add_help=False,
            formatter_class=argparse.RawTextHelpFormatter)

    def add_required_arguments(self):
        group = self.parser.add_argument_group(f'{BOLD}{RED}Required{END}')
        for item in REQUIRED:
            group.add_argument(*item['keys'], **item['properties'])

    def add_optional_arguments(self):
        group = self.parser.add_argument_group(f'{BOLD}{YELLOW}Optional{END}')
        for item in OPTIONAL:
            group.add_argument(*item['keys'], **item['properties'])

    def run(self):
        args = self.parser.parse_args()
        print(f'Start running ChIP-seq pipeline version {__VERSION__}\n', flush=True)
        # chip_seq_pipeline.Main().main(
        #     ref_fa=args.ref_fa,
        #     gtf=args.gtf,
        #     fq1=args.fq1,
        #     fq2=args.fq2,
        #     adapter=args.adapter,
        #     base_quality_cutoff=args.base_quality_cutoff,
        #     min_read_length=args.min_read_length,
        #     max_read_length=args.max_read_length,
        #     read_aligner=args.read_aligner,
        #     bowtie2_mode=args.bowtie2_mode,
        #     discard_bam=args.discard_bam,
        #     min_count_mapq=args.min_count_mapq,
        #     nonunique_count=args.nonunique_count,
        #     stranded_count=args.stranded_count,
        #     outdir=args.outdir,
        #     threads=args.threads,
        #     debug=args.debug)


if __name__ == '__main__':
    EntryPoint().main()
