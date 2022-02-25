import sys
import speech_recognition as sr #https://www.lfd.uci.edu/~gohlke/pythonlibs/
from bs4 import BeautifulSoup
from thefuzz import fuzz
import re
import textwrap
from satzmetzger.satzmetzger import Satzmetzger
metzgerle = Satzmetzger()
from einfuehrung import *
from time import sleep

drucker = Farbprinter()


def sleep_with_statusbar(maxrange):
    """usage: sleep_with_statusbar(10)
    output: [==========] 10 of 10"""
    for i in range(maxrange+1):
        sys.stdout.write('\r')
        sys.stdout.write(f"[{'=' * i}] {i} / {maxrange}")
        sys.stdout.flush()
        sleep(1)
    sys.stdout.write('\r')
    sys.stdout.write(f"                                                                                                                                ")
    sys.stdout.flush()


def txtdateien_lesen(text):
    try:
        dateiohnehtml = (
            b"""<!DOCTYPE html><html><body><p>""" + text + b"""</p></body></html>"""
        )
        soup = BeautifulSoup(dateiohnehtml, "html.parser")
        soup = soup.text
        return soup.strip()
    except Exception as Fehler:
        print(Fehler)

def get_file_path(datei):
    pfad = sys.path
    pfad = [x.replace('/', '\\') + '\\' + datei for x in pfad]
    exists = []
    for p in pfad:
        if os.path.exists(p):
            exists.append(p)
    return list(dict.fromkeys(exists))

def get_text():
    p = subprocess.run(get_file_path(r"Everything2TXT.exe")[0], capture_output=True)
    ganzertext = txtdateien_lesen(p.stdout)
    return ganzertext

maximize_console()
einfuehrung(name='Babbler')

textzumvorlesen = get_text()
gesplittetertext = metzgerle.zerhack_den_text(textzumvorlesen)

for satz in gesplittetertext:
    sleep_with_statusbar(5)

    wrapper = textwrap.TextWrapper(width=50)
    word_list = wrapper.wrap(text=satz)

    # Print each line.
    print(drucker.f.black.brightwhite.normal(f'\n\n                  \n'), end = '')
    for element in word_list:
        print(drucker.f.black.brightwhite.normal(f'\n{element}\n'), end='')


    r = sr.Recognizer()
    with sr.Microphone() as source:
        print(drucker.f.black.brightyellow.normal('\n\nBitte lies den Satz vor!\n\n'))
        print(drucker.f.black.brightred.normal('\nAchte bitte darauf, dass du in einer ruhigen Umgebung bist und ein gutes Mikrofon verwendest,\nsonst weiß das Programm nicht, wann du zu Ende gesprochen hast!\n'))

        audio = r.listen(source)

    try:
        erkannter_text= r.recognize_google(audio, language="de-DE")
        # ohne_korrektur = fuzz.ratio(erkannter_text, textzumvorlesen)
        textzumvorlesen_klein = re.sub(r"['\W\d_']+", '', satz)
        erkannter_text_klein = erkannter_text.lower()
        erkannter_text_klein = re.sub(r"['\W\d_']+", '', erkannter_text_klein)
        # print(drucker.f.red.magenta.normal(f'{textzumvorlesen_klein}'))
        # print(drucker.f.red.cyan.normal(f'{erkannter_text_klein}'))
        ohne_korrektur_2 = fuzz.ratio(textzumvorlesen_klein, erkannter_text_klein)
        colorfunctionslogo = [drucker.f.black.red.normal, drucker.f.black.brightyellow.normal]
        drucker.p_ascii_front_on_flag_with_border(
            text=f'{ohne_korrektur_2} von 100',
            colorfunctions=colorfunctionslogo,
            bordercolorfunction=drucker.f.brightgreen.black.italic,
            font="slant",
            width=1000,
            offset_from_left_side=5,
            offset_from_text=15,
        )
    except sr.UnknownValueError:
        print("\nGoogle Speech Recognition could not understand audio\n")
    except sr.RequestError as e:
        print(drucker.f.brightwhite.brightred.normal("\nCould not request results from Google Speech Recognition service; {0}\n".format(e)))
    except Exception as Fehler:
        print(drucker.f.brightwhite.brightred.normal(f'\n{Fehler}\n'))
    print(drucker.f.green.brightyellow.normal('\nGleich geht es weiter! Atme tief durch und konzentriere dich\n'))
    print(10 *'\n')

input(drucker.f.black.brightyellow.italic('Fertig! Beliebige Taste drücken, um das Programm zu beenden!'))