import util

input_data = ['makeblastdb -in 16SrRNA.fasta -dbtype nucl -out ref -parse_seqids']
util.excuteCommand(input_data)