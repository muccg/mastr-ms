import wx
import string

class IconBar:

    numIcons = 5
    ##
    # \brief the constructor default left: red, default right: green
    #
    def __init__(self,l_off=[128,0,0],l_on=[255,0,0],r_off=[0,128,0],r_on=[0,255,0]):
        self.s_line = "\xff\xff\xff"+"\0"*45
        self.s_border = "\xff\xff\xff\0\0\0"
        self.s_point = "\0"*3
        self.sl_off = string.join(map(chr,l_off),'')*6
        self.sl_on = string.join(map(chr,l_on),'')*6
        self.sr_off = string.join(map(chr,r_off),'')*6
        self.sr_on = string.join(map(chr,r_on),'')*6

    ##
    # \brief gets a new icon with 0 <= l,r <= 5
    #
    def Get(self,l,r):
        s=""+self.s_line
        for i in range(5):
            if i<(self.numIcons-l):
                sl = self.sl_off
            else:
                sl = self.sl_on

            if i<(self.numIcons-r):
                sr = self.sr_off
            else:
                sr = self.sr_on

            s+=self.s_border+sl+self.s_point+sr+self.s_point
            s+=self.s_border+sl+self.s_point+sr+self.s_point
            s+=self.s_line

        image = wx.EmptyImage(16,16)
        image.SetData(s)

        bmp = image.ConvertToBitmap()
        bmp.SetMask(wx.Mask(bmp, wx.WHITE)) #sets the transparency colour to white

        icon = wx.EmptyIcon()
        icon.CopyFromBitmap(bmp)



        return icon


