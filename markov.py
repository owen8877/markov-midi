import MidoHelper
import random


def getTransitionMatrix(seq):
    init = dict()
    cnt = dict()
    for i in range(len(seq)):
        if init.get(seq[i].pitch) is None:
            init[seq[i].pitch] = 1
        else:
            init[seq[i].pitch] = init[seq[i].pitch] + 1
        if i + 1 < len(seq):
            tr = (seq[i].pitch, seq[i + 1].pitch)
            if cnt.get(tr) is None:
                cnt[tr] = 1
            else:
                cnt[tr] = cnt[tr] + 1
    return (init, cnt)


def generateRandomNotes(init: dict, cnt: dict, length: int):
    ret = []
    if length == 0:
        return ret
    cur = random.choices(init.keys(), init.values())
    ret.append(cur)
    for i in range(length - 1):
        weight = []
        for note in init.keys():
            if cnt.get((cur, note)) is None:
                weight.append(0)
            else:
                weight.append(cnt[(cur, note)])
        cur = random.choices(init.keys(), weight)
        ret.append(cur)
    return ret

