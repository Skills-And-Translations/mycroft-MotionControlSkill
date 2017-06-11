from adapt.intent import IntentBuilder
from mycroft.skills.core import MycroftSkill
import subprocess
import psutil

class motionWatcherSkill(MycroftSkill):
    def __init__(self):
        super(motionWatcherSkill, self).__init__("motionWatcherSkill")

    def initialize(self):
        self.language = self.config_core.get('lang')
        startIntent = IntentBuilder("StartIntent").require("startMotionKeyword").build()
        self.register_intent(startIntent, self.handle_start)
        stopIntent = IntentBuilder("StopIntent").require("stopMotionKeyword").build()
        self.register_intent(stopIntent, self.handle_stop)
        statusIntent = IntentBuilder("StatusIntent").require("statusMotionKeyword").build()
        self.register_intent(statusIntent, self.handle_status)

    def stop(self):
        pass

    def handle_start(self, message):
        subprocess.call(['motion'])
        if(subprocess.call(['echo', '$?'])==0):
            if self.language=="de":
                self.speak("Ueberwachung ist an.")
            else:
                self.speak("Motion is started. I will have a eye on your stuff.")
        else:
           self.speak("Motion seems to have starting problems") 
        
    def handle_stop(self, message):
        subprocess.call(['killall','motion'])
        if(subprocess.call(['echo', '$?'])==0):
            if self.language=="de":
                self.speak("Motion is stopped")
            else:
                self.speak("Ueberwachung aus")
        else:
            if self.language=="de":
                self.speak("Ueberwachung konnte nicht gestoppt werden")
            else:
                self.speak("Motion could not been stopped") 
        
    def handle_status(self, message):
        notRunning=True
        for pid in psutil.pids():
            p = psutil.Process(pid)
            if p.name() == "motion":
                if notRunning:
                    if self.language=="de":
                        self.speak("Ja, ich beobachte dich")
                    else:
                        self.speak("Yes, i am watching you")
                    notRunning=False
        if notRunning:
            if self.language=="de":
                self.speak("Die ueberwachung ist ausgeschaltet")
            else:
                self.speak("Right now, my eye is closed")

def create_skill():
    return motionWatcherSkill()
