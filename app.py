from tkinter import *
from tkinter import colorchooser, messagebox
from random import randint


class App:

  def __init__(self,parent):
    # Základní nastavení
    self.color_fg = 'black'
    self.color_bg = 'white'
    self.action = ""
    self.slovo = ""
    self.text = 'black'
    self.x = 0
    self.y = 0
    self.parent = parent
    self.files()
    self.gui()


  def gui(self):
    # Nastavení obrazovky
    screen_width = self.parent.winfo_screenwidth()
    screen_height = self.parent.winfo_screenheight()
    width = screen_width / 3*2
    height = screen_width / 5*2
    x = (screen_width/2) - (width/2)
    y = (screen_height/2) - (height/2)
    root.geometry('%dx%d+%d+%d' % (width, height, x, y))

    self.container = Frame(self.parent, width=screen_width / 2, bg="gray", highlightthickness=3, highlightbackground="gray")

    # Menu nahoře
    menu = Menu(self.parent)
    self.parent.config(menu=menu)

    basicmenu = Menu(menu)
    menu.add_cascade(label='Soubor',menu=basicmenu)
    basicmenu.add_command(label='Nová hra',command=self.new_game)
    basicmenu.add_command(label='O programu',command=self.about)
    basicmenu.add_command(label='Konec',command=self.parent.destroy)

    canvasmenu = Menu(menu)
    menu.add_cascade(label='Nastavení',menu=canvasmenu)
    canvasmenu.add_command(label='Barva pozadí',command=self.change_bg)
    canvasmenu.add_command(label='Barva textu',command=self.change_fg)

    giveupmenu = Menu(menu)
    menu.add_command(label='Vzdát se',command=self.give_up)

    self.container.pack(fill=BOTH)

    self.canvas = Canvas(self.parent, width=screen_width / 3 * 2, height=screen_height / 5 * 2, bg=self.color_bg, highlightthickness=3, highlightbackground="gray")

    self.cvs()


  def files(self):
    
    # Načtení slov do proměnné
    words = []
    with open('words.txt', 'r') as file:
      line = file.readline().strip()
      words.append(line)
      while line:
        line = file.readline().strip()
        words.append(line)
    
    # Vygenerování náhodného indexu a získání slova z tohoto indexu
    rand_idx = randint(0, len(words))
    self.slovo = words[rand_idx]
    print("Slovo: "+self.slovo)
    

  # Canvas:
  
  def cvs(self):
    # Text
    self.canvas.create_text(500,50,text="Vítejte !",font=("Purisa",18),fill=self.text)
  
    # self.canvas.create_text(500,100,text=self.slovo)
    self.canvas.create_text(50,125,text=" _ "*len(self.slovo),anchor="w",font=("Purisa",14),fill=self.text)
    # Put all input to upper() - list of words is uppercase
    self.canvas.create_text(50,175,text="Zadejte písmeno: ",anchor="w",font=("Purisa",14),fill=self.text)
    self.canvas.create_window(225,175,anchor="w",window=Entry(self.canvas),width="20")

    self.canvas.pack(fill=BOTH,expand=True)


  # Funkce:

  # Redraw canvas - DONE
  def redraw_canvas(self):     
    self.canvas.delete("all")
    self.cvs()
    print("Redrawing...")
  
  # Nová hra - DONE
  def new_game(self):
    self.redraw_canvas()
    print("Nová hra")

  # O programu
  def about(self):
    print("O programu...")

  # Změna pozadí - DONE
  def change_bg(self):
    self.color_bg = colorchooser.askcolor(color=self.color_bg)[1]
    self.canvas['bg'] = self.color_bg
    self.redraw_canvas()
    print("Změna barvy pozadí")

  # Změna barvy textu - DONE
  def change_fg(self):
    print("Změna barvy textu")
    self.text = colorchooser.askcolor(initialcolor=self.text)[1]
    self.redraw_canvas()

  # Vzdát se pokud není známé slovo - DONE
  def give_up(self):
    print("Hráč se vzdává")
    gu = messagebox.askyesno('Giving up ?', 'Are you sure about this ?', icon='warning')
    if gu == TRUE:
      self.new_game()
    else:
      pass


root = Tk()
myapp = App(root)
root.mainloop()


# TEXT : https://effbot.org/tkinterbook/canvas.htm#Tkinter.Canvas.create_text-method
# HANGMAN EXAMPLE : https://www.practicepython.org/exercise/2016/09/24/30-pick-word.html
