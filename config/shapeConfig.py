class ShapeConfig():

    def __init__(
        self,
        shape=[74, 74, 125, 125],
        verbose=False
    ):

        self.shape = shape
        self._number_of_substrip = len(self.shape)
        self._number_of_pixels = 0
        for pixel_number in self.shape:
            self._number_of_pixels += pixel_number

        self._offsets = []
        for i, bock_size in enumerate(self.shape):
            if(i - 1 >= 0):
                self._offsets.append(bock_size + self._offsets[i - 1])
            else:
                self._offsets.append(bock_size)

        if(verbose):
            self.print()

    def print(self):
        print("--")
        print("----------------")
        print("Shape Config : ")
        print("----------------")
        print("shape -> ", self.shape)
        print("number_of_substrip -> ", self._number_of_substrip)
        print("number_of_pixels -> ", self._number_of_pixels)
        print("shape chunks offset -> ", self._offsets)
        print("----------------")
        print("--")
