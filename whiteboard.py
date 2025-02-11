
import tkinter as tk
from tkinter import ttk  # for themed widgets
from tkinter.colorchooser import askcolor
from tkinter import filedialog, messagebox

#Create the main application window
window = tk.Tk()     
window.title("Whiteboard App")  #set the title of the window
window.geometry("1200x600")    # set the initial size of the window


#function to begin drawing when the mouse button is pressed
def begin_drawing(event): 
    global is_drawing, prev_x, prev_y
    is_drawing = True
    prev_x, prev_y = event.x, event.y
    
#Function to drw line as th mouse id dragged
def draw(event):
    global is_drawing, prev_x, prev_y
    if is_drawing:
        current_x, current_y = event.x, event.y
        line = canvas.create_line(prev_x, prev_y, current_x, current_y, fill=drawing_color, width=line_width, capstyle=tk.ROUND, smooth=True)
        lines.append(line)
        prev_x, prev_y = current_x, current_y


#Function to stop drawing when the mouse button is released
def stop_drawing(event):
    global is_drawing
    is_drawing = False
    

#Function for Opening a color chooser dialog and changing the pen color
def change_pen_color(): 
    global drawing_color
    color = askcolor()[1] #Ask the user to select a color and get the color code
    if color:
        drawing_color = color
    update_status(f"Pen color changed to {drawing_color}")


#Function for Changing the width of the drawing line based on the slider value.
def change_line_width(value): 
    global line_width
    line_width = round(float(value)) 
    update_status(f"Line width changed to {line_width}")


#Hightlight text FUnction
def highlight_selected_text(): 
    try:
        text_widget.tag_add("highlight", tk.SEL_FIRST, tk.SEL_LAST)
        text_widget.tag_config("highlight", background=highlight_color)
        update_status("Text highlighted")
    except tk.TclError:
        update_status("No text selected")


#Function to save the text in the text widget to a file
def save_to_text(): 
    try:
        file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
        if file_path:
            with open(file_path, "w") as file:
                file.write(text_widget.get("1.0", "end-1c"))
            update_status(f"Notes saved to {file_path}")
            messagebox.showinfo("Saved", "File saved successfully.")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to save notes: {str(e)}")


#Function to remove the last drawn line from the canvas
def undo(): 
    if lines:
        canvas.delete(lines.pop())
    update_status("Undo last action")

#Function to update the status bar with a message
def update_status(message): 
    status_var.set(message)


# Create a frame to hold control buttons
controls_frame = tk.Frame(window, bg="#f0f0f0", bd=2, relief=tk.RIDGE)
controls_frame.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

# Create a frame to display a logo or photo
photo_frame = tk.Frame(window, bg="white", bd=2, relief=tk.RIDGE)
photo_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

# Create the drawing area (canvas)
canvas = tk.Canvas(window, bg="white", highlightthickness=0)
canvas.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")

# Create a frame for text input and display
text_frame = tk.Frame(window)
text_frame.grid(row=1, column=1, padx=10, pady=10, sticky="nsew")

# Create a frame for the status bar at the bottom
status_frame = tk.Frame(window, bd=1, relief=tk.SUNKEN)
status_frame.grid(row=2, column=0, columnspan=2, sticky="we")

# Create a label to display status messages
status_var = tk.StringVar()
status_label = tk.Label(status_frame, textvariable=status_var, bd=1, relief=tk.SUNKEN, anchor=tk.W)
status_label.pack(fill="x")


# Initialize variables for drawing and text
is_drawing = False #it indicates if drawing is active or not
drawing_color = "black" #current pen colour
highlight_color = "yellow" #hightlight color for text
line_width = 2 #width of drawing line
lines = []  # List to store drawn lines

# Style dictionary for buttons
button_style = {
    "bg": "green",
    "fg": "white",
    "activebackground": "#45a049",
    "font": ("Arial", 11, "bold"),  # Adjust font size here.
    "relief": tk.FLAT,
    "bd": 1,
    "cursor": "hand2", #change cursor when hovering to buttons
    "width": 12,  # Adjust width here.
    "height": 1,  # Adjust height here.
    
}

# Function buttons
color_button = tk.Button(controls_frame, text="Choose Color", command=change_pen_color, **button_style)
clear_button = tk.Button(controls_frame, text="Clear Board", command=lambda: canvas.delete("all"), **button_style)
save_text_button = tk.Button(controls_frame, text="Save Text", command=save_to_text, **button_style)
undo_button = tk.Button(controls_frame, text="Undo", command=undo, **button_style)
highlight_button = tk.Button(controls_frame, text="Highlight Text", command=highlight_selected_text, **button_style)

# Line width slider (ttk)
line_width_label = tk.Label(controls_frame, text="Line Size:", bg="#f0f0f0", font=("Arial", 12))
line_width_slider = ttk.Scale(controls_frame, from_=1, to=10, orient="horizontal", command=lambda val: change_line_width(val), length=200)
line_width_slider.set(line_width)

# Grid layout for buttons and slider
color_button.grid(row=0, column=0, pady=5, padx=5, sticky="ew")
clear_button.grid(row=0, column=1, pady=5, padx=5, sticky="ew")
save_text_button.grid(row=0, column=2, pady=5, padx=5, sticky="ew")
undo_button.grid(row=0, column=3, padx=5, pady=5, sticky="ew")
highlight_button.grid(row=0, column=4, pady=5, padx=5, sticky="ew")
line_width_label.grid(row=1, column=0, pady=5, padx=5)
line_width_slider.grid(row=1, column=1, columnspan=4, pady=5, padx=5, sticky="ew")

# Load and display a logo or photo in the photo frame
logo_image = tk.PhotoImage(file='logo.png') #For Nullbyte Photo.
logo_label = tk.Label(photo_frame, image=logo_image, bg="white")
logo_label.pack(pady=10, padx=10)

# Create a label and text widget for notes input and display
text_widget_label = tk.Label(text_frame, text="Notes:", font=("Arial", 12))
text_widget_label.pack(side="top", anchor="w", padx=5, pady=5)
text_widget = tk.Text(text_frame, height=30, width=40, font=("Arial", 10), wrap=tk.WORD)
text_widget.pack(fill="both", expand=True, pady=5, padx=5)


# Bind mouse events to drawing functions on the canvas
canvas.bind("<Button-1>", begin_drawing)
canvas.bind("<B1-Motion>", draw)
canvas.bind("<ButtonRelease-1>", stop_drawing)
canvas.config(cursor="cross") # Change cursor appearance when hovering over the canvas


# Make the window responsive using row and column weights
window.grid_rowconfigure(1, weight=1)
window.grid_columnconfigure(0, weight=1)
window.grid_columnconfigure(1, weight=1)

# Start the main event loop
window.mainloop()
