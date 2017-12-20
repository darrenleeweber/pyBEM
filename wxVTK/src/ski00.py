# python planes8.py -c camera.pickle
# Hit "b" to save a camera position into a file called camera.pickle
# Hit "t" to save an image.

import vtk
import cmath
import pickle
import os
import math
import sys
import getopt

from DisplayWindow import DisplayWindow
from Backdrop import Backdrop
from ParametricSurface import ParametricSurface
from LineTube import LineTube

def ParametricUp(t):
  return [t, cmath.asinh(t).real, 2]

def ParametricShift(t):
  return [t, cmath.asinh(t).real, -2]

def ParametricDown(t):
  return [t, cmath.asinh(-t).real, -2]

    
# HERE is MAIN()		
if __name__ == "__main__":
  domain = [ -5, 5, .1 ]
  backdrop = Backdrop(((-6, -4, -2), (6, 4, 2)))
  twist = ParametricSurface(domain, ParametricUp, ParametricShift)
  upTube = LineTube(ParametricUp, domain)
  downTube = LineTube(ParametricShift, domain)
  window = DisplayWindow()
  window.AddActor(twist.GetActor())
  window.AddActor(upTube.GetActor())
  window.AddActor(downTube.GetActor())
  backActors = backdrop.GetActor()
  #window.AddActor(backActors[0])
  #window.AddActor(backActors[1])
  
  window.Start()

	