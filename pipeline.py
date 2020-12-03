import habits
import analytics
import user

# Class for wrapping all functionality for the command line interface


class Pipeline(object):
    def __init__(self):
        self.manage = habits.Habit()
        self.analyse = analytics.Analytics()
