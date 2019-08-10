
import breakword as bw


def lfsr_hash(state):
    bw.brk()
    result = 0
    for i in range(32):
        bit = ((state >> 0) ^ (state >> 2)
               ^ (state >> 3) ^ (state >> 5)) & 1
        state = (state >> 1) | (bit << 15)
        result = (result << 1) | bit
    return result


def myhash(word):
    h = 0
    for letter in word:
        h = h ^ ord(letter)
    return lfsr_hash(h)


phrase = "No shenanigans during office hours"


if __name__ == '__main__':
    for w in phrase.split():
        h = myhash(w)
        bw.log(w, h)
