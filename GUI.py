import customtkinter


class ParkListFrame(customtkinter.CTkScrollableFrame):
    def __init__(self, master):
        super().__init__(master)

        self.parks_ = []
        self.grid_columnconfigure(0, weight=1)
        self.label = customtkinter.CTkLabel(self, text="Getting the list of park...",
                                            fg_color="transparent",
                                            font=("Arial", 18))
        self.label.grid(row=0, column=0, sticky="nsew")

    def update_parks(self, parks):
        self.label.destroy()
        for park in parks:
            park_button = customtkinter.CTkButton(self, text=park,
                                                  fg_color="transparent",
                                                  font=("Robot", 12),
                                                  command=lambda park_name=park: self.button_callback(park_name))
            park_button.grid(row=len(self.parks_), column=0, sticky="nsew")
            self.parks_.append(park_button)

    def button_callback(self, park_name):
        print(park_name)



class ParkFrame(customtkinter.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=20)

        self.title = customtkinter.CTkLabel(self, text="Park Name", fg_color="transparent", font=("Arial", 28))
        self.title.grid(row=0, column=0)

        self.park_list = ParkListFrame(self)
        self.park_list.grid(row=1, column=0, sticky="nsew")

    def update_parks(self, parks):
        self.park_list.update_parks(parks)


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.title("Parks Queue Times")
        self.geometry("1920x1080")
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=15)

        self.park_frame = ParkFrame(self)
        self.park_frame.grid(row=0, column=0, sticky="nsew")
        self.update_idletasks()

    def update_parks(self, parks):
        self.park_frame.update_parks(parks)
