from Properties import *

class PropertySet:
  def __init__(self):
    self.Properties = []
    self.PropertyDict = {}
  
  def __len__(self):
    return self.Properties.__len__()
  def __getitem__(self, key):
    return self.Properties.__getitem__(key)
  def __setitem__(self, key, value):
    self.Properties.__setitem__(key, value)
  def __delitem__(self, key):
    self.Properties.__delitem__(key)
  def __iter__(self):
    return self.Properties.__iter__()
  def __contains__(self, item):
    return self.Properties.__contains__(item)

  def append(self, item):
    if not hasattr(item,"Name"):
      raise RuntimeError, "Properties must have names."
    if self.PropertyDict.has_key(item.Name):
      raise RuntimeError, "dictionary already has property name "+item.Name
    self.PropertyDict[item.Name] = item
    self.Properties.append(item)
  
  def WriteToDict(self):
    vals = {}
    for readProp in self.Properties:
      vals[readProp.Name] = readProp.GetValue()
    return vals
    
  def ReadFromDict(self, initializeDict):
    for key in initializeDict.keys():
      if self.PropertyDict.has_key(key):
        self.PropertyDict[key].SetValue(initializeDict[key])

        
def TestPropertySet():
  ps = PropertySet()
  ps.append(TestFloat())
  ps.append(TestColor())
  ps.append(TestChoice())
  if len(ps) is not 3:
    print "no go len"
  for prop in ps:
    name = prop.Name
  dict = ps.WriteToDict()
  if len(dict.keys()) is not 3:
    print "no go keys"
  print dict
  ps.ReadFromDict(dict)

if __name__ == "__main__":
  TestPropertySet()
