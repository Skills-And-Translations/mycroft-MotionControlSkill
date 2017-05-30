from adapt.intent import IntentBuilder
from mycroft.skills.core import MycroftSkill
import subprocess
import psutil

class motionWatcherSkill(MycroftSkill):
    def __init__(self):
        super(motionWatcherSkill, self).__init__("motionWatcherSkill")

    def initialize(self):
        startIntent = IntentBuilder("StartIntent").require("startMotionKeyword").build()
        self.register_intent(startIntent, self.handle_start)
        stopIntent = IntentBuilder("StopIntent").require("stopMotionKeyword").build()
        self.register_intent(stopIntent, self.handle_stop)
        statusIntent = IntentBuilder("StatusIntent").require("statusMotionKeyword").build()
        self.register_intent(statusIntent, self.handle_status)

    def stop(self):
        pass

    def handle_start(self, message):
        subprocess.call(['sudo', 'motion'])
        if(subprocess.call(['echo', '$?'])==0):
            self.speak("Motion is started")
        else:
           self.speak("Motion seems to have problems") 
        
    def handle_stop(self, message):
        subprocess.call(['sudo', 'killall','motion'])
        if(subprocess.call(['echo', '$?'])==0):
            self.speak("Motion is stoped")
        else:
           self.speak("Motion could not been stoped") 
        
    def handle_status(self, message):
        notRunning=True
        for pid in psutil.pids():
            p = psutil.Process(pid)
            if p.name() == "motion":
                self.speak("Motion is running")
                notRunning=False
        if notRunning:
            self.speak("Motion is not running")

def create_skill():
    return motionWatcherSkill()
