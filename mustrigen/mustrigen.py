# -*- coding: utf-8 -*-

"""
Mustrigen: Musical Trivia Generator

This scripts takes files containing list of urls to Youtube musics, and build a Trivia Music Generator from them. The Trivia is streamed using vlc.

https://github.com/Amidattelion/SYMP

Copyright (C)  2013-2014 np1

This program is free software: you can redistribute it and/or modify it under
the terms of the GNU Lesser General Public License as published by the Free
Software Foundation, either version 3 of the License, or (at your option) any
later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY
WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A
PARTICULAR PURPOSE.  See the GNU Lesser General Public License for more details.

You should have received a copy of the GNU Lesser General Public License along
with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

import pip
import sys
import importlib
import keyboard
import time
import os
import random as rd
import matplotlib.pyplot as plt
import inspect
import pafy
import vlc
from tkinter import *

# -----------------------------------------------------------------

class video:
    def __init__(self,url,key_word):
        self.vid      = pafy.new(url)
        self.title    = self.vid.title
        self.url      = url
        self.duration = self.vid.duration
        self.key_word = key_word

    def likely_to_be_in(self,list,e):
        '''compare la similitude du titre avec celui des video de la list, si
        similaire à plus de e pourcent (e compris entre 0 et 1) à un des titres
        des video dans la liste, renvois true'''
        like = 0
        for other_vid in list:

            text1 = self.title
            text1.replace(self.key_word,'')
            text2 = other_vid.title
            text2.replace(self.key_word,'')

            like = likelihood(text1,text2)
            if(like>=e):
                return(True,like)
        return(False,like)

    def check_duration(self,lower_lim,higher_lim):
        '''renvoie True si la video est plus longue ou plus courte que les limites indiquées en seconde'''
        duration_int = self.duration.split(':')
        for k in range(len(duration_int)):
            duration_int[k] = int(duration_int[k])

        duration_sec = duration_int[0]*3600+duration_int[1]*60+duration_int[2]

        return((duration_sec > higher_lim) or (duration_sec < lower_lim))

class FullScreenApp(object):
    def __init__(self, master, **kwargs):
        self.master=master
        pad=3
        self._geom='200x200+0+0'
        master.geometry("{0}x{1}+0+0".format(
            master.winfo_screenwidth()-pad, master.winfo_screenheight()-pad))
        master.bind('<Escape>',self.toggle_geom)
    def toggle_geom(self,event):
        geom=self.master.winfo_geometry()
        print(geom,self._geom)
        self.master.geometry(self._geom)
        self._geom=geom

def play(content,guess_time,play_time):

    global root
    global player

    # start_position = 0.25
    start_position = 0
#     position de début de la vidéo en % (entre 0 et 1), pour éviter les longs débuts silencieux des clips

    name,type,url = content

    if name=='Private video':
        return()

    video = pafy.new(url)
    best = video.getbest()
    playurl = best.url

    Media = player.get_instance().media_new(playurl)
    Media.get_mrl()
    player.set_media(Media)

    player.play()
    player.audio_set_volume(0)

# video_set_marquee_int(nb_correspondant_au_parametre,valeur_du_parametre
# aller sur https://www.videolan.org/developers/vlc/doc/doxygen/html/group__libvlc__media__player.html#ga412d5b45da5bda967f656cb17ecc83fd
# et chercher libvlc_video_marquee_option_t pour la liste des paramètres
    player.video_set_marquee_int(0,1)#     activer le sous-titre 1
    player.video_set_marquee_int(4,4)#     mettre en haut au centre
    player.video_set_marquee_int(6,30)#     taille du sous-titre
    player.video_set_marquee_int(2,16761165)#     couleur en hexa (FFFFFF = blanc, FF0000 = R (RVB)) convertie en décimal)
    player.video_set_marquee_string(1,name)#     mettre le titre en sous titre

    text = Label(root,text='Devinez le titre de cette musique ! Elle vient d\'un(e) {} ...'.format(type),font=("Helvetica", 30),bg='black',fg='white')
    text.pack()
    # text.place(relx=0.1,rely=0.1)
    root.update()
    root.focus_force()

    while(player.get_time()<500):
#   attendre que la musique se lance avant de lancer le chrono
        root.focus_force()

    player.set_position(start_position)
    play_time_compensation = player.get_length() * start_position
#     pour compenser le fait de démarrer plus tard la vidéo

# Monter progressivement le volume
    for vol in range(0,205,5):
        player.audio_set_volume(vol)
        time.sleep(0.2)

    t0 = time.perf_counter()

#   fenêtre pour guess
    timer = StringVar()
    label_timer = Label(root,textvariable=timer,font=("Helvetica", 30),bg='black',fg='gold')
    label_timer.pack()
    timer.set('Il reste {} sec'.format(guess_time))
    # label_timer.place(relx=0.5,rely=0.2)
    root.update()
    root.focus_force()


    time_over = False
    pause_delta = 0
    while True:
        chrono = time.perf_counter()-t0-pause_delta
        delta_t = int(guess_time-chrono)
        root.update()
        root.focus_force()
        time.sleep(0.05)

        if(chrono < guess_time):
            timer.set('Il reste {} sec'.format(delta_t))
            root.update()


        if not(time_over):
            if(chrono > guess_time):
                # player.toggle_fullscreen()
                # player.toggle_fullscreen()
                # player.toggle_fullscreen()
                timer.set('Il s\'agissait de :\n {}'.format(name))
                root.update()
                root.focus_force()
                # root.wm_attributes('-alpha',0)

                # disparition progressive de la fenêtre:
                for k in range(10,-1,-1):
                    root.wm_attributes('-alpha',k/10)
                    time.sleep(0.05)

                time_over = True

        if(keyboard.is_pressed('ctrl+p')):
            t1 = chrono
            player.pause()
            keyboard.wait('ctrl+r')
            player.play()
            pause_delta += (chrono-t1)


        if(keyboard.is_pressed('ctrl+up')):
            player.audio_set_volume(player.audio_get_volume()+10)

        if(keyboard.is_pressed('ctrl+down')):
            player.audio_set_volume(player.audio_get_volume()-10)

        if(keyboard.is_pressed('ctrl+space')):
            player.stop()
            break

        # if((((player.get_time()-play_time_compensation)//1000)>play_time) or ((player.get_time()) >= (player.get_length()))):
        if((chrono > play_time) or (player.get_time() >= player.get_length())):
            # diminuer progressivement le volume
            for vol in range(200,-5,-5):
                player.audio_set_volume(vol)
                time.sleep(0.2)

            # Affichage progressif de la fenêtre:
            for k in range(0,11,1):
                root.wm_attributes('-alpha',k/10)
                root.focus_force()
                time.sleep(0.05)

            player.stop()
            break

        if(keyboard.is_pressed('ctrl+q')):
            player.stop()
            exit()
            break



    root.focus_force()
    text.pack_forget()
    timer.set('')
    label_timer.pack_forget()
    root.update()

def play_trivia(file,guess_time,play_time,n=1,all=True,history_file='none'):
    '''lance le blind test en sélectionnant n lignes aléatoire de file (1 ligne = music,type,url)
    time est la durée en seconde pour deviner'''

    global player
    global root

    content = {}
    deja_vu = {}
    nb_music = 0

    default_guess_time = guess_time

    #Création du player de vlc
    Instance = vlc.Instance("prefer-insecure") #     prefer-insecure pour éviter les erreurs réseau en utilisant http au lieu de https
    player = Instance.media_player_new("--sub-filter=marq") #     --sub-filter=marq pour activer les sous-titres
    player.toggle_fullscreen()

    #Création de la fenêtre tkinter
    root = Tk()
    root.configure(background='black')
    app=FullScreenApp(root)

    if(history_file!='none'):
        with open(history_file,'r',encoding = 'utf-8') as f:
            for l in f.readlines():
                try:

                    music,type,url = l.split(';')
                    url = url.replace('\n','').replace(' ','')
                    if not type in content.keys():
                        content[type] = {}
                        deja_vu[type] = []
                    deja_vu[type].append(music)
                    nb_music += 1
                except:
                    continue

    with open(file,'r',encoding='utf-8') as f:
        for l in f.readlines():
            # print(nb_music)
            try:

                music,type,url = l.split(';')
                url = url.replace('\n','').replace(' ','')
                if not type in content.keys():
                    content[type] = {}
                    deja_vu[type] = []
                content[type][music] = url
                nb_music += 1
            except:
                continue

    type_counter = 0
    nb_types = len(content.keys())
    if(all): n = nb_music

    for k in range(n+1):
        current_guess_time = default_guess_time
        current_play_time = play_time

        chosed_type = list(content.keys())[type_counter % nb_types]
        if len(deja_vu[chosed_type])>=len(content[chosed_type].keys()):
            type_counter += 1
            continue

        while True:
            i = rd.randint(0,len(content[chosed_type].keys())-1)
            chosed_music = list(content[chosed_type].keys())[i]
            music_info = [chosed_music,chosed_type,content[chosed_type][chosed_music]]
            if chosed_music in deja_vu[chosed_type]:
                continue
            deja_vu[chosed_type].append(chosed_music)
            type_counter += 1
            break


        if(chosed_type in ['Pub']):
            current_guess_time = default_guess_time//2
            current_play_time = play_time//2

        if(chosed_type in ['Musique']):
            current_guess_time = default_guess_time * 2
            current_play_time = play_time * 2


        try:
            play(music_info,current_guess_time,current_play_time)
        except:
            continue
        with open(file.replace('.txt','')+'_historique.txt','a',encoding='utf-8') as f:
            f.write('{};{};{}\n'.format(*music_info))
    finis = Label(root,text='Merci d\'avoir joué ! \n Ajoutez de nouvelles musiques dans la liste pour une prochaine session !',font=("Helvetica", 30),bg='black',fg='white')
    finis.pack()
    root.destroy()
    print('Finis !')
    time.sleep(5)
    exit()
