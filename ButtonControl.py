from scapy.all import *
import os
import pygame
import random
import time
import threading

class ButtonControl():

    def __init__(self):
        self.current_dir = os.path.dirname(os.path.abspath(__file__))

        self.song_list = []
        for song in os.listdir(self.current_dir + "/sounds"):
            self.song_list.append(song)

        self.playing = False

        pygame.init()
        pygame.mixer.init()
        pygame.mixer.music.set_volume(1.0)

    def dhcp_discover(self, pkt):
       try:
            if pkt[DHCP].options[0][1] == 1:
                if pkt[Ether].src == 'aa:bb:cc:dd:ee:ff':
                    print "Doorbell"
                    if not self.playing:
                        song = random.choice(self.song_list)
                        pygame.mixer.music.load(self.current_dir + '/sounds/' + song)
                        pygame.mixer.music.play()

                        self.playing = True
                        threading.Timer(10, self.reset_doorbell).start()

        except IndexError:
            print pkt.show()
        
    def reset_doorbell(self):
        if self.playing:
            self.playing = False

if __name__ == "__main__":

    bc = ButtonControl()

    print sniff(prn=bc.dhcp_discover, filter="udp and (port 67 or 68)", store=0)
