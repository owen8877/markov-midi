import mido
from mido import Message, MidiFile, MidiTrack, MetaMessage


class Note:
    PitchNameMapping = {'C': 0, 'D': 2, 'E': 4, 'F': 5, 'G': 7, 'A': 9, 'B': 11}
    ReverseMapping = ['C', '#C', 'D', '#D', 'E', 'F', '#F', 'G', '#G', 'A', '#A', 'B']

    def __init__(self, pitch: int, duration: float, noteOn: bool=True):
        self.pitch = pitch
        self.duration = duration
        self.noteOn = noteOn

    def __str__(self):
        subIndex = self.pitch % 12
        octave = self.pitch // 12 - 1
        return '{}{} 1/{}{}'.format(Note.ReverseMapping[subIndex], octave, 1/self.duration, '' if self.noteOn else ' rest')
    
    
    def __repr__(self):
        return str(self)
    
    
    def __eq__(self, other):
        return self.pitch == other.pitch and self.duration == other.duration and self.noteOn == other.noteOn
    
    def __hash__(self):
        return hash(self.pitch) + hash(self.duration) + hash(self.noteOn)

    @staticmethod
    def StrPitch(strPitch: str, denominator: int):
        name = strPitch[0]
        octave = int(strPitch[1])
        return Note(16 + Note.PitchNameMapping[name] + 12 * octave, 1.0 / denominator)

    @staticmethod
    def Rest(denominator: int):
        return Note(0, 1.0 / denominator, noteOn=False)

    @staticmethod
    def PreciseRest(duration: float):
        return Note(0, duration, noteOn=False)


class Instrument:
    def __init__(self, value: int):
        self.value = value


class InstrumentHelper:
    Violin = Instrument(41)
    Trombone = Instrument(58)
    Bassoon = Instrument(71)
    Clarinet = Instrument(72)
    Default = Clarinet


class MidoHelper:
    def __init__(self, tempo: int=60, numerator: int=4, denominator: int=4):
        self.tracks = list()
        self.tempo = tempo
        self.numerator = numerator
        self.denominator = denominator

    def addTrack(self, notes: list, instrument: Instrument=InstrumentHelper.Default):
        self.tracks.append({'list': notes, 'instrument': instrument})
        return self

    def getDefaultTrackNotes(self):
        return self.tracks[0]['list']

    def export(self, filename: str):
        mid = MidiFile()

        metaTrack = MidiTrack()
        mid.tracks.append(metaTrack)
        metaTrack.append(MetaMessage('set_tempo', tempo=int(mido.tempo2bpm(self.tempo))))
        metaTrack.append(MetaMessage('time_signature', numerator=self.numerator, denominator=self.denominator))

        for track in self.tracks:
            midiTrack = MidiTrack()
            mid.tracks.append(midiTrack)
            program = track['instrument'].value

            midiTrack.append(Message('program_change', program=program, time=0))

            notes = track['list']
            delta = 480 * self.denominator
            noteDelay = 0.0
            for note in notes:
                if note.noteOn:
                    midiTrack.append(Message('note_on', note=note.pitch, time=int(noteDelay)))
                    noteDelay = 0
                    midiTrack.append(Message('note_off', note=note.pitch, time=int(delta*note.duration)))
                else:
                    noteDelay += delta*note.duration

        mid.save(filename)

    @staticmethod
    def read(filename: str, trackId :int=1, tempo: int=-1, numerator: int=-1, denominator: int=-1):
        mid = MidiFile(filename)

        if len(mid.tracks) <= trackId:
            raise Exception('This midi file {} has only {} tracks rather than {}.'.format(filename, len(mid.tracks), trackId))

        for metaMessage in mid.tracks[0]:
            if metaMessage.type == 'set_tempo':
                if tempo == -1:
                    tempo = mido.bpm2tempo(metaMessage.tempo)
            elif metaMessage.type == 'time_signature':
                if denominator == -1:
                    denominator = metaMessage.denominator
                if numerator == -1:
                    numerator = metaMessage.numerator

        ticksPerBeat = mid.ticks_per_beat
        delta = ticksPerBeat * denominator

        track = mid.tracks[trackId]
        notes = []
        for message in track:
            if message.type == 'note_on':
                if message.time != 0:
                    notes.append(Note.PreciseRest(message.time / delta))
            elif message.type == 'note_off':
                notes.append(Note(message.note, message.time/delta))

        return MidoHelper(tempo, numerator, denominator).addTrack(notes)