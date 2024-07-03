import tkinter as tk
from tkinter.filedialog import askopenfilename, asksaveasfilename


class Canvas:
    def __init__(self) -> None:
        self.window = tk.Tk()
        self.size = 1000
        self.canvas = tk.Canvas(self.window, width=self.size, height=self.size)
        self.canvas.grid()
        self.file = None
        self.photo = None
        self.photo_image = None
        self.file_var = tk.StringVar()
        self.file_var.set(self.file if self.file is not None else "No file selected")
        self.export_text_var = tk.StringVar()
        self.export_text_var.set("Export Image")

        # <-- Denser ----------------------------------------------- Sparser -->
        self.density_string = (
            "$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,\"^`'."
        )

        tk.Button(
            self.window,
            text="Pick image",
            bg="yellow",
            command=self.select_file,
        ).grid(row=2, column=0)
        tk.Button(
            self.window,
            textvariable=self.export_text_var,
            bg="yellow",
            command=self.export_image,
        ).grid(row=3, column=0)
        tk.Label(self.window, textvariable=self.file_var).grid(row=1, column=0)

        self.window.mainloop()

    def get_character(self, avg: int) -> chr:
        if avg == 0:
            return self.density_string[-1]
        return self.density_string[int(((avg * len(self.density_string)) // 255) - 1)]

    def select_file(self) -> None:
        allowedTypes = [("PNG files", "*.png")]
        self.file = askopenfilename(filetypes=allowedTypes)
        if self.file is None or self.file == "":
            return
        self.file_var.set(self.file)
        self.photo = Image.open(self.file)
        self.photo = self.photo.resize((250, 250))
        width, height = self.photo.size

        # Draw a rectangle to clear the canvas
        self.canvas.create_rectangle(0, 0, self.size, self.size, fill="white")

        for y in range(0, height):
            for x in range(0, width):
                pixel = self.photo.getpixel((x, y))
                r = pixel[0]
                g = pixel[1]
                b = pixel[2]
                hex_color = "#{:02x}{:02x}{:02x}".format(r, g, b)
                avg = (r + g + b) / 3
                self.canvas.create_text(
                    x * 4,
                    y * 4,
                    anchor="nw",
                    font=("Courier", "4", "bold"),
                    text=self.get_character(avg),
                    fill=hex_color,
                )

    def export_image(self) -> None:
        if self.photo is None:
            self.select_file()
        self.export_text_var.set("Exporting Image")
        width, height = self.photo.size
        dlg = asksaveasfilename(filetypes=[("Text File", "*.txt")])
        fname = dlg
        if fname != "":
            try:
                f = open(fname, "w")
                for y in range(0, height):
                    for x in range(0, width):
                        pixel = self.photo.getpixel((x, y))
                        r = pixel[0]
                        g = pixel[1]
                        b = pixel[2]
                        avg = (r + g + b) / 3
                        f.write(self.get_character(avg))
                    f.write("\n")
                f.close()
                self.export_text_var.set("Export Image Completed")
            except:
                self.export_text_var.set("Export Image Failed")
                return


if __name__ == "__main__":
    Canvas()
