import cv2
from pyzbar.pyzbar import decode


class Decode:
    def __init__(self):
        pass

    def decode(self, im):
        dec = self.decode_im(self.decode_blur(im))
        if dec:
            return dec

        im = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
        closed = cv2.morphologyEx(self.decode_blur(im), cv2.MORPH_CLOSE, kernel)

        dec = self.decode_im(closed)
        if dec:
            return dec

        # cv2.imwrite(os.path.join(path, 'qr_' + name), closed)

        # im = decode_resize(im)

        dec = self.decode_im(im)
        if dec:
            return dec

        # im = cv2.GaussianBlur(im,(3,3),0)
        # im = cv2.medianBlur(im,3)

        dec = self.decode_im(self.decode_equalize(im))
        if dec:
            return dec

        # im = cv2.blur(im,(1,1))

        dec = self.decode_im(self.decode_threshold(im))
        if dec:
            return dec

    @staticmethod
    def decode_equalize(im):
        # im = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)

        return cv2.equalizeHist(im)

    @staticmethod
    def decode_resize(image):
        scale_percent = 60  # percent of original size
        width = int(image.shape[1] * scale_percent / 100)
        height = int(image.shape[0] * scale_percent / 100)
        dim = (width, height)

        # final_wide = 1024
        # r = float(final_wide) / int(image.shape[1])
        # dim = (final_wide, int(int(image.shape[0]) * r))

        return cv2.resize(image, dim, interpolation = cv2.INTER_AREA)

    @staticmethod
    def decode_threshold(image):
        (thresh, im) = cv2.threshold(image, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
        thresh = 127

        return cv2.threshold(im, thresh, 255, cv2.THRESH_BINARY)[1]

    @staticmethod
    def decode_blur(image):
        return cv2.GaussianBlur(image, (3, 3), 0)

    @staticmethod
    def decode_dilate(image):
        return cv2.dilate(image, (3, 3))

    @staticmethod
    def decode_erode(image):
        return cv2.erode(image, (3, 3))

    @staticmethod
    def decode_sobel(image):
        # compute the Scharr gradient magnitude representation of the images
        # in both the x and y direction
        gradX = cv2.Sobel(image, ddepth = cv2.CV_32F, dx = 1, dy = 0, ksize = -1)
        gradY = cv2.Sobel(image, ddepth = cv2.CV_32F, dx = 0, dy = 1, ksize = -1)

        # subtract the y-gradient from the x-gradient
        gradient = cv2.subtract(gradX, gradY)
        gradient = cv2.convertScaleAbs(gradient)

        return gradient

    @staticmethod
    def decode_im(im):
        decodedObjects = decode(im)
        for obj in decodedObjects:
            return obj.data.decode('utf-8')
        return False
