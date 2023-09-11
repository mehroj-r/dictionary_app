import customtkinter as ctk
from functions import request_word
from PIL import ImageTk, Image
from tkhtmlview import HTMLLabel

# Constant app parameters
root = ctk.CTk()
root.title("R-Dictionary App")
width= root.winfo_screenwidth()
height= root.winfo_screenheight()
root.geometry("%dx%d+%d+%d" % (800, 500, ((width - 800) // 2), ((height - 500) / 2)))
root.resizable(False, False)
ctk.set_default_color_theme("dark-blue")
ctk.set_appearance_mode("system")


## Data resources

# Image for restart button
restart_image = ctk.CTkImage(light_image=Image.open("./data/restart.png"),
                                  dark_image=Image.open("./data/restart.png"),
                                  size=(30, 30))



class AnimFrame2(ctk.CTkFrame):
	def __init__(self, parent, width, height, fg_color):
		super().__init__(master=parent, width=width, height=height, fg_color=fg_color)

		self.rel_x=0.5
		self.rel_y=-0.5

	def animate_down(self):
		self.rel_y += 0.01
		self.place(relx=self.rel_x, rely=self.rel_y, anchor='center', relheight=1)
		if self.rel_y < 0.5:
			self.after(1, self.animate_down)

	def animate_back_up(self):
		self.rel_y -= 0.01
		self.place(relx=self.rel_x, rely=self.rel_y, anchor='center', relheight=1)
		if self.rel_y > -0.5:
			self.after(1, self.animate_back_up)
		else:
			search_word_frame.animate_back_down()




class AnimFrame1(ctk.CTkFrame):
	def __init__(self, parent, width, height):
		super().__init__(master=parent, width=width, height=height)

		self.rel_x=0.5
		self.rel_y=0.5

	def animate_up(self):
		self.rel_y -= 0.01
		self.place(relx=self.rel_x, rely=self.rel_y)
		if self.rel_y > -0.5:
			self.after(1, self.animate_up)
		else:
			result_frame.animate_down()

	def animate_back_down(self):
		self.rel_y += 0.01
		self.place(relx=self.rel_x, rely=self.rel_y)
		if self.rel_y < 0.5:
			self.after(1, self.animate_back_down)





# Function to start the process
def search_word_api(*x):
	entry_input = word_entry.get()
	if entry_input:
		# Receive API response
		response = request_word(entry_input.lower())

		# HTML render for response visualization
		html_view.set_html(response)

		# Show animation between Input and Response frames
		search_word_frame.animate_up()	

		# Passing new word as title for result_frame
		current_searched_word.configure(text = entry_input)

# Function to restart the process
def back_to_new_word():

	# Initializing animation
	result_frame.animate_back_up()

	# Clearing input entry
	word_entry.delete(0, 999)




## Frame for text input

search_word_frame = AnimFrame1(root, width=200, height=200)
search_word_frame.place(relx=0.5, rely=0.5, anchor='center')

# Label for App Title
app_name_label = ctk.CTkLabel(search_word_frame, text="R-Dictionary", font=("Arial bold", 50), fg_color="transparent")
app_name_label.pack(padx=40, pady=40)

# Input Entry to enter words
word_entry = ctk.CTkEntry(search_word_frame, placeholder_text="Enter the word ...", width=300, height=30)
word_entry.pack(padx=40)

# Button to start the process
button_search = ctk.CTkButton(search_word_frame, text="Search", command=search_word_api)
button_search.pack(pady=40)

# Loading ProgressBar
progressbar = ctk.CTkProgressBar(root, orientation="horizontal", mode="indeterminate")
progressbar.start()
#progressbar.pack(pady=30)




## Frame for response visualization

result_frame = AnimFrame2(root, width=800, height=700, fg_color="transparent")

# Button to go back to search a new word
new_word_btn = ctk.CTkButton(result_frame, text="", image=restart_image, command=back_to_new_word, width=30, height=30, hover=False)
new_word_btn.place(relx=0.9, rely=0.08, anchor='center')

# Label to show the word that is in process
current_searched_word = ctk.CTkLabel(result_frame, text="", font=("Arial bold", 50))
current_searched_word.place(relx=0.5, rely=0.08, anchor='center')



## Frame with scrolling to display the data

data_frame = ctk.CTkScrollableFrame(master=result_frame, width=700, height=400)
data_frame.place(relx=0.5, rely=0.55, anchor='center')

html_view = HTMLLabel(data_frame, html="", background="#212121")
html_view.pack(pady=20, padx=20)

# Bind 'enter' to start the process
root.bind('<Return>', search_word_api)

root.mainloop()