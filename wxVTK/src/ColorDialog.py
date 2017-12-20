import wx

class ColorDialog(wx.Dialog):

  def __init__(self, mediator, parent, ID, title, size=wx.DefaultSize, pos=wx.DefaultPosition,
               style=wx.DEFAULT_DIALOG_STYLE):
    wx.Dialog.__init__(self,parent,ID, title, [200,200])
    
    self.mediator = mediator
    
    sizer = wx.BoxSizer(wx.VERTICAL)

    for addItem in range(mediator.size()):
      box = mediator.WidgetForItem(self, addItem)
      if box:
        sizer.Add(box, 0, wx.GROW|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
  
    btnSizer = wx.StdDialogButtonSizer()
    okBtn = wx.Button(self, wx.ID_OK)
    btnSizer.AddButton(okBtn)
    cancelBtn = wx.Button(self, wx.ID_CANCEL)
    btnSizer.AddButton(cancelBtn)
    applyBtn = wx.Button(self, wx.ID_APPLY)
    applyBtn.SetDefault()
    btnSizer.AddButton(applyBtn)
    btnSizer.Realize()
    sizer.Add(btnSizer, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
    
    #self.Bind(wx.EVT_BUTTON, self.OnApply, okBtn)
    self.Bind(wx.EVT_BUTTON, self.OnApply, applyBtn)
    
    self.SetSizer(sizer)
    sizer.Fit(self)
 
  def OnApply(self, event,):
    self.mediator.Apply(event)
