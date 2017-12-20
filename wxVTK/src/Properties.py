

class IntProperty:
  def __init__(self, name, setCallBack, getCallBack):
    self.Name = name
    self._setCallBack = setCallBack
    self._getCallBack = getCallBack
  
  def SetValue(self, val):
    self._setCallBack(val)

  def GetValue(self):
    return self._getCallBack()

def SetInt(f): print f
def GetInt(): return 4

def TestInt():
  f = IntProperty("testint", SetInt, GetInt)
  return f
  
class FloatProperty:
  def __init__(self, name, setCallBack, getCallBack):
    self.Name = name
    self._setCallBack = setCallBack
    self._getCallBack = getCallBack
  
  def SetValue(self, val):
    self._setCallBack(val)

  def GetValue(self):
    return self._getCallBack()

def SetFloat(f): print f
def GetFloat(): return 3.14

def TestFloat():
  f = FloatProperty("testfloat", SetFloat, GetFloat)
  return f


class ColorProperty:
  def __init__(self, name, setCallBack, getCallBack):
    self.Name = name
    self._setCallBack = setCallBack
    self._getCallBack = getCallBack
  
  def SetValue(self, val):
    apply(self._setCallBack, val)

  def GetValue(self):
    return self._getCallBack()

    
def SetColor(a,b,c): print a,b,c
def GetColor(): return [.5, .5, 1.0]
def TestColor():
  f = ColorProperty("testcolor", SetColor, GetColor)
  return f


class ChoiceProperty:
  def __init__(self, name, setCallBack, getCallBack):
    self.Name = name
    self._setCallBack = setCallBack
    self._getCallBack = getCallBack
  
  def SetValue(self, val):
    if val:
      self._setCallBack(1)
    else:
      self._setCallBack(0)

  def GetValue(self):
    return (self._getCallBack() is not 0)

def SetChoice(a): print a
def GetChoice(): return True
def TestChoice():
  f = ChoiceProperty("testchoice", SetChoice, GetChoice)
  return f
