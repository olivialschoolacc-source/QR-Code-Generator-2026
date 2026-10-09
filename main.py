import os
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import qrcode
from datetime import datetime
import ctypes
from ctypes import wintypes

class QRCodeGeneratorApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("QR Code Generator")
        self.root.geometry("400x620")
        self.root.resizable(False, False)
        self.root.configure(bg="#f0f0f0")

        self.mainFrame = tk.Frame(self.root, bg="#f0f0f0")
        self.mainFrame.pack(fill=tk.BOTH, expand=True)

        self.qrImage = None

        self.callFonts()

        self.placeComponents()

    def splitFrame(self, imagePath, borderSize=20):
        image = Image.open(imagePath).convert("RGBA")
        width, height = image.size

        bx = min(borderSize, width // 3)
        by = min(borderSize, height // 3)

        x1, x2 = bx, width - bx
        y1, y2 = by, height - by

        coordinates = [
            (0, 0, x1, y1),
            (x1, 0, x2, y1),
            (x2, 0, width, y1),
            (0, y1, x1, y2),
            (x1, y1, x2, y2),
            (x2, y1, width, y2),
            (0, y2, x1, height),
            (x1, y2, x2, height),
            (x2, y2, width, height)
        ]

        return [image.crop(box) for box in coordinates]

    
    def placeFrame(self, parent, x, y, width, height):
        season = self.checkSeason()

        imagePath = os.path.join(
            os.path.dirname(__file__),
            "assets", "images", season,
            season + "Button.png"
        )

        pieces = self.splitFrame(imagePath, borderSize=20)

        canvas = tk.Canvas(
            parent,
            width=width,
            height=height,
            highlightthickness=0,
            bd=0,
            bg=parent.cget("bg")
        )
        canvas.place(x=x, y=y)

        leftW = pieces[0].width
        rightW = pieces[2].width
        topH = pieces[0].height
        bottomH = pieces[6].height

        positions = [
            (0, 0, leftW, topH),
            (leftW, 0, max(1, width - leftW - rightW), topH),
            (width - rightW, 0, rightW, topH),

            (0, topH, leftW, max(1, height - topH - bottomH)),
            (leftW, topH, max(1, width - leftW - rightW), max(1, height - topH - bottomH)),
            (width - rightW, topH, rightW, max(1, height - topH - bottomH)),

            (0, height - bottomH, leftW, bottomH),
            (leftW, height - bottomH, max(1, width - leftW - rightW), bottomH),
            (width - rightW, height - bottomH, rightW, bottomH)
        ]

        if not hasattr(self, "frameImages"):
            self.frameImages = []

        for piece, (px, py, pw, ph) in zip(pieces, positions):
            resized = piece.resize(
                (max(1, pw), max(1, ph)),
                Image.Resampling.NEAREST
            )
            photo = ImageTk.PhotoImage(resized)
            self.frameImages.append(photo)
            canvas.create_image(px, py, image=photo, anchor="nw")

        return canvas


    def callImages(self):
        imagePath = os.path.join(os.path.dirname(__file__), "assets", "images")
        
        self.SpringQRBG = Image.open(os.path.join(imagePath, "Spring", "SpringQRBG.png"))
        self.SummerQRBG = Image.open(os.path.join(imagePath, "Summer", "SummerQRBG.png"))
        self.FallQRBG = Image.open(os.path.join(imagePath, "Fall", "FallQRBG.png"))
        self.WinterQRBG = Image.open(os.path.join(imagePath, "Winter", "WinterQRBG.png"))

    def callFonts(self):
        fontPath = os.path.join(os.path.dirname(__file__), "assets", "fonts")

        self.grapeSodaFont = os.path.join(fontPath, "GrapeSoda.ttf")

        if not os.path.exists(self.grapeSodaFont):
            raise FileNotFoundError(f"Font file not found: {self.grapeSodaFont}")

        FR_PRIVATE = 0x10

        result = ctypes.windll.gdi32.AddFontResourceExW(self.grapeSodaFont, FR_PRIVATE, 0)

        if result == 0:
            raise RuntimeError(f"Failed to load font: {self.grapeSodaFont}")

        self.grapeSodaFontName = "GrapeSoda"

    def checkSeason(self):
        month = datetime.now().month

        if month in [3, 4, 5]:
            return "Spring"
        elif month in [6, 7, 8]:
            return "Summer"
        elif month in [9, 10, 11]:
            return "Fall"
        else:
            return "Winter"

    def imagesFromSeasons(self):
        self.callImages()
        season = self.checkSeason()

        if season == "Spring":
            self.backgroundImage = ImageTk.PhotoImage(
                                self.SpringQRBG.resize((280, 280), Image.Resampling.NEAREST)
                            )
        elif season == "Summer":
            self.backgroundImage = ImageTk.PhotoImage(
                                self.SummerQRBG.resize((280, 280), Image.Resampling.NEAREST)
                            )
        elif season == "Fall":
            self.backgroundImage = ImageTk.PhotoImage(
                                self.FallQRBG.resize((280, 280), Image.Resampling.NEAREST)
                            )
        else:
            self.backgroundImage = ImageTk.PhotoImage(
                                self.WinterQRBG.resize((280, 280), Image.Resampling.NEAREST)
                            )
    
    def createComponents(self):

        self.imagesFromSeasons()

        self.titleLabel = tk.Label(
            self.mainFrame,
            text="QR Code Generator",
            font=(self.grapeSodaFontName, 20, "bold"),
            bg="#f0f0f0"
            )
        
        self.entryLabel = tk.Label(
            self.mainFrame,
            text="Enter Text or URL:",
            font=(self.grapeSodaFontName, 14),
            bg="#f0f0f0"
            )
        
        self.entry = tk.Entry(
            self.mainFrame,
            font=(self.grapeSodaFontName, 16),
            width=35
            )
        
        self.QRFrame = tk.Frame(
            self.mainFrame,
            width=280,
            height=280,
            bg="#f0f0f0"
            )

        self.QRFrame.pack_propagate(False)

        self.QRBGLabel = tk.Label(
            self.QRFrame,
            image=self.backgroundImage,
            borderwidth=0
        )

        self.QRBGLabel.place(
            x=0,
            y=0,
            relwidth=1,
            relheight=1
        )
        
        self.imageLabel = tk.Label(
            self.QRFrame,
            text="Your QR Code will\nappear here",
            font=(self.grapeSodaFontName, 16),
            bg="white"
            )

        self.imageLabel.place(
            relx=0.5,
            rely=0.5,
            anchor="center"
        )

    def makeCanvasButton(self, x, y, width, height, text, command, state=tk.NORMAL):
        canvas = self.placeFrame(self.mainFrame, x, y, width, height)
        
        color = "#000000" if state == tk.NORMAL else "#888888"
        
        text_id = canvas.create_text(
            width // 2,
            height // 2,
            text=text,
            font=(self.grapeSodaFontName, 15),
            fill=color
        )
        
        canvas.button_state = state
        canvas.button_text_id = text_id
        
        def on_click(event):
            if getattr(canvas, "button_state", tk.NORMAL) == tk.NORMAL:
                command()
                
        canvas.bind("<Button-1>", on_click)
        canvas.tag_bind(text_id, "<Button-1>", on_click)
        return canvas

    def setCanvasButtonState(self, canvas, state):
        canvas.button_state = state
        color = "#000000" if state == tk.NORMAL else "#888888"
        canvas.itemconfig(canvas.button_text_id, fill=color)


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

            previewImage = self.qrImage.resize((160, 160), Image.Resampling.NEAREST)
            self.tkImage = ImageTk.PhotoImage(previewImage)

            self.imageLabel.config(image=self.tkImage, text="")
            self.setCanvasButtonState(self.saveButtonCanvas, tk.NORMAL)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to generate QR Code. \n{e}")

    
    
    def placeComponents(self):
        self.createComponents()

        self.titleLabel.place(
            x=0, y=10, width=400, height=35
        )

        self.entryLabel.place(
            x=30, y=50, width=340, height=25
        )

        self.entry.place(
            x=40, y=80, width=320, height=30
        )

        # Generate button
        self.generateButtonCanvas = self.makeCanvasButton(
            50, 125, 300, 70, "Generate QR Code", self.generateQR
        )

        # Save button
        self.saveButtonCanvas = self.makeCanvasButton(
            50, 205, 300, 70, "Save QR Code", self.saveQR, state=tk.DISABLED
        )

        # QR preview
        self.QRFrame.place(
            x=60, y=295, width=280, height=280
        )



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