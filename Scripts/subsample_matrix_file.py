import sys
import Oligotyping.utils.utils as utils


def main(matrix_file, cols_to_remove = None, rows_to_remove = None, output_file = None):
    if cols_to_remove == None and rows_to_remove == None:
        print 'Error: both cols and rows to remove are empty. Exiting.'
        sys.exit()
    
    matrix = open(matrix_file)
    header = matrix.readline().strip().split('\t')
    rows = []

    for line in matrix.readlines():
        rows.append(line.strip().split('\t'))
   
    cols_to_keep = range(0, len(header))
    rows_to_keep = range(0, len(rows))
    
    if cols_to_remove:
        for i in range(0, len(header)):
            if header[i] in cols_to_remove:
                cols_to_keep.remove(i)

    if rows_to_remove:
        for i in range(0, len(rows)):
            if rows[i][0] in rows_to_remove:
                rows_to_keep.remove(i)

    output = open(output_file, 'w')
    
    output.write('%s\n' % '\t'.join([header[i] for i in cols_to_keep]))
    for i in rows_to_keep:
        output.write('%s\n' % '\t'.join([rows[i][c] for c in cols_to_keep]))
    
    output.close()


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description='Removes COLS and ROWS from a matrix file')
    parser.add_argument('matrix_file', metavar = 'FILE',
                        help = 'TAB delimited matrix to be processed')
    parser.add_argument('-c', '--cols-to-remove', metavar = 'FILE', default = None,
                        help = 'Columns to be removed from the matrix (one column id in each line)')
    parser.add_argument('-r', '--rows-to-remove', metavar = 'FILE', default = None,
                        help = 'Rows to be removed from the matrix (one row id in each line)')
    parser.add_argument('-o', '--output-file', default = None,
                        help = 'Output file name')

    args = parser.parse_args()


    def get_content(f):
        if f:
            return [x.strip() for x in open(f).readlines()]
        else:
            return None


    if not args.output_file:
        output_file = args.matrix_file + '-SUBSAMPLED'
    else:
        output_file = args.output_file

    cols_to_remove = get_content(args.cols_to_remove)
    rows_to_remove = get_content(args.rows_to_remove)
  
    sys.exit(main(args.matrix_file, cols_to_remove, rows_to_remove, output_file))

