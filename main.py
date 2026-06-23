import tkinter as tk
from cryptography.fernet import Fernet
import hashlib
import base64
from tkinter import messagebox

window = tk.Tk()
window.title("Secret Notes")
window.minsize(500,720)

img = tk.PhotoImage(file="noteb.png")
img_label = tk.Label(window, image=img)
img_label.pack()

label1 = tk.Label(window, text="Title", font=("Arial", 15))
label1.pack(pady=(15, 0))

entry1 = tk.Entry(window, width=35, font=("Malgun Gothic",12))
entry1.pack()

label2 = tk.Label(window, text="Enter Your Text", font=("Arial", 15))
label2.pack(pady=(5, 0))

text2 = tk.Text(window, width=45, height=15, font=("Malgun Gothic", 12))
text2.pack()

label3 = tk.Label(window, text="Enter Password", font=("Arial", 15))
label3.pack(pady=(5,0))

entry3 = tk.Entry(window, width=35, font=("Malgun Gothic",12), show="*")
entry3.pack()

def password_to_key(password):
    hash_digest = hashlib.sha256(password.encode()).digest()
    return base64.urlsafe_b64encode(hash_digest)

def saving():
    title = entry1.get()
    secret = text2.get("1.0", "end-1c")
    password = entry3.get()
    if len(title) ==0 or len(secret) ==0 or len(password) ==0:
        tk.messagebox.showerror("Error", "Please enter all fields!")
    else:
        try:
            key = password_to_key(password)
            fernet = Fernet(key)
            secretted = fernet.encrypt(secret.encode("utf-8"))
            with open("secrets.txt", "a") as f:
                f.write(f"{title}\n{secretted.decode()}\n")
            entry1.delete(0, tk.END)
            entry3.delete(0, tk.END)
            text2.delete("1.0", tk.END)
            tk.messagebox.showinfo("Successful", "Secret notes saved")
        except Exception as e:
            print(f"Encryption error: {repr(e)}")
            messagebox.showerror("Error", "An error occurred while saving the note.")

def decryption():
    try:
        secret_input = text2.get("1.0", "end-1c").encode()
        password = entry3.get()
        if len(text2.get("1.0", "end-1c")) != 0 and len(password) != 0:
            key = password_to_key(password)
            fernet = Fernet(key)
            decrypted = fernet.decrypt(secret_input).decode()
            text2.delete("1.0", tk.END)
            text2.insert(tk.END, decrypted)
        else:
            tk.messagebox.showerror("Error!", "Enter all fields!")
    except Exception as e:
        print(f"Decryption error: {repr(e)}")
        messagebox.showwarning("Access Denied", "Wrong password or corrupted secret data!")

button1 = tk.Button(window, text="Save & Encrypt", command=saving)
button1.pack(pady=10)
button2 = tk.Button(window, text="Decrypt", command=decryption)
button2.pack()

window.mainloop()
