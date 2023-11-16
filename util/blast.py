import subprocess


def excuteCommand(com):
    ex = subprocess.Popen(com, stdout=subprocess.PIPE, shell=True)
    out, err = ex.communicate()
    status = ex.wait()
    print("cmd in:", com)
    print("cmd out: ", out.decode())
    return out.decode()


if __name__ == '__main__':
    input_data = ['blastn', '-query', 'scaffold_AF07-33B.fa', '-db', 'ref', '-out', 'blastResult.txt', '-outfmt', '6',
                  '-evalue', '1e-5']
    excuteCommand(input_data)
