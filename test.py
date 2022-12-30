import pyperclip

with open("test.jpg", "w") as t:
    t.write(pyperclip.paste())