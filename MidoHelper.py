import mido
from mido import Message, MidiFile, MidiTrack, MetaMessage


class Note:
    PitchNameMapping = {'C': 0, 'D': 2, 'E': 4, 'F': 5, 'G': 7, 'A': 9, 'B': 11}

    def __init__(self, pitch: int, duration: float, noteOn: bool=True):
        self.pitch = pitch
        self.duration = duration
        self.noteOn = noteOn

    @staticmethod
    def StrPitch(strPitch: str, denominator: int):
        name = strPitch[0]
        octave = int(strPitch[1])
        return Note(16 + Note.PitchNameMapping[name] + 8 * octave, 1.0 / denominator)

    @staticmethod
    def Rest(denominator: int):
        return Note(0, 1.0 / denominator, noteOn=False)


class MidoHelper:
    def __init__(self, notes: list, tempo: int=60, numerator: int=4, denominator: int=4):
        self.notes = notes
        self.tempo = tempo
        self.numerator = numerator
        self.denominator = denominator

    def export(self, filename: str):
        mid = MidiFile()

        metaTrack = MidiTrack()
        mid.tracks.append(metaTrack)
        metaTrack.append(MetaMessage('set_tempo', tempo=int(mido.tempo2bpm(self.tempo))))
        metaTrack.append(MetaMessage('time_signature', numerator=self.numerator, denominator=self.denominator))

        track = MidiTrack()
        mid.tracks.append(track)
        track.append(Message('program_change', program=72, time=0))

        delta = 480 * self.denominator
        noteDelay = 0.0
        for note in self.notes:
            if note.noteOn:
                track.append(Message('note_on', note=note.pitch, time=int(noteDelay)))
                noteDelay = 0
                track.append(Message('note_off', note=note.pitch, time=int(delta*note.duration)))
            else:
                noteDelay += delta*note.duration

        mid.save(filename)
