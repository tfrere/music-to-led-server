import numpy as np


def hsv_to_rgb(h, s, v):
    if s == 0.0:
        v *= 255
        return (v, v, v)
    i = int(h*6.)  # XXX assume int() truncates!
    f = (h*6.)-i
    p, q, t = int(255*(v*(1.-s))), int(255*(v*(1.-s*f))
                                       ), int(255*(v*(1.-s*(1.-f))))
    v *= 255
    i %= 6
    if i == 0:
        return (v, t, p)
    if i == 1:
        return (q, v, p)
    if i == 2:
        return (p, v, t)
    if i == 3:
        return (p, q, v)
    if i == 4:
        return (t, p, v)
    if i == 5:
        return (v, p, q)


class FullHue():

    def initFullHue(self):
        self.old_full_intensity = 0

    def visualizeFullHue(self):
        newHue = self.clampToNewRange(
            self.active_state.time_interval, 0, 500, 0, 1)
        color = hsv_to_rgb(newHue, 1., 1.)
        self.pixels[0] = color[0]
        self.pixels[1] = color[1]
        self.pixels[2] = color[2]

        return self.pixelReshaper.reshapeFromPixels(self.pixels)
