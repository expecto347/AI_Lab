import customtkinter

import GETAPI


class TopLevelReminder(customtkinter.CTkToplevel):
    def __init__(self, master, park_name, ride_name):
        super().__init__(master)
        self.label = None
        self.park_name = park_name
        self.ride_name = ride_name
        self.geometry("400x300")
        self.title("Reminder")
        self.reminder_Label = customtkinter.CTkLabel(self,
                                                     text=ride_name,
                                                     fg_color="transparent",
                                                     text_color="black",
                                                     font=("Arial", 22))
        self.reminder_Label.grid(row=0, column=0, sticky="nsew")
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure((0, 1, 2), weight=1)
        self.option_menu = customtkinter.CTkOptionMenu(self,
                                                       values=["15min", "30min", "45min", "60min", "75min", "90min"])
        self.option_menu.set("15min")
        self.option_menu.grid(row=1, column=0)
        self.reminder_button = customtkinter.CTkButton(self, text="Remind me!",
                                                       command=self.remind_me,
                                                       font=("Robot", 18))
        self.reminder_button.grid(row=2, column=0)

    def remind_me(self):
        time = self.option_menu.get()
        self.reminder_button.destroy()
        self.option_menu.destroy()
        self.label = customtkinter.CTkLabel(self, text_color="black",
                                            fg_color="transparent",
                                            text="Reminder set! ",
                                            font=("Arial", 18))
        self.label.grid(row=1, column=0, sticky="nsew")
        self.grid_rowconfigure(1, weight=1)
        self.update()


class ProjectFrame(customtkinter.CTkFrame):
    def __init__(self, master, park_name, ride_name):
        super().__init__(master)
        self.remind_process = None
        self.park_name = park_name
        self.ride_name = ride_name
        self.remind_button = customtkinter.CTkButton(self, text="Remind me!",
                                                     fg_color="Blue",
                                                     text_color="black",
                                                     command=self.remind_me,
                                                     font=("Robot", 18))
        self.remind_button.grid(row=0, column=0, sticky="nsew")

    def remind_me(self):
        self.remind_process = TopLevelReminder(self, self.park_name, self.ride_name)


class QueueTimeFrame(customtkinter.CTkScrollableFrame):
    park_name = None

    def __init__(self, master):
        super().__init__(master)

        self.fresh_button = None
        self.error_label = None
        self.master = master
        self.grid_columnconfigure((0, 2), weight=10)
        self.grid_columnconfigure((1, 3), weight=1)

    def update_ride(self, attractions, closed, park_name):
        self.park_name = park_name
        i: int = 0
        j: int = 0
        for key in attractions:
            ride_name = customtkinter.CTkButton(self, text=key,
                                                fg_color="transparent",
                                                text_color="black",
                                                command=lambda ride_name_=key: self.button(ride_name_),
                                                font=("Arial", 18))
            ride_name.grid(row=i, column=j, sticky="nsew")
            j = j + 1

            if attractions[key] > 60:
                ride_time = customtkinter.CTkLabel(self, text=str(attractions[key]) + " minutes",
                                                   fg_color="red",
                                                   font=("Arial", 18))
            elif attractions[key] > 30:
                ride_time = customtkinter.CTkLabel(self, text=str(attractions[key]) + " minutes",
                                                   fg_color="orange",
                                                   font=("Arial", 18))
            elif attractions[key] > 15:
                ride_time = customtkinter.CTkLabel(self, text=str(attractions[key]) + " minutes",
                                                   fg_color="yellow",
                                                   font=("Arial", 18))
            else:
                ride_time = customtkinter.CTkLabel(self, text=str(attractions[key]) + " minutes",
                                                   fg_color="green",
                                                   font=("Arial", 18))
            ride_time.grid(row=i, column=j, padx=(10, 10), pady=(10, 10), sticky="nsew")
            j = j + 1
            if j == 4:
                j = 0
                i = i + 1
        for ride in closed:
            ride_name = customtkinter.CTkLabel(self, text=ride,
                                               fg_color="transparent",
                                               text_color="black",
                                               font=("Arial", 18))
            ride_name.grid(row=i, column=j, sticky="nsew")
            j = j + 1
            ride_time = customtkinter.CTkLabel(self, text="Closed",
                                               fg_color="grey",
                                               font=("Arial", 18))
            ride_time.grid(row=i, column=j, padx=(10, 10), pady=(10, 10), sticky="nsew")
            j = j + 1
            if j == 4:
                j = 0
                i = i + 1

        self.update()

    def get_ride_error(self, name):
        self.error_label = customtkinter.CTkLabel(self, text="Opos! Something went wrong!",
                                                  fg_color="transparent",
                                                  font=("Arial", 18))
        self.error_label.grid(row=0, column=0, columnspan=4, sticky="nsew")
        self.fresh_button = customtkinter.CTkButton(self, text="Refresh", fg_color="green",
                                                    font=("Robot", 30),
                                                    command=lambda park_name=name: self.refresh(park_name))
        self.fresh_button.grid(row=1, column=0, columnspan=4)

    def refresh(self, park_name):
        self.error_label.destroy()
        self.fresh_button.destroy()
        self.update()
        self.master.master.update_rides(park_name)

    def button(self, ride_name):
        self.master.master.update_project(self.park_name, ride_name)


class RideFrame(customtkinter.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        self.queue_time_frame = None
        self.master = master
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=10)

        self.title = customtkinter.CTkLabel(self, text="Please choose the park from the left list!",
                                            fg_color="transparent",
                                            font=("Arial", 28))
        self.title.grid(row=0, column=0, sticky="nsew")
        self.schedule = customtkinter.CTkLabel(self, text=" ",
                                               fg_color="transparent",
                                               text_color="grey",
                                               font=("Robot", 20))
        self.schedule.grid(row=1, column=0, sticky="nsew")
        self.queue_time_frame = QueueTimeFrame(self)
        self.queue_time_frame.grid(row=2, column=0, sticky="new")

    def update_rides(self, park_name, attractions, closed, closing_time, opening_time):
        self.title.configure(text=park_name)
        self.schedule.configure(text="Opening time: " + opening_time + "\nClosing time: " + closing_time)
        self.queue_time_frame.destroy()
        self.queue_time_frame = QueueTimeFrame(self)
        self.queue_time_frame.grid(row=2, column=0, sticky="nsew")
        self.queue_time_frame.update_ride(attractions, closed, park_name)
        self.update()

    def update_project(self, park_name, ride_name, wait_time):
        self.title.configure(text=ride_name)
        self.schedule.configure(text="Wait time: " + str(wait_time) + " minutes")
        self.queue_time_frame.destroy()
        self.queue_time_frame = ProjectFrame(self, park_name, ride_name)
        self.queue_time_frame.grid(row=2, column=0, sticky="nsew")

    def get_ride_error(self, name):
        self.queue_time_frame.destroy()
        self.title.configure(text=name)
        self.queue_time_frame = QueueTimeFrame(self)
        self.queue_time_frame.grid(row=2, column=0, sticky="nsew")
        self.queue_time_frame.get_ride_error(name)
        self.update()


class ParkListFrame(customtkinter.CTkScrollableFrame):
    refresh_button = None
    parks_ = None
    rides_ = None

    def __init__(self, master):
        super().__init__(master)

        self.master = master
        self.grid_columnconfigure(0, weight=1)
        self.label = customtkinter.CTkLabel(self, text="Getting the list of park...",
                                            fg_color="transparent",
                                            font=("Arial", 18))
        self.label.grid(row=0, column=0, sticky="nsew")

    def update_parks(self, parks):
        self.label.destroy()
        self.parks_ = []
        for park in parks:
            park_button = customtkinter.CTkButton(self, text=park,
                                                  fg_color="transparent",
                                                  text_color="black",
                                                  font=("Robot", 12),
                                                  command=lambda park_name=park: self.button_callback(park_name))
            park_button.grid(row=len(self.parks_), column=0, sticky="nsew")
            self.parks_.append(park_button)
        self.update()

    def update_rides(self, attractions):
        self.rides_ = []
        for park in self.parks_:
            park.destroy()
        for ride in attractions:
            ride_name = customtkinter.CTkButton(self, text=ride,
                                                fg_color="transparent",
                                                text_color="black",
                                                font=("Arial", 18))
            ride_name.grid(row=len(self.rides_), column=0, sticky="nsew")
            self.rides_.append(ride_name)
        self.update()

    def get_list_error(self):
        self.label.configure(text="Something went wrong!")
        self.refresh_button = customtkinter.CTkButton(self,
                                                      text="Refresh",
                                                      fg_color="green",
                                                      font=("Robot", 38),
                                                      command=self.refresh)
        self.refresh_button.grid(row=1, column=0, sticky="ns")
        self.update()

    def refresh(self):
        self.refresh_button.destroy()
        self.master.master.update_parks()

    def button_callback(self, park_name):
        self.master.master.update_rides(park_name)


class ParkFrame(customtkinter.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        self.master = master
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=20)

        self.title = customtkinter.CTkLabel(self, text="Park Name", fg_color="transparent", font=("Arial", 28))
        self.title.grid(row=0, column=0)

        self.park_list = ParkListFrame(self)
        self.park_list.grid(row=1, column=0, sticky="nsew")

    def update_parks(self, parks):
        self.title.configure(text="Park List")
        self.park_list.update_parks(parks)

    def get_list_error(self):
        self.park_list.get_list_error()

    def update_rides(self, attractions):
        self.title.configure(text="Ride List")
        self.park_list.update_rides(attractions)


class App(customtkinter.CTk):
    parks = None

    def __init__(self):
        super().__init__()

        self.closed = None
        self.attractions = None
        customtkinter.set_appearance_mode("light")
        customtkinter.set_default_color_theme("dark-blue")

        self.title("Parks Queue Times")
        self.geometry("1920x1080")
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=15)

        self.park_frame = ParkFrame(self)
        self.park_frame.grid(row=0, column=0, sticky="nsew")
        self.ride_frame = RideFrame(self)
        self.ride_frame.grid(row=0, column=1, sticky="nsew")
        self.update()
        self.api = GETAPI.API()
        self.update_parks()

    def update_parks(self):
        self.parks = self.api.get_parks()
        if self.parks == 0:
            self.park_frame.get_list_error()
        else:
            self.park_frame.update_parks(self.parks)

    def update_rides(self, name):
        self.attractions, self.closed = self.api.get_park(name)
        if self.attractions == 0:
            self.ride_frame.get_ride_error(name)
        else:
            closing_time, opening_time = self.api.get_schedule(name)
            if closing_time == 0:
                self.ride_frame.get_ride_error(name)
            else:
                self.ride_frame.update_rides(name, self.attractions, self.closed, closing_time, opening_time)
        self.update()

    def update_project(self, park_name, ride_name):
        self.park_frame.update_rides(self.attractions)
        self.ride_frame.update_project(park_name, ride_name, self.attractions[ride_name])
