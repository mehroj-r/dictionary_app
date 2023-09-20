import customtkinter as ctk
from functions import request_word
from PIL import ImageTk, Image
from tkhtmlview import HTMLLabel
from ctypes import windll
import darkdetect



# Constant app parameters
windll.shcore.SetProcessDpiAwareness(1)
root = ctk.CTk(fg_color=("white", "#141414"))
root.title("R-Dictionary App")
width= root.winfo_screenwidth()
height= root.winfo_screenheight()
root.geometry("%dx%d+%d+%d" % (800, 500, ((width - 800) // 2), ((height - 500) / 2)))
root.minsize(800, 500)
ctk.set_default_color_theme("./data/custom-r.json")


if darkdetect.theme() == "Light":
	ctk.set_appearance_mode("light")
else:
	ctk.set_appearance_mode("dark")

## Data resources

# Image for restart button
restart_image = ctk.CTkImage(light_image=Image.open("./data/restart.png"), dark_image=Image.open("./data/restart.png"), size=(30, 30))



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

class AnimErrorFrame(ctk.CTkFrame):
	def __init__(self, parent, width, height, border_width, border_color):
		super().__init__(master=parent, width=width, height=height, border_color=border_color, border_width=border_width)

		self.rel_x=0.85
		self.rel_y=-0.08
		self.status="inactive"

	def animate(self):
		self.rel_y += 0.001
		self.place(relx=self.rel_x, rely=self.rel_y, anchor='center')
		if self.rel_y < 0.08:
			self.after(1, self.animate)
		else:
			self.status = "active"
			self.after(3000, self.animate_back)

	def animate_back(self):
		self.rel_y -= 0.001
		self.place(relx=self.rel_x, rely=self.rel_y, anchor='center')
		if self.rel_y > -0.08:
			self.after(1, self.animate_back)
		else:
			self.status="inactive"



# Function to start the process
def search_word_api(*x):

	# HTML label to display API response (Follows light/dark theme)
	if darkdetect.theme() == "Light":
		html_view = HTMLLabel(data_frame, html="", background="#E5E5E5")
		html_view.pack(pady=20, padx=20)
	else:
		html_view = HTMLLabel(data_frame, html="", background="#191919")
		html_view.pack(pady=20, padx=20)

	# Load entry value to perform operations with it
	entry_input = word_entry.get().lower()

	if entry_input:

		# Receive API response
		response = request_word(entry_input)

		# Check if request was successful
		if response != False:

			# Return the error popup
			if error_popup.status != "inactive":
				error_popup.animate_back()

			# HTML render for response visualization
			if darkdetect.theme() == "Light":
				html_view.set_html(response[0])
			else:
				html_view.set_html(response[1])

			# Show animation between Input and Response frames
			search_word_frame.animate_up()	

			# Passing new word as title for result_frame
			current_searched_word.configure(text = entry_input)

			# Bind 'espace' to comeback to input menu
			root.bind('<Escape>', back_to_new_word)

			# Unbind unnessary key
			root.bind('<Return>')
		else:
			# Activate error popup
			if error_popup.status != "active":
				error_popup.animate()


# Function to restart the process
def back_to_new_word(*x):

	# Initializing animation
	result_frame.animate_back_up()

	# Clearing input entry
	word_entry.delete(0, 999)

	# Bind 'enter' to start the request
	root.bind('<Return>', search_word_api)

	# Unbind unnessary key
	root.unbind('<Escape>')



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

# Error pop-up to alert the response was not 200
error_popup = AnimErrorFrame(root, width = 200, height = 50, border_width=2, border_color="#f77c74")

# Label for Error
error_label = ctk.CTkLabel(error_popup, text="The word was not found", fg_color="transparent")
error_label.place(relx=0.5, rely=0.5, anchor='center')

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


# Bind 'enter' to start the process
root.bind('<Return>', search_word_api)

root.mainloop()