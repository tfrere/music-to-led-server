import numpy as np


class Scroll():

    def visualizeScroll(self):
        """Effect that originates in the center and scrolls outwards"""
        self.audio_data = self.audio_data**2.0
        self.gain.update(self.audio_data)
        self.audio_data /= self.gain.value
        self.audio_data *= 50.0

        active_color_scheme = self.config._formatted_color_schemes[
            self.active_state.active_color_scheme_index]
        length_of_color_scheme = len(active_color_scheme)
        chunk_size = len(self.audio_data) // length_of_color_scheme
        r = 0
        g = 0
        b = 0

        for i in range(length_of_color_scheme):
            x = chunk_size * i
            y = chunk_size * (i + 1)
            value = int(np.mean(self.audio_data[x:y]))
            r += value * active_color_scheme[i][0]
            g += value * active_color_scheme[i][1]
            b += value * active_color_scheme[i][2]

        r = r / (length_of_color_scheme + 2)
        g = g / (length_of_color_scheme + 2)
        b = b / (length_of_color_scheme + 2)

        offset = 0
        roll_value = int(1 * (self.active_state.time_interval / 100)) + 1

        ## r = int(np.max(self.audio_data[:len(self.audio_data) // 3]))
        ## g = int(np.max(self.audio_data[len(self.audio_data) // 3: 2 * len(self.audio_data) // 3]))
        ## b = int(np.max(self.audio_data[2 * len(self.audio_data) // 3:]))

        # simple shape 

        self.pixels = self.roll(self.pixels, roll_value)
        # self.pixels = np.roll(self.pixels, roll_value, axis=1)

        # this is an attempt to reverse scroll effect properly
        # if(self.active_state.is_reverse):
        #     print("scroll is reverse triggered")
        #     offset = len(self.pixels[0]) - roll_value

        for i in range(roll_value):
            self.pixels[0, offset + i] = r
            self.pixels[1, offset + i] = g
            self.pixels[2, offset + i] = b

        self.pixels = np.clip(self.pixels, 0, 255)

        return self.pixelReshaper.reshapeFromPixels(self.pixels)

        # multi shape handling

        # for x, strip in enumerate(self.pixelReshaper._strips):
        #     max_length = len(strip[0])

        #     if(self.active_state.is_reverse):
        #         offset = len(strip[0]) - roll_value

        #     for i in range(roll_value):
        #         strip[0, offset + i] = r
        #         strip[1, offset + i] = g
        #         strip[2, offset + i] = b
            
        #     self.pixelReshaper._strips[x] = self.roll( 
        #         self.pixelReshaper._strips[x], roll_value)

        # return self.pixelReshaper.reshapeFromStrips(self.pixelReshaper._strips)
