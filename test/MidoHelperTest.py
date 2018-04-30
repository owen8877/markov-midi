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
# midi.export("test.mid")

midi2 = MidoHelper.read('../cuphead.mid', trackId=1)
midi2.export('cuphead-1.mid')

midi2 = MidoHelper.read('../cuphead.mid', trackId=2)
midi2.export('cuphead-2.mid')