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
    output.export("music/output/{input}_compound_deg{degree}_{ins}.mid".format(degree=degree, ins='_'.join([x.name for x in instrumentTracks.values()]), input=input))


def getIndependentRandomMusicWrapper(input: str, degree: int, instrumentTracks):
    inst = list(instrumentTracks.values())
    inputFile = 'music/sample/{}.mid'.format(input)
    m = getIndependentRandomMusic(degree, *[MidoHelper.read(inputFile, trackId=x).getDefaultTrackNotes() for x in instrumentTracks.keys()])
    sample = MidoHelper.read(inputFile, trackId=1)
    output = MidoHelper(sample.tempo, sample.numerator, sample.denominator)
    for i, st in enumerate(m):
        output.addTrack(st, inst[i])
    output.export("music/output/{input}_independent_deg{degree}_{ins}.mid".format(degree=degree, ins='_'.join([x.name for x in instrumentTracks.values()]), input=input))


def showSampleInfo(input: str):
    from mido import MidiFile
    midi = MidiFile('music/sample/{}.mid'.format(input))
    for i, t in enumerate(midi.tracks):
        print('Track: {}, Instrument: {}'.format(i, t.name))

# cupheadITS = {
#     1: InstrumentHelper.Clarinet,
#     4: InstrumentHelper.Bassoon,
#     7: InstrumentHelper.Violin,
# }
# getCompoundRandomMusicWrapper('cuphead', 1, cupheadITS)
# getIndependentRandomMusicWrapper('cuphead', 1, cupheadITS)
# showSampleInfo('cuphead')

# K465ITS = {
#     1: InstrumentHelper.Violin,
#     2: InstrumentHelper.Violin,
#     3: InstrumentHelper.Viola,
#     4: InstrumentHelper.Cello,
# }
# getCompoundRandomMusicWrapper('K465', 4, K465ITS)
# getIndependentRandomMusicWrapper('K465', 2, K465ITS)
# showSampleInfo('K465')

# RV156ITS = {
#     1: InstrumentHelper.Violin,
#     2: InstrumentHelper.Violin,
#     3: InstrumentHelper.Viola,
#     4: InstrumentHelper.Cello,
#     5: InstrumentHelper.Cello,
#     6: InstrumentHelper.Harpsichord,
# }
# getCompoundRandomMusicWrapper('RV156', 4, RV156ITS)
# getIndependentRandomMusicWrapper('RV156', 2, RV156ITS)
# showSampleInfo('RV156')

MahlerITS = {
    1: InstrumentHelper.Violin,
    2: InstrumentHelper.Violin,
    3: InstrumentHelper.Viola,
    # 4: InstrumentHelper.Viola,
    5: InstrumentHelper.Cello,
    # 6: InstrumentHelper.Contrabass,
}
# getCompoundRandomMusicWrapper('Mahler', 4, MahlerITS)
getIndependentRandomMusicWrapper('Mahler', 4, MahlerITS)
showSampleInfo('Mahler')