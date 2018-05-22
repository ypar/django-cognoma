import os
from urllib.request import urlretrieve

from django.core.management.base import BaseCommand

COMMIT_HASH = 'da832c5edc1ca4d3f665b038d15b19fced724f4c'
REPO_URL_TEMPLATE = 'https://github.com/cognoma/cancer-data/raw/{commit_hash}/{directory}/{filename}'

# Genes have their own repo
GENES_COMMIT_HASH = "ad9631bb4e77e2cdc5413b0d77cb8f7e93fc5bee"


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument(
            '--path',
            dest='path',
            default='data',
            help='Path to location of data files.',
        )

    def handle(self, *args, **options):
        if not os.path.exists(options['path']):
            os.makedirs(options['path'])

        files_in_data_path = ['samples.tsv', 'mutation-matrix.tsv.bz2']

        for filename in files_in_data_path:
            table_path = os.path.join(options['path'], filename)
            if not os.path.exists(table_path):
                table_url = REPO_URL_TEMPLATE.format(
                    commit_hash=COMMIT_HASH, directory="data", filename=filename)
                print("Downloading " + filename + " data from: " + table_url)
                urlretrieve(table_url, table_path)

        filename = 'genes.tsv'
        genes_path = os.path.join(options['path'], filename)
        if not os.path.exists(genes_path):
            genes_url = "https://github.com/cognoma/genes/raw/" + GENES_COMMIT_HASH + "/data/" + filename
            print("Downloading genes data from: " + genes_url)
            urlretrieve(genes_url, genes_path)

        # Diseases lives in a different directory because it is
        # composed of inputs from external locations.
        filename = 'diseases.tsv'
        disease_path = os.path.join(options['path'], filename)
        if not os.path.exists(disease_path):
            disease_url = REPO_URL_TEMPLATE.format(
                commit_hash=COMMIT_HASH, directory="mapping", filename=filename)
            print("Downloading diseases data from: " + disease_url)
            urlretrieve(disease_url, disease_path)
