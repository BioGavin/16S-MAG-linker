import subprocess


def excuteCommand(com):
    ex = subprocess.Popen(com, stdout=subprocess.PIPE, shell=True)
    out, err = ex.communicate()
    status = ex.wait()
    print("cmd in:", com)
    print("cmd out: ", out.decode())
    return out.decode()


def aniCompare(query, ref):
    input_data = ['fastANI', '-q', query, '--rl', ref, '-o', 'aniResult.txt']
    excuteCommand(input_data)
