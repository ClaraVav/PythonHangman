from tkinter import *
from tkinter import colorchooser, messagebox, simpledialog
from random import randint
from PIL import Image, ImageTk
import os.path


class App:

  def __init__(self,parent):
    # Základní nastavení
    self.color_fg = 'black'
    self.color_bg = 'white'
    self.found_letters = []
    self.slovo = ""
    self.wrong = 0
    self.images = ['construction','head','torso','left_hand','right_hand','left_leg','right_leg']
    self.letter = ""
    self.uhadnute = ["."]
    self.text = 'black'
    self.x = 0
    self.y = 0
    self.v = 0
    self.g = 0
    self.parent = parent
    self.files()
    self.gui()


  def gui(self):  # DONE
    # Nastavení obrazovky
    screen_width = self.parent.winfo_screenwidth()
    screen_height = self.parent.winfo_screenheight()
    width = screen_width / 3*2 - 45
    height = screen_width / 5*2 - 50
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
    self.canvas = Canvas(self.parent, width=screen_width / 5 * 2, height=screen_height / 5 * 2, bg=self.color_bg, highlightthickness=3, highlightbackground="gray")

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
    for a in self.slovo:
      self.found_letters.append("_")
    

  # Canvas:

  def cvs(self):
    # Text "Vítejte"
    self.canvas.create_text(self.parent.winfo_screenwidth()/5,50,text="Vítejte !",font=("Courier",18),fill=self.text)
    # Obrázek
    img = ImageTk.PhotoImage(Image.open(os.path.normpath('images/'+self.images[self.wrong]+'.png')))
    mg = Label(self.canvas,image=img,background="White")
    mg.image = img
    mg.place(x=600,y=3)

    # Zobrazení slova/čárek
    x = 0
    y = 0
    for a in self.slovo:
      if self.letter == a:
        if self.found_letters[y] == "_":
          self.found_letters[y] = self.letter
          self.g += 1
      for b in self.found_letters:
        self.canvas.create_text(50+x,125,text=""+self.found_letters[y]+"",anchor="w",font=("Courier",14),fill=self.text)
      y += 1
      x = x+33
    print(self.found_letters)
    
    if len(self.found_letters) == len(self.slovo):
      if self.g == len(self.slovo):
        print(len(self.slovo))
        print(self.g)
        self.win()
    if self.wrong == len(self.images)-1:
      self.lose()

    # Tlačítko
    btn = Button(self.canvas, text="Zadat písmeno", command=self.pismeno_input).place(x=55,y=155)

    self.canvas.pack(fill=BOTH,expand=True)


  # Funkce:

  # Zadání písmena
  def pismeno_input(self):
    print("Input")
    guess = simpledialog.askstring("Písmeno", "Zadejte písmeno:", parent=root)
    if guess:
      self.letter = guess.upper()
      print(self.letter)
      self.hadanka()
      self.redraw_canvas()

  # Zjištění jestli je písmeno již zadané / ve slově
  def hadanka(self):
    print("Finding")
    self.v = 0
    if (len(self.letter)>1):
      print("More than one character")
      messagebox.showinfo('Špatný počet znaků','Zadali jste špatný počet znaků.')
      self.pismeno_input()
    elif not re.match("[A-Z]", self.letter):
      print("Wrong character")
      messagebox.showinfo('Špatný znak','Zadali jste špatný znak, zadejte prosím jen písmena A - Z.')
      self.pismeno_input()
    else:
      for i in range(len(self.uhadnute)):
        if self.letter == self.uhadnute[i]:
          print("Already guessed")
          self.pismeno_input()
        else:
          for n in self.slovo:
            #if (self.letter != n):
              #print("Wrong letter")
              #print(self.v)
            #else:
              self.v += 1
              #print(self.v)
              #print("Right letter")
      self.uhadnute.append(self.letter)
    if self.v == 0:
      self.wrong += 1
      self.v = 0
    print(self.wrong)  

  # Překreslení canvasu - DONE
  def redraw_canvas(self):     
    self.canvas.delete("all")
    self.cvs()
    print("Redrawing...")

  # Nová hra - DONE
  def new_game(self):
    self.wrong = 0
    self.g = 0
    self.slovo = ""
    self.found_letters = []
    self.uhadnute = ["."]
    self.letter = ""
    self.files()
    self.redraw_canvas()
    print("Nová hra")
  
  # Výhra
  def win(self):
    print("Win")
    wn = messagebox.askyesno('Výhra !', 'Chcete novou hru ?', icon='information')
    if wn == True:
      print("Win - new game")
      self.new_game()
    else:
      print("Win - end game")
      root.destroy()

  # Prohra
  def lose(self):
    print("Lose")
    ls = messagebox.askyesno('Prohra !', 'Chcete novou hru ?', icon='information')
    if ls == True:
      print("Lose - new game")
      self.new_game()
    else:
      print("Lose - end game")
      root.destroy()

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
    if gu == True:
      print("Ano")
      self.new_game()
    else:
      print("Ne")


root = Tk()
root.title("Hangman")
myapp = App(root)
root.mainloop()

# GitHub: https://github.com/ClaraVav/PythonHangman
