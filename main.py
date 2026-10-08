import os
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import ImageTk
import qrcode

class QRCodeGeneratorApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("QR Code Generator")
        self.root.geometry("400x550")
        self.root.resizable(False, False)
        self.root.configure(bg="#f0f0f0")

        self.mainFrame = tk.Frame(self.root, bg="#f0f0f0")
        self.mainFrame.pack(fill=tk.BOTH, expand=True)

        self.qrImage = None

        self.placeComponents()

    def createComponents(self):
        self.titleLabel = tk.Label(self.mainFrame, text="QR Code Generator", font=("Helvetica", 16, "bold"), bg="#f0f0f0")
        self.entryLabel = tk.Label(self.mainFrame, text="Enter Text or URL:", font=("Helvetica", 10), bg="#f0f0f0")
        self.entry = tk.Entry(self.mainFrame, font=("Helvetica", 12), width=35)
        self.imageLabel = tk.Label(self.mainFrame, text="Your QR Code will appear here", font=("Helvetica", 12), bg="#f0f0f0")
        self.createButtons()

    def placeComponents(self):
        self.createComponents()

        self.titleLabel.pack(pady=(0,20))
        self.entryLabel.pack(anchor="w")
        self.entry.pack(pady=(5,20))
        self.generateButton.pack(fill=tk.X, pady=(0,10))
        self.saveButton.pack(fill=tk.X, pady=(0,20))
        self.imageLabel.pack(fill=tk.BOTH, expand=True, ipady=20)

    def createButtons(self):
        self.generateButton = tk.Button(self.mainFrame, text="Generate QR Code", font=("Helvetica", 11), command=self.generateQR)
        self.saveButton = tk.Button(self.mainFrame, text="Save QR Code", font=("Helvetica", 11), command=self.saveQR, state=tk.DISABLED)

    def generateQR(self):
        data = self.entry.get().strip()

        if not data or data == "https://":
            messagebox.showwarning("Warning", "Please enter some text or a valid URL to generate a QR code.")
            return
        try:
            qr=qrcode.QRCode(
                version = 1,
                error_correction = qrcode.constants.ERROR_CORRECT_M,
                box_size = 10,
                border = 4
            )
            qr.add_data(data)
            qr.make(fit=True)

            self.qrImage = qr.make_image(fill_color="black", back_color="white")

            previewImage = self.qrImage.resize((220, 220))
            self.tkImage = ImageTk.PhotoImage(previewImage)

            self.imageLabel.config(image=self.tkImage, text="")
            self.saveButton.config(state=tk.NORMAL)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to generate QR Code. \n{e}")

    def saveQR(self):
        if self.qrImage is None:
            return

        file_path = filedialog.asksaveasfilename(
            defaultextension = ".png",
            filetypes = [("PNG file", "*.png"), ("All files", "*.*")],
            title  ="Save QR Code As",
        )

        if file_path:
            self.qrImage.save(file_path)
            messagebox.showinfo("Success", "QR Code saved successfully!")


    def start(self):
        self.root.mainloop()

if __name__ == "__main__":
    QRCodeGeneratorApp().start()
