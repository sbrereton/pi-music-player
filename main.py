import os
import random
import time
import subprocess

MUSIC_FOLDER = '/mnt/music'  # Change this to the path of your USB music folder
PLAY_TIMES = ['08:55:10', '11:20:10', '14:05:10']  # Change this to a list of times you want the music to start playing
MUSIC_DURATION = 290  # The duration of the music in seconds (5 minutes)
RESET_TIME = '21:00:00'  # The time to reset the list of played songs


def play_random_music(played_music):
    now = time.strftime('%H:%M:%S')

    music_files = []
    for root, dirs, files in os.walk(MUSIC_FOLDER):
        for file in files:
            if file.endswith('.mp3') and os.path.join(root, file) not in played_music:
                music_files.append(os.path.join(root, file))
    if not music_files:
        print('[', now, '] No unplayed music files found!')
        return played_music
    file_path = random.choice(music_files)
    print('[', now, '] Playing', os.path.basename(file_path))  # Display the currently playing song
    music_player = subprocess.Popen(
        ['vlc', '--play-and-exit', file_path])  # Change this to the command to play music using your preferred player
    time.sleep(MUSIC_DURATION)
    try:
        print('[', now, '] Timer reached. Stopping playback')
        music_player.terminate()
        music_player.wait(timeout=1)
    except subprocess.TimeoutExpired:
        print('[', now, '] Could not stop playback, forcibly killing VLC')
        music_player.kill()
    subprocess.Popen(['pkill', 'vlc'])
    played_music.append(file_path)
    if len(played_music) > len(music_files):
        played_music.pop(0)
    return played_music


def reset_played_music():
    return []


def run():
    played_music = []
    print('ESC Music Player v1.0')
    print('Written by: Samuel Brereton')
    print('Sleeping...')
    while True:
        now = time.strftime('%H:%M:%S')
        if now == RESET_TIME:
            print('[', now, '] Resetting playlist...')
            played_music = reset_played_music()
        elif now in PLAY_TIMES:
            print('[', now, '] Beginning playback...')
            played_music = play_random_music(played_music)
        # print('Not playing due to time restriction')
        print('[', now, '] Sleeping. Zzz...')
        time.sleep(1)  # Check the time every minute


while True:
    print('Init!')
    run()
