import customtkinter as ctk

# Constant app parameters
root = ctk.CTk()
root.title("R-Dictionary App")
width= root.winfo_screenwidth()
height= root.winfo_screenheight()
root.geometry("%dx%d+%d+%d" % (800, 500, ((width - 800) // 2), ((height - 500) / 2)))
root.resizable(False, False)
ctk.set_default_color_theme("dark-blue")
ctk.set_appearance_mode("system")

class AnimFrame2(ctk.CTkFrame):
	def __init__(self, parent, width, height, fg_color):
		super().__init__(master=parent, width=width, height=height, fg_color=fg_color)

		self.rel_x=0.5
		self.rel_y=-0.5

	def animate_down(self):
		self.rel_y += 0.01
		print(self.rel_y)
		self.place(relx=self.rel_x, rely=self.rel_y, anchor='center', relheight=1)
		if self.rel_y < 0.5:
			self.after(1, self.animate_down)

class AnimFrame1(ctk.CTkFrame):
	def __init__(self, parent, width, height):
		super().__init__(master=parent, width=width, height=height)

		self.rel_x=0.5
		self.rel_y=0.5

	def animate_up(self):
		self.rel_y -= 0.01
		print(self.rel_y)
		self.place(relx=self.rel_x, rely=self.rel_y)
		if self.rel_y > -0.5:
			self.after(1, self.animate_up)
		else:
			result_frame.animate_down()

# Function to start the process
def search_word_api(*x):
	search_word_frame.animate_up()
	entry_input = word_entry.get()
	if entry_input:
		app_name_label.configure(text=entry_input)
	else:
		app_name_label.configure(text="R-Dictionary")

search_word_frame = AnimFrame1(root, width=200, height=200)
search_word_frame.place(relx=0.5, rely=0.5, anchor='center')

# Label for App Title
app_name_label = ctk.CTkLabel(search_word_frame, text="R-Dictionary", font=("Arial bold", 50), fg_color="transparent")
app_name_label.pack(padx=40, pady=40)

# Input Entry to enter words
word_entry = ctk.CTkEntry(search_word_frame, placeholder_text="Enter the word ...")
word_entry.configure(width=300, height=30)
word_entry.pack(padx=40)

button_search = ctk.CTkButton(search_word_frame, text="Search", command=search_word_api)
button_search.pack(pady=40)

# Loading ProgressBar
progressbar = ctk.CTkProgressBar(root, orientation="horizontal")
progressbar.start()
progressbar.configure(mode="indeterminate")
#progressbar.pack(pady=30)

result_frame = AnimFrame2(root, width=300, height=600, fg_color="transparent")
#result_frame.place(relx=0.5, rely=0.5, anchor='center', relheight=1)

data_tabs = ctk.CTkTabview(master=result_frame)
data_tabs.configure(width=700, height=600)
data_tabs.pack(pady=20)

data_tabs.add("Definition")  # add tab at the end
data_tabs.add("Pronunciation")  # add tab at the end
data_tabs.add("Examples")  # add tab at the end
data_tabs.set("Definition")  # set currently visible tab

# Bind enter' to start the process
root.bind('<Return>', search_word_api)

root.mainloop()