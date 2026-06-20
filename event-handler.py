from tkinter import *
window=Tk()
window.title("event_handler")
window.geometry("100x100")
def handle_key_press(event):
  '''print the character associated to the key press'''
  print(event.char)
window.bind("<Key>",handle_key_press)
def handle_click(event):
  print("\nThe button was clicked ")
button=Button(text="Click me")
button.pack()
button.bind("<Button-1>",handle_click)
window.mainloop()
