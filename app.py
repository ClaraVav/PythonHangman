from tkinter import *
from tkinter import colorchooser, messagebox, simpledialog
from random import randint
from PIL import Image, ImageTk


class App:

  def __init__(self,parent):
    # Základní nastavení
    self.color_fg = 'black'
    self.color_bg = 'white'
    self.found_letters = []
    self.slovo = ""
    self.wrong = 0
    self.image = Image.open('images\construction.png')
    self.letter = ""
    self.uhadnute = []
    self.text = 'black'
    self.x = 0
    self.y = 0
    self.parent = parent
    self.files()
    self.gui()


  def gui(self):  # DONE
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

  # Načtení slova ze souboru
  def files(self):  # DONE
    
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
    mid_pos = self.parent.winfo_screenwidth()/5
    self.canvas.create_text(mid_pos,50,text="Vítejte !",font=("Courier",18),fill=self.text)

    img = ImageTk.PhotoImage(self.image)
    mg = Label(self.canvas,image=img).pack()

    # Zobrazení slova/čárek
    x = 0
    y = 0
    for a in self.slovo:
      if self.letter == a:
        self.canvas.create_text(50+x,125,text=" "+self.letter+" ",anchor="w",font=("Courier",14),fill=self.text)
        if self.found_letters[y] == " _ ":
          self.found_letters[y] = self.letter
      elif self.letter == self.found_letters[y]:
        self.canvas.create_text(50+x,125,text=" "+self.letter+" ",anchor="w",font=("Courier",14),fill=self.text)
      else:
        self.canvas.create_text(50+x,125,text=" _ ",anchor="w",font=("Courier",14),fill=self.text)
      y += 1
      x = x+33

    # Tlačítko
    btn = Button(self.canvas, text="Zadat písmeno", command=self.pismeno_input).pack(side=LEFT)

    self.canvas.pack(fill=BOTH,expand=True)
    

  # Funkce:

  # Zadání písmena
  def pismeno_input(self):
    guess = simpledialog.askstring("Písmeno", "Zadejte písmeno:", parent=root)
    if self.letter:
      self.letter = guess.upper()
      print(self.letter)
      self.hadanka()
      self.redraw_canvas()

  # Zjištění jestli je písmeno již zadané / ve slově
  def hadanka(self):
    # Uhádnutí písmena ve slově
    if (len(self.letter)>1):
      print("More than one character")
      self.pismeno_input()
    elif not re.match("[A-Z]", self.letter):
      print("Wrong character")
    else:
      for i in self.uhadnute:
        if self.letter == self.uhadnute[i]:
          print("Already guessed")
        else:
          for n in self.slovo:
            if (self.letter != n):
              self.wrong += 1
              print("Wrong letter")
              self.uhadnute.append(self.letter)
            else:
              print("Right letter")
              self.uhadnute.append(self.letter)

  # Překreslení canvasu - DONE
  def redraw_canvas(self):     
    self.canvas.delete("all")
    self.cvs()
    print("Redrawing...")
  
  # Nová hra - DONE
  def new_game(self):
    self.redraw_canvas()
    self.wrong = 0
    print("Nová hra")
    self.files()

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
    print("Hráč se vzdává?")
    gu = messagebox.askyesno('Giving up ?', 'Are you sure about this ?', icon='warning')
    if gu == TRUE:
      print("Ano")
      self.new_game()
    else:
      print("Ne")
      pass


root = Tk()
root.title("Hangman")
myapp = App(root)
root.mainloop()

# GitHub: https://github.com/ClaraVav/PythonHangman
