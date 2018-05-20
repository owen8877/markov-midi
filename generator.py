from MidoHelper import InstrumentHelper, MidoHelper
from markov import getCompoundRandomMusic, getIndependentRandomMusic


def getCompoundRandomMusicWrapper(input: str, degree: int, instrumentTracks):
    inst = list(instrumentTracks.values())
    inputFile = 'music/sample/{}.mid'.format(input)
    m = getCompoundRandomMusic(degree, *[MidoHelper.read(inputFile, trackId=x).getDefaultTrackNotes() for x in instrumentTracks.keys()])
    sample = MidoHelper.read(inputFile, trackId=1)
    output = MidoHelper(sample.tempo, sample.numerator, sample.denominator)
    for i, st in enumerate(m):
        output.addTrack(st, inst[i])
    output.export("music/output/{input}-compound-deg{degree}-{ins}.mid".format(degree=degree, ins='-'.join([x.name for x in instrumentTracks.values()]), input=input))


def getIndependentRandomMusicWrapper(input: str, degree: int, instrumentTracks, ignoreDuration: bool=False):
    inst = list(instrumentTracks.values())
    inputFile = 'music/sample/{}.mid'.format(input)
    m = getIndependentRandomMusic(degree, *[MidoHelper.read(inputFile, trackId=x).getDefaultTrackNotes() for x in instrumentTracks.keys()])
    sample = MidoHelper.read(inputFile, trackId=1)
    output = MidoHelper(sample.tempo, sample.numerator, sample.denominator)
    for i, st in enumerate(m):
        output.addTrack(st, inst[i])
    output.export("music/output/{input}-independent-deg{degree}-{ins}{ignore}.mid".format(degree=degree, ins='-'.join([x.name for x in instrumentTracks.values()]), input=input, ignore="-ignore" if ignoreDuration else ""), ignoreDuration=ignoreDuration)


def showSampleInfo(input: str):
    from mido import MidiFile
    midi = MidiFile('music/sample/{}.mid'.format(input))
    for i, t in enumerate(midi.tracks):
        print('Track: {}, Instrument: {}'.format(i, t.name))

cupheadITS = {
    1: InstrumentHelper.Clarinet,
    4: InstrumentHelper.Bassoon,
    7: InstrumentHelper.Violin,
}
getCompoundRandomMusicWrapper('cuphead', 1, cupheadITS)
getIndependentRandomMusicWrapper('cuphead', 1, {1: InstrumentHelper.Clarinet})
getIndependentRandomMusicWrapper('cuphead', 1, {1: InstrumentHelper.Clarinet}, ignoreDuration=True)
# showSampleInfo('cuphead')

K465ITS = {
    1: InstrumentHelper.Violin,
    2: InstrumentHelper.Violin,
    3: InstrumentHelper.Viola,
    4: InstrumentHelper.Cello,
}
getCompoundRandomMusicWrapper('K465', 4, K465ITS)
getIndependentRandomMusicWrapper('K465', 2, K465ITS)
getIndependentRandomMusicWrapper('K465', 2, {1: InstrumentHelper.Violin})
# showSampleInfo('K465')

RV156ITS = {
    1: InstrumentHelper.Violin,
    2: InstrumentHelper.Violin,
    3: InstrumentHelper.Viola,
    4: InstrumentHelper.Cello,
    5: InstrumentHelper.Cello,
    6: InstrumentHelper.Harpsichord,
}
getCompoundRandomMusicWrapper('RV156', 4, RV156ITS)
getIndependentRandomMusicWrapper('RV156', 2, RV156ITS)
getIndependentRandomMusicWrapper('RV156', 2, {4: InstrumentHelper.Cello})
# showSampleInfo('RV156')

MahlerITS = {
    1: InstrumentHelper.Violin,
    2: InstrumentHelper.Violin,
    3: InstrumentHelper.Viola,
    4: InstrumentHelper.Viola,
    5: InstrumentHelper.Cello,
    6: InstrumentHelper.Contrabass,
}
getCompoundRandomMusicWrapper('Mahler', 4, MahlerITS)
getIndependentRandomMusicWrapper('Mahler', 4, MahlerITS)
getIndependentRandomMusicWrapper('Mahler', 4, {3: InstrumentHelper.Viola})
# showSampleInfo('Mahler')