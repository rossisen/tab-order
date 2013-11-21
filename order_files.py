import sublime
import sublime_plugin

class OrderFilesInGroupCommand(sublime_plugin.TextCommand):
  def run(self, edit, **kwargs):
    currentGroup = kwargs.get('group')
    if (currentGroup == None):
      currentGroup = 0
    self.sortGroup(currentGroup, -1)
  def sortGroup(self, groupNumber, tabNumber):
      files = []  # keep track of filenames
      lookupArray = []
      if (tabNumber == None):
        tabNumber = -1
      #for each view(tab) in the active window
      for v in sublime.active_window().views_in_group(groupNumber):
        if (sublime.active_window().get_view_index(v)[1] > tabNumber):
          #define file size and file name
          fileName = v.file_name()
          if (fileName==None):
            fileName = "untitled"
            baseFile = "untitled"
          else:
            fwdSlashName = fileName.replace('\\', '/')
            baseFile = fwdSlashName.split('/')[-1]

          files.append((baseFile+ "_v" + str.format("{0}",v.id())).lower())
          lookupArray.append((v.id(), v))
        #fileViews.append([baseFile+ "_v" + str.format("{0}",v.id())] )
      # end the for loop
      lookupDictionary = dict(lookupArray)
      files.sort()  # sort the files

      newIndex = tabNumber + 1
      for f in files:
        viewString = f.split('_v')[-1]
        sublime.active_window().set_view_index(lookupDictionary[int(viewString)], groupNumber, newIndex)
        newIndex+=1

class OrderFilesCommand(OrderFilesInGroupCommand):
  def run(self, edit):
    for g in range(sublime.active_window().num_groups()):
     self.sortGroup(g, -1)

class OrderFilesToRightCommand(OrderFilesInGroupCommand):
  def run(self, edit, **kwargs):
    currentGroup = kwargs.get('group')
    if (currentGroup == None):
      currentGroup = 0
    self.sortGroup(currentGroup, kwargs.get('index'))