from MidoHelper import Note, InstrumentHelper, MidoHelper
from functools import reduce
import random


def getTransitionMatrix(seq, deg = 1):
    init = dict()
    cnt = dict()
    cseq = tuple()
    curSymbol = tuple()
    for i in range(deg):
        curSymbol = curSymbol + (seq[i],)
    cseq = cseq + (curSymbol, )
    for i in range(deg, len(seq)):
        curSymbol = curSymbol[:-1] + (seq[i],)
        cseq = cseq + (curSymbol, )
    for i in range(len(cseq)):
        if init.get(cseq[i]) is None:
            init[cseq[i]] = 1
        else:
            init[cseq[i]] = init[cseq[i]] + 1
        if i + 1 < len(cseq):
            tr = (cseq[i], cseq[i + 1])
            if cnt.get(tr) is None:
                cnt[tr] = 1
            else:
                cnt[tr] = cnt[tr] + 1
    return (init, cnt)


def generateRandomNotes(init: dict, cnt: dict, length: int):
    gen = []
    if length == 0:
        return gen
    cur = random.choices(list(init.keys()), list(init.values()), k = 1)[0]
    gen.append(cur)
    for i in range(length - 1):
        weight = []
        terminal = True
        for note in init.keys():
            if cnt.get((cur, note)) is None:
                weight.append(0)
            else:
                weight.append(cnt[(cur, note)])
                terminal = False
        if terminal:
            cur = random.choices(list(init.keys()), list(init.values()), k=1)[0]
        else:
            cur = random.choices(list(init.keys()), weight)[0]
        gen.append(cur)
    ret = gen[0] + tuple(map(lambda x: x[-1], gen[1:]))
    return ret


def splitNotes(notes):
    return reduce(lambda x, y: x + y, map(lambda x: (Note(x.pitch, 1.0 / 8, x.noteOn), ) * round(x.duration * 8), notes))


def getCompoundRandomMusic(deg: int, *trk):
    composedSeq = tuple(zip(*tuple(map(splitNotes, trk))))
    init, cnt = getTransitionMatrix(composedSeq, deg)
    res = generateRandomNotes(init, cnt, len(composedSeq) - deg + 1)
    return reduce(lambda x, y: [x[i] + y[i] for i in range(len(x))], list(map(lambda x: [(x[i], ) for i in range(len(x))], res)))


def getIndependentRandomMusic(deg: int, *trk):
    ret = tuple()
    for tk in trk:
        init, cnt = getTransitionMatrix(tk, deg)
        ret = ret + (generateRandomNotes(init, cnt, len(tk) - deg + 1), )
    return ret