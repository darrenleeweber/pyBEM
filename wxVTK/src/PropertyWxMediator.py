import wx
import re
from Properties import *
from DynamicDialog import *


class ChoiceWidget:
  def __init__(self, property):
    self.property = property
    self.isChecked = False

  def CreateWidget(self, parentFrame):
    box = wx.BoxSizer(wx.HORIZONTAL)
    checkId = wx.NewId()
    control = wx.CheckBox(parentFrame, checkId, self.property.Name, style=wx.ALIGN_RIGHT)
    self.isChecked = self.property.GetValue()
    control.SetValue(self.isChecked)
    box.Add(control, 0, wx.ALIGN_CENTRE|wx.ALL, 5)
    parentFrame.Bind(wx.EVT_CHECKBOX, self.BoxChecked, id=checkId)
    self.control = control
    control.Pipename = self.property.Name
    return box
  
  def BoxChecked(self, event):
    self.isChecked = event.IsChecked()
    self.SetFromWidget()

  def SetFromWidget(self):
    self.property.SetValue(self.isChecked)


class IntWidget:
  def __init__(self, property):
    self.property = property
    self.numericDigit = re.compile(r"[+-.eE]|[0-9]")
    self.numericString = re.compile(r"[+-]?\d+")

  def CreateWidget(self, parentFrame):
    box = wx.BoxSizer(wx.HORIZONTAL)
    label = wx.StaticText(parentFrame, -1, self.property.Name)
    box.Add(label, 0, wx.ALIGN_CENTRE|wx.ALL, 5)
    control = wx.TextCtrl(parentFrame, -1, str(self.property.GetValue()))
    box.Add(control, 1, wx.ALIGN_CENTRE|wx.ALL, 5)
    #parentFrame.Bind(wx.EVT_TEXT, self.TextEvent, control)
    #control.Bind(wx.EVT_SET_FOCUS, self.TextEvent)
    control.Bind(wx.EVT_KILL_FOCUS, self.ApplyEvent)
    control.Bind(wx.EVT_CHAR, self.CharEvent)
    self.control = control
    #control.Bind(wx.EVT_WINDOW_DESTROY, self.TextEvent)
    return box
      
  def CharEvent(self, event):
    event.Skip()
    #if self.numericDigit.match(chr(event.GetKeyCode())):
    #  event.Skip()
      
  def ApplyEvent(self, event):
    control = event.GetEventObject()
    self.SetFromWidget()

  def SetFromWidget(self):
    val = self.control.GetValue()
    if self.numericString.match(val):
      self.property.SetValue(int(val))
      

class FloatWidget:
  def __init__(self, property):
    self.property = property
    self.numericDigit = re.compile(r"[+-.eE]|[0-9]")
    self.numericString = re.compile(r"[+-]?(\d+[.]?\d*|.\d+)([eE][+-]\d+)?")

  def CreateWidget(self, parentFrame):
    box = wx.BoxSizer(wx.HORIZONTAL)
    label = wx.StaticText(parentFrame, -1, self.property.Name)
    box.Add(label, 0, wx.ALIGN_CENTRE|wx.ALL, 5)
    control = wx.TextCtrl(parentFrame, -1, str(self.property.GetValue()))
    box.Add(control, 1, wx.ALIGN_CENTRE|wx.ALL, 5)
    #parentFrame.Bind(wx.EVT_TEXT, self.TextEvent, control)
    #control.Bind(wx.EVT_SET_FOCUS, self.TextEvent)
    control.Bind(wx.EVT_KILL_FOCUS, self.ApplyEvent)
    control.Bind(wx.EVT_CHAR, self.CharEvent)
    self.control = control
    #control.Bind(wx.EVT_WINDOW_DESTROY, self.TextEvent)
    return box
      
  def CharEvent(self, event):
    event.Skip()
    #if self.numericDigit.match(chr(event.GetKeyCode())):
    #  event.Skip()
      
  def ApplyEvent(self, event):
    control = event.GetEventObject()
    self.SetFromWidget()

  def SetFromWidget(self):
    val = self.control.GetValue()
    if self.numericString.match(val):
      self.property.SetValue(float(val))

      
      

class ColorWidget:
  def __init__(self, property):
    self.property = property
    self.color = None

  def CreateWidget(self, parentFrame):
    box = wx.BoxSizer(wx.HORIZONTAL)
    label = wx.StaticText(parentFrame, -1, self.property.Name)
    box.Add(label, 0, wx.ALIGN_CENTRE|wx.ALL, 5)
    colorId = wx.NewId()
    control = wx.Button(parentFrame, colorId, "set color")
    box.Add(control, 1, wx.ALIGN_CENTRE|wx.ALL, 5)
    parentFrame.Bind(wx.EVT_BUTTON, self.OnButton, control, id=colorId)
    self.control = control
    self.parentFrame = parentFrame
    return box
      
  def OnButton(self, event):
    dlg = wx.ColourDialog(self.parentFrame)
    dlg.GetColourData().SetChooseFull(True)
    c = self.property.GetValue()
    charColor = map(lambda x: int(round(255*x)), c)
    dlg.GetColourData().SetColour(charColor)
    if dlg.ShowModal() == wx.ID_OK:
      data = dlg.GetColourData()
      self.color = data.GetColour().Get()
    dlg.Destroy()
    self.SetFromWidget();
  
  def SetFromWidget(self):
    if self.color:
      c = self.color
      self.property.SetValue((float(c[0])/255,float(c[1])/255, float(c[2])/255))

      
class PropertyWxMediator:
  def __init__(self, properties):
    self.Properties = properties
    self.Widgets = []
    self.PropertyToWidget = { FloatProperty : FloatWidget, IntProperty : IntWidget,
      ColorProperty : ColorWidget, ChoiceProperty : ChoiceWidget
      }
    
  def WidgetForItem(self, parent, addItem):
    property = self.Properties[addItem]
    box = None
    if self.PropertyToWidget.has_key(property.__class__):
      widgetDecorator = self.PropertyToWidget[property.__class__](property)
      box = widgetDecorator.CreateWidget(parent)
      self.Widgets.append(widgetDecorator)
    return box
    
    
  def size(self):
    return len(self.Properties)
    
  def Apply(self, event):
    for widget in self.Widgets:
      widget.SetFromWidget()

# Testing below this line.

class App(wx.App):

  def OnInit(self):
    'Create the main window and insert the custom frame'
    frame = wx.Frame(None, -1, "Test Window", size=wx.Size(400,400))
    frame.Show(True)
    props = [ TestFloat(), TestColor(), TestChoice() ]
    dialog = DynamicDialog(PropertyWxMediator(props), frame, -1, "test dialog")
    dialog.Show()
    return True


if __name__ == "__main__":
  app = App(0)
  app.MainLoop()