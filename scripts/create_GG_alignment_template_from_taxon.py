#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (C) 2010 - 2012, A. Murat Eren
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation; either version 2 of the License, or (at your option)
# any later version.
#
# Please read the COPYING file.

import os
import sys
import argparse

sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), '..'))
import lib.fastalib as u

def gen_tmpl(taxon, otu_id_to_greengenes, greengenes_alignment, output_file_path = None):
    ids = []
    
    for id, tax in [line.strip().split('\t') for line in open(otu_id_to_greengenes).readlines()]:
        if tax.find(taxon) > 0:
            ids.append(id)
    
    ids = list(set(ids))
    print '%d ids found for %s.' % (len(ids), taxon)
    
    template = u.FastaOutput('%s.tmpl' % taxon)
    fasta = u.SequenceSource(greengenes_alignment)
    while fasta.next():
        if fasta.id in ids:
            template.store(fasta, split = False)
            ids.remove(fasta.id)
    
    fasta.close()
    template.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Create GreenGenes Alignment Template')
    parser.add_argument('taxon', metavar = 'TAXON',
                        help = '"Taxon" name to be searched in GreenGenes')
    parser.add_argument('otu_id_to_greengenes', metavar = 'OTU_ID_TO_GREENGENES',
                        help = 'Path to the "otu_id_to_greengenes" file. You can download it from \
                               "http://greengenes.lbl.gov/Download/OTUs/gg_otus_6oct2010/taxonomies/otu_id_to_greengenes.txt"')
    parser.add_argument('greengenes_alignment', metavar = 'GREENGENES_ALIGNMENT',
                        help = 'Path to the GreenGenes alignment file. You can download it from \
                               "http://greengenes.lbl.gov/Download/OTUs/gg_otus_6oct2010/rep_set/gg_97_otus_6oct2010_aligned.fasta"')
    parser.add_argument('-o', '--output', help = 'Output file name', default = None)


    args = parser.parse_args()
    gen_tmpl(args.taxon, args.otu_id_to_greengenes, args.greengenes_alignment, args.output)
