from MidoHelper import Note, MidoHelper
import random

denominators = [4, 8, 16]
# notes = [Note(random.randint(60, 71), 1/random.choice(denominators)) for i in range(20)]
notes = [
    Note.StrPitch('C5', 4),
    Note.StrPitch('C5', 4),
    Note.StrPitch('G5', 4),
    Note.StrPitch('G5', 4),
    Note.StrPitch('A5', 4),
    Note.StrPitch('A5', 4),
    Note.StrPitch('G5', 4),
    Note.StrPitch('G5', 4),
]

midi = MidoHelper(notes, tempo=90, denominator=4)
midi.export("test.mid")