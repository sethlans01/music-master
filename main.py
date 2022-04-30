import glob
import os
import youtube_dl
from pytube import Playlist
from tkinter import *
from tkinter import messagebox


# GLOBAL VARIABLE THAT COUNTS DOWNLOAD ERRORS, WILL BE USEFUL LATER ;)
errorz = 0

# GET CURRENT DIRECTORY'S PATH
dir_path = os.getcwd()

# CREATE TEMPORARY-FILES' DIRECTORY'S PATH
temp_path = dir_path + "\\temp"

# OPEN THE PATHS FILE AND READ THE PATH
file = open("paths.txt", 'r')
file.seek(0, 0)
final_path = file.readline()
file.close()

# OPEN THE FILE FOR THE ERRORS
try:
    os.remove("errors.txt")
except:
    errorz = 0
file = open("errors.txt", 'w')

# MAKE DIRECTORY TO CONTAIN RAW DOWNLOADED FILES
try:
    os.mkdir(temp_path)
except:
    #RANDOM COMMAND, OTHERWISE PYTHON IS NOT HAPPY
    errorz = 0

# ENTER IN THE DIRECTORY AND COUNT THE FILES IN IT
os.chdir(temp_path)
file_inside = int(len(glob.glob('*')))
# IF THERE ARE FILES DELETE THEM
if file_inside != 0:
    file_list = os.listdir('.')
    for counter in range(file_inside):
        os.remove(file_list[counter])


def start():
    # GET LINK FROM THE USER
    link = entry1.get()
    # CHECK IF IT'S A SINGLE SONG OR A PLAYLIST AND DOWNLOAD IT
    link_lenght = len(link)
    if link[24] == 'p':
        download_playlist(link)
    else:
        if link[link_lenght-2] == '=':
            download_playlist(link)
        else:
            download_song(link)


def download_song(link):
    # DEFINE THE OPTIONS FOR THE DONWLOAD
    ydl_opts = {
        'format': 'bestaudio/best',
    }
    # TRY TO DOWNLOAD THE SONG
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        try:
            ydl.download([link])
            convert_all()
        except:
            file.close()
            MsgBox = messagebox.showinfo("Warning", "Download not completed...\nThe song requested could not be downloaded...")
            if MsgBox == 'ok':
                finestra1.destroy()




def download_playlist(link):
    # COUNT THE SONGS INSIDE THE PLAYLIST
    playlist = Playlist(link)
    playlist_lenght = playlist.length
    # CREATE AN ARRAY WITH THE LINKS OF EACH SONG
    playlist_links = []
    for url in playlist.video_urls:
        playlist_links.append(url)
    # DEFINE THE OPTIONS FOR THE DOWNLOAD
    ydl_opts = {
        'format': 'bestaudio/best',
    }
    # TRY TO DOWNLOAD THE SONG
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        for url in playlist_links:
            try:
                ydl.download([url])
            except:
                errorz = int(errorz) + 1
                stringz = url + "\n"
                file.write(stringz)
    convert_all()


def convert_all():
    # ENTER IN THE OUTPUT FOLDER
    os.chdir(final_path)
    # CHECK IF THERE ARE FILES AND, IF THERE ARE, DELETE THEM
    file_to_delete_number = int(len(glob.glob('*')))
    file_to_delete = os.listdir('.')
    for counter in range(file_to_delete_number):
        os.remove(file_to_delete[counter])
    # CONVERT M4A FILES INTO MP3 FILES
    m4a_command = "audioconvert convert " + temp_path + " " + final_path + " --output-format .mp3"
    os.system(m4a_command)
    # CONVERT WEBM FILES INTO MP3 FILES
    os.chdir(temp_path)
    temp_files_number = int(len(glob.glob('*')))
    temp_files = os.listdir('.')
    for counter in range(temp_files_number):
        song_name = temp_files[counter]
        song_name_lenght = int(len(song_name))
        cut_song_name = song_name[0:song_name_lenght - 4]
        destination_path = "\"" + final_path + "\\" + cut_song_name + "mp3\""
        webm_command = "ffmpeg -i \"" + temp_path + "\\" + song_name + "\" " + destination_path
        print(webm_command)
        os.system(webm_command)
    kill()


def kill():
    file.close()
    if errorz == 0:
        MsgBox = messagebox.showinfo("Warning", "Download Completed!\nTo close the program press the \'OK\' button...")
        if MsgBox == 'ok':
            finestra1.destroy()
    else:
        MsgBox = messagebox.showinfo("Warning", "Download partially completed...\nSome songs could not be downloaded\nThe file error.txt contains the links of the songs not downloaded")
        if MsgBox == 'ok':
            finestra1.destroy()



# GUI COMPONENTS DECLARATION
finestra1 = Tk()
finestra1.title("Music Master")

frame1 = Frame(master=finestra1)
frame2 = Frame(master=finestra1)
frame3 = Frame(master=finestra1)

label1 = Label(master=frame1, text="Welcome to Music Master!", fg="#154360")
label1.configure(font=("Times New Roman", 20))

label2 = Label(master=frame2, text="Please insert a valid link...", fg="#424949")
label2.configure(font=("Times New Roman", 12, "italic"))

button1 = Button(master=frame3, text="Start", command=start)

entry1 = Entry(master=frame3)

# GUI COMPONENTS DISPLAYING
label1.pack()
label2.grid(row=0, column=0)

entry1.grid(row=0, column=0, padx=0)

button1.grid(row=0, column=1, padx=10)

frame1.pack()
frame2.pack(pady=10, ipadx=100)
frame3.pack(padx=10, ipadx=100)

finestra1.mainloop()
