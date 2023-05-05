import time as tm
from multiprocessing import Process
import asyncio
import customtkinter

import GETAPI
import os


def set_reminder(park_name, ride_name, time):
    api = GETAPI.API()
    api.get_parks()
    # print(type(time))
    # print(time)
    while True:
        current_time = api.get_ride_time(park_name, ride_name)
        if current_time == -1:
            continue
        elif current_time < time:
            break
        tm.sleep(5 * 60)  # Update every 5 minutes

    TopLevelRemindUser(ride_name, current_time)


class TopLevelRemindUser(customtkinter.CTk):
    def __init__(self, ride_name, time):
        super().__init__()
        customtkinter.set_appearance_mode("light")
        customtkinter.set_default_color_theme("dark-blue")

        self.geometry("600x150")
        self.title("Reminder")
        self.reminder_Label = customtkinter.CTkLabel(self,
                                                     text="The wait time of " + ride_name +
                                                          " is " + str(time) + " minutes now!",
                                                     fg_color="transparent",
                                                     text_color="black",
                                                     font=("Arial", 22))
        self.reminder_Label.grid(row=0, column=0, sticky="nsew")
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.mainloop()


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
        self.grid_rowconfigure((0, 1, 2, 3), weight=1)
        self.Label = customtkinter.CTkLabel(self,
                                            text="Remind me when the wait time less than ",
                                            fg_color="transparent",
                                            text_color="black",
                                            font=("Arial", 18))
        self.Label.grid(row=1, column=0, sticky="nsew")
        self.option_menu = customtkinter.CTkOptionMenu(self,
                                                       values=["15min", "30min", "45min", "60min", "75min", "90min"])
        self.option_menu.set("15min")
        self.option_menu.grid(row=2, column=0, padx=(30, 30), pady=(30, 30), sticky="nsew")
        self.reminder_button = customtkinter.CTkButton(self, text="Remind me!",
                                                       command=self.remind_me,
                                                       font=("Robot", 18))
        self.reminder_button.grid(row=3, column=0, padx=(10, 10), pady=(10, 10), sticky="nsew")

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
        p = Process(target=set_reminder, args=(self.park_name, self.ride_name, int(time.removesuffix("min"))))
        p.start()



class QueueTimeFrame(customtkinter.CTkScrollableFrame):
    park_name = None

    def __init__(self, master):
        super().__init__(master)

        self.reminder = None
        self.fresh_button = None
        self.error_label = None
        self.master = master
        self.grid_columnconfigure((0, 3), weight=10)
        self.grid_columnconfigure((1, 4), weight=1)
        self.grid_columnconfigure((2, 5), weight=1)

    def update_ride(self, attractions, closed, park_name):
        self.park_name = park_name
        i: int = 0
        j: int = 0
        for key in attractions:
            ride_name = customtkinter.CTkLabel(self, text=key,
                                               fg_color="transparent",
                                               text_color="black",
                                               font=("Arial", 18))
            ride_name.grid(row=i, column=0, sticky="nsew")

            ride_reminder = customtkinter.CTkButton(self, text="Reminder",
                                                    command=lambda park_name_=park_name, ride_name_=key: self.button(
                                                        park_name_, ride_name_),
                                                    font=("Robot", 18))
            ride_reminder.grid(row=i, column=1, padx=(15, 15), pady=(10, 10), sticky="nsew")

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
            ride_time.grid(row=i, column=2, padx=(10, 10), pady=(10, 10), sticky="nsew")
            i = i + 1

        for ride in closed:
            ride_name = customtkinter.CTkLabel(self, text=ride,
                                               fg_color="transparent",
                                               text_color="black",
                                               font=("Arial", 18))
            ride_name.grid(row=i, column=0, columnspan=2, sticky="nsew")

            ride_time = customtkinter.CTkLabel(self, text="Closed",
                                               fg_color="grey",
                                               font=("Arial", 18))
            ride_time.grid(row=i, column=2, padx=(10, 10), pady=(10, 10), sticky="nsew")
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

    def button(self, park_name, ride_name):
        self.reminder = TopLevelReminder(self, park_name, ride_name)


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
