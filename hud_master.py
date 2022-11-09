import os

while True:
    x = input("Command: ")

    if "text" in x:
        if x[4] == "0":
            with open ("master_text.txt", "w") as ms:
                ms.write("")
            with open ("master_text1.txt", "w") as ms1:
                ms1.write("")
            with open ("master_text2.txt", "w") as ms2:
                ms2.write("")
            with open ("master_text3.txt", "w") as ms3:
                ms3.write("")
        if x[4] == "1":
            with open ("master_text.txt", "w") as ms:
                ms.write(x)
        if x[4] == "2":
            with open ("master_text1.txt", "w") as ms1:
                ms1.write(x[5: ])
        if x[4] == "3":
            with open ("master_text2.txt", "w") as ms2:
                ms2.write(x[5: ])
        if x[4] == "4":
            with open ("master_text3.txt", "w") as ms3:
                ms3.write(x[5: ])

    if x == "stream":
        with open ("status.txt", "w") as status:
            status.write(x)
    if x == "pic":
        with open ("status.txt", "w") as status:
            status.write(x)
    if x == "sound":
        with open ("sound.txt", "w") as sound:
            sound.write(x)
    if x == "nosound":
        with open ("sound.txt", "w") as sound:
            sound.write(x)
    if x == "sharpen":
        with open ("sharpen.txt", "w") as sh:
            sh.write(x)
    if x == "nosharpen":
        with open ("sharpen.txt", "w") as sh:
            sh.write(x)