import tkinter
import requests

class CanteenApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Canteen CRUD App")
        self.root.geometry("600x650")
        self.root.resizable(False, False)

        self.name_label = tkinter.Label(self.root, text="Name:")
        self.name_label.grid(row=0, column=0, sticky='e')
        self.name = tkinter.Entry(self.root, width=40)
        self.name.grid(row=0, column=1)

        self.location_label = tkinter.Label(self.root, text="Location:")
        self.location_label.grid(row=1, column=0, sticky='e')
        self.location = tkinter.Entry(self.root, width=40)
        self.location.grid(row=1, column=1)

        self.time_open_label = tkinter.Label(self.root, text="Time Open:")
        self.time_open_label.grid(row=2, column=0, sticky='e')
        self.time_open = tkinter.Entry(self.root, width=40)
        self.time_open.grid(row=2, column=1)


        self.time_closed_label = tkinter.Label(self.root, text="Time Closed:")
        self.time_closed_label.grid(row=3, column=0, sticky='e')
        self.time_closed = tkinter.Entry(self.root, width=40)
        self.time_closed.grid(row=3, column=1)

        self.add_button = tkinter.Button(self.root, text="Add", command=self.add_canteen)
        self.add_button.grid(row=4, column=0)
        self.update_button = tkinter.Button(self.root, text="Update", command=self.update_canteen)
        self.update_button.grid(row=4, column=1)
        self.delete_button = tkinter.Button(self.root, text="Delete", command=self.delete_canteen)
        self.delete_button.grid(row=4, column=2)

        self.canteens_listbox = tkinter.Listbox(self.root, width=95, height=20)
        self.canteens_listbox.grid(row=5, column=0, columnspan=3)
        self.canteens_listbox.bind("<ButtonRelease-1>", self.on_click)
        self.canteens_listbox.bind("<Up>", self.on_click)
        self.canteens_listbox.bind("<Down>", self.on_click)

        self.time_filter_label = tkinter.Label(self.root, text="Filter by Open Time (HH:MM):")
        self.time_filter_label.grid(row=7, column=0)
        self.time_filter_entry = tkinter.Entry(self.root)
        self.time_filter_entry.grid(row=7, column=1)
        self.filter_button = tkinter.Button(self.root, text="Filter", command=self.filter_by_open_time)
        self.filter_button.grid(row=7, column=2)

        self.refresh_canteens()

    def add_canteen(self):
        data = {
            'name': self.name.get(),
            'location': self.location.get(),
            'time_open': self.time_open.get(),
            'time_closed': self.time_closed.get()
        }
        response = requests.post("http://127.0.0.1:5000/api/add_canteen", data=data)
        if response.status_code == 201:
            self.refresh_canteens()

    def update_canteen(self):
        selected_index = self.canteens_listbox.curselection()
        if selected_index:
            canteen_id = self.canteens_listbox.get(selected_index)[0]
            data = {
                'id': canteen_id,
                'name': self.name.get(),
                'location': self.location.get(),
                'time_open': self.time_open.get(),
                'time_closed': self.time_closed.get()
            }
            response = requests.put(f"http://127.0.0.1:5000/api/canteens/update/", data=data)
            if response.status_code == 200:
                self.refresh_canteens()

    def delete_canteen(self):
        selected_index = self.canteens_listbox.curselection()
        if selected_index:
            canteen_id = self.canteens_listbox.get(selected_index)[0]
            response = requests.delete(f"http://127.0.0.1:5000/api/canteens/delete/{canteen_id}")
            if response.status_code == 200:
                self.refresh_canteens()

    def refresh_canteens(self):
        self.canteens_listbox.delete(0, tkinter.END)
        response = requests.get("http://127.0.0.1:5000/api/canteens")
        if response.status_code == 200:
            canteens = response.json()
            for canteen in canteens:
                canteen_str = f"{canteen['name']}, {canteen['location']}, Open: {canteen['time_open']}, Close: {canteen['time_closed']}"
                self.canteens_listbox.insert(tkinter.END, (canteen['id'], canteen_str))

    def on_click(self, event):
        selected_index = self.canteens_listbox.curselection()
        if selected_index:
            canteen_id = self.canteens_listbox.get(selected_index)[0]
            response = requests.get(f"http://127.0.0.1:5000/api/canteens/update/{canteen_id}")
            if response.status_code == 200:
                canteen = response.json()

                self.name.delete(0, 'end')
                self.location.delete(0, 'end')
                self.time_open.delete(0, 'end')
                self.time_closed.delete(0, 'end')

                self.name.insert(0, canteen['name'])
                self.location.insert(0, canteen['location'])
                self.time_open.insert(0, canteen['time_open'])
                self.time_closed.insert(0, canteen['time_closed'])


    def filter_by_open_time(self):
        time = self.time_filter_entry.get()
        if time:
            response = requests.get(f"http://127.0.0.1:5000/api/canteens/open/{time}")
            if response.status_code == 200:
                canteens = response.json()

                self.canteens_listbox.delete(0, tkinter.END)

                for canteen in canteens:
                    canteen_str = f"{canteen['name']}, {canteen['location']}, Open: {canteen['time_open']}, Close: {canteen['time_closed']}"
                    self.canteens_listbox.insert(tkinter.END, (canteen['id'], canteen_str))


if __name__ == "__main__":
    window = tkinter.Tk()
    app = CanteenApp(window)
    window.mainloop()
