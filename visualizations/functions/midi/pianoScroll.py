import numpy as np
import time

from scipy.ndimage.filters import gaussian_filter1d


def getValueFromPercentage(value, percentage):
    return value / 100 * percentage

def applyGradientDecrease(pixels):
    pixels_length = len(pixels[0])
    for i in range(pixels_length):
        if(pixels[0][i] > 0):
            pixels[0][i] = pixels[0][i] - i / pixels_length * 2
        if(pixels[1][i] > 0):
            pixels[1][i] = pixels[1][i] - i / pixels_length * 2
        if(pixels[2][i] > 0):
            pixels[2][i] = pixels[2][i] - i / pixels_length * 2

def putPixel(strip, ledIndex, r, g, b, velocity):
    if(ledIndex < len(strip[0]) and ledIndex > -len(strip[0])):
        strip[0][ledIndex] = r / 127 * (velocity + 1)
        strip[1][ledIndex] = g / 127 * (velocity + 1)
        strip[2][ledIndex] = b / 127 * (velocity + 1)


class PianoScroll():

    def initPianoScroll(self):
        self.piano_scroll_notes_on = []
        self.pitch = 0
        self.value = 0

    def visualizePianoScroll(self):
        """Piano midi visualizer"""

        color_scheme = self.config._formatted_color_schemes[
            self.active_state.active_color_scheme_index]

        for midi_note in self.midi_datas:
            if(midi_note["type"] == "note_on" and midi_note["velocity"] > 0):
                self.piano_scroll_notes_on.append(midi_note)
            if(midi_note["type"] == "note_off" or (midi_note["type"] == "note_on" and midi_note["velocity"] == 0)):
                for i, note_on in enumerate(self.piano_scroll_notes_on):
                    if(note_on["note"] == midi_note["note"]):
                        del self.piano_scroll_notes_on[i]

            if(midi_note["type"] == "pitchwheel"):
                self.pitch = midi_note["pitch"]

        roll_value = int(1 * (self.active_state.time_interval / 100)) + 1
        self.pixels = self.roll(self.pixels, roll_value)

        if(len(self.piano_scroll_notes_on) > 0):
            which_color = 0
            which_color = len(self.piano_scroll_notes_on)

            if(which_color >= len(color_scheme)):
                which_color = 0

            r = color_scheme[which_color][0]
            g = color_scheme[which_color][1]
            b = color_scheme[which_color][2]

            value = self.clampToNewIntRange(self.pitch, -8191, 8191, 0, 127)

            for i in range(roll_value):
                putPixel(self.pixels, i, r, g, b, self.piano_scroll_notes_on[len(
                    self.piano_scroll_notes_on) - 1]["velocity"] / 2 + value)
        else:
            for i in range(roll_value):
                putPixel(self.pixels, i, 0, 0, 0, 100)

        return self.pixelReshaper.reshapeFromPixels(self.pixels)
