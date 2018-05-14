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


inst = [InstrumentHelper.Clarinet, InstrumentHelper.Bassoon, InstrumentHelper.Violin]
m = getCompoundRandomMusic(1, *[MidoHelper.read('cuphead.mid', trackId=x).getDefaultTrackNotes() for x in [1, 4, 7]])
output = MidoHelper.read("cuphead.mid", trackId = 1)
output = MidoHelper(output.tempo, output.numerator, output.denominator)
for i, st in enumerate(m):
    output.addTrack(st, inst[i])
output.export("cuphead_random_compound_deg1.mid")

m = getIndependentRandomMusic(1, *[MidoHelper.read('cuphead.mid', trackId=x).getDefaultTrackNotes() for x in [1, 4, 7]])
output = MidoHelper.read("cuphead.mid", trackId = 1)
output = MidoHelper(output.tempo, output.numerator, output.denominator)
for i, st in enumerate(m):
    output.addTrack(st, inst[i])
output.export("cuphead_random_independent_deg1.mid")
#midi = MidoHelper.read('cuphead.mid', trackId=1)
#midi2 = MidoHelper.read('cuphead.mid', trackId=2)
#res = splitNotes(midi)
#res2 = splitNotes(midi2)
#init, cnt = getTransitionMatrix(tuple(zip(res, res2)))
#rdm = generateRandomNotes(init, cnt, min(len(res), len(res2)))

#output = MidoHelper(midi.tempo, midi.numerator, midi.denominator)
#output.addTrack(res)
#output.export("cuphead1_recovered.mid")
#for deg in range(1, 4):
#    cupheadinit, cupheadtrans = getTransitionMatrix(midi.getDefaultTrackNotes(), deg)
#    output = MidoHelper(midi.tempo, midi.numerator, midi.denominator)
#    output.addTrack(generateRandomNotes(cupheadinit, cupheadtrans, len(midi.getDefaultTrackNotes()) - deg + 1))
#    output.export('cuphead1_random_deg{0}.mid'.format(deg))
#deg = 1
###
#clarinetMidi = MidoHelper.read('cuphead.mid', trackId=1)
#bassonMidi = MidoHelper.read('cuphead.mid', trackId=4)
#violinMidi = MidoHelper.read('cuphead.mid', trackId=7)
#cupheadinitcl, cupheadtranscl = getTransitionMatrix(clarinetMidi.getDefaultTrackNotes(), 4)
#cupheadinitba, cupheadtransba = getTransitionMatrix(bassonMidi.getDefaultTrackNotes(), 4)
#cupheadinitvi, cupheadtransvi = getTransitionMatrix(bassonMidi.getDefaultTrackNotes(), 4)
#output = MidoHelper(midi.tempo, midi.numerator, midi.denominator)
#output.addTrack(generateRandomNotes(cupheadinitcl, cupheadtranscl, len(midi.getDefaultTrackNotes()) - deg + 1), InstrumentHelper.Clarinet)
#output.addTrack(generateRandomNotes(cupheadinitba, cupheadtransba, len(midi.getDefaultTrackNotes()) - deg + 1), InstrumentHelper.Bassoon)
#output.addTrack(generateRandomNotes(cupheadinitvi, cupheadtransvi, len(midi.getDefaultTrackNotes()) - deg + 1), InstrumentHelper.Violin)
#output.export('clarinet-basson.mid')
