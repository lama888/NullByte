import tkinter as tk
from tkinter import ttk  # Import ttk for themed widgets
from tkinter.colorchooser import askcolor
from tkinter import filedialog, messagebox

def start_drawing(event):
    global is_drawing, prev_x, prev_y
    is_drawing = True
    prev_x, prev_y = event.x, event.y
    update_status("Drawing...")

def draw(event):
    global is_drawing, prev_x, prev_y
    if is_drawing:
        current_x, current_y = event.x, event.y
        line = canvas.create_line(prev_x, prev_y, current_x, current_y, fill=drawing_color, width=line_width, capstyle=tk.ROUND, smooth=True)
        lines.append(line)
        prev_x, prev_y = current_x, current_y

def stop_drawing(event):
    global is_drawing
    is_drawing = False
    update_status("")

def change_pen_color():
    global drawing_color
    color = askcolor()[1]
    if color:
        drawing_color = color
    update_status(f"Pen color changed to {drawing_color}")

def change_line_width(value):
    global line_width
    line_width = round(float(value))
    update_status(f"Line width changed to {line_width}")

def highlight_selected_text():
    try:
        text_widget.tag_add("highlight", tk.SEL_FIRST, tk.SEL_LAST)
        text_widget.tag_config("highlight", background=highlight_color)
        update_status("Text highlighted")
    except tk.TclError:
        update_status("No text selected")

def save_text():
    try:
        file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
        if file_path:
            with open(file_path, "w") as file:
                file.write(text_widget.get("1.0", tk.END))
            update_status(f"Notes saved to {file_path}")
            messagebox.showinfo("Saved", "Notes saved successfully.")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to save notes: {str(e)}")

def undo():
    if lines:
        canvas.delete(lines.pop())
    update_status("Undo last action")

def undo_with_shortcut(event):
    if event.state == 4 and event.keysym == 'z':  # event.state == 4 corresponds to Ctrl key
        undo()

def update_status_bar(event):
    cursor_position = text_widget.index(tk.INSERT)
    line, column = cursor_position.split('.')
    update_status(f"Line: {line}, Column: {column}")

def update_status(message):
    status_var.set(message)

root = tk.Tk()
root.title("Whiteboard App")
root.geometry("1200x600")  # Adjusted window size for better layout

# Frame for controls
controls_frame = tk.Frame(root, bg="#f0f0f0", bd=2, relief=tk.RIDGE)
controls_frame.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

# Frame for logo/image
photo_frame = tk.Frame(root, bg="white", bd=2, relief=tk.RIDGE)
photo_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

canvas = tk.Canvas(root, bg="white", highlightthickness=0)
canvas.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")

text_frame = tk.Frame(root)
text_frame.grid(row=1, column=1, padx=10, pady=10, sticky="nsew")

status_frame = tk.Frame(root, bd=1, relief=tk.SUNKEN)
status_frame.grid(row=2, column=0, columnspan=2, sticky="we")

status_var = tk.StringVar()
status_label = tk.Label(status_frame, textvariable=status_var, bd=1, relief=tk.SUNKEN, anchor=tk.W)
status_label.pack(fill="x")

is_drawing = False
drawing_color = "black"
highlight_color = "yellow"
line_width = 2
lines = []

# Button style with slightly smaller size
button_style = {
    "bg": "#4CAF50",
    "fg": "white",
    "activebackground": "#45a049",
    "font": ("Arial", 11, "bold"),  # Adjusted font size
    "relief": tk.FLAT,
    "bd": 1,
    "width": 12,  # Adjusted width
    "height": 1,  # Adjusted height
}

# Function buttons
color_button = tk.Button(controls_frame, text="Change Color", command=change_pen_color, **button_style)
clear_button = tk.Button(controls_frame, text="Clear Screen", command=lambda: canvas.delete("all"), **button_style)
save_text_button = tk.Button(controls_frame, text="Save Notes", command=save_text, **button_style)
undo_button = tk.Button(controls_frame, text="Undo", command=undo, **button_style)
highlight_button = tk.Button(controls_frame, text="Highlight Text", command=highlight_selected_text, **button_style)

# Line width slider with ttk
line_width_label = tk.Label(controls_frame, text="Line Width:", bg="#f0f0f0", font=("Arial", 12))
line_width_slider = ttk.Scale(controls_frame, from_=1, to=10, orient="horizontal", command=lambda val: change_line_width(val), length=200)
line_width_slider.set(line_width)

# Grid layout for buttons and slider
color_button.grid(row=0, column=0, padx=5, pady=5, sticky="ew")
clear_button.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
save_text_button.grid(row=0, column=2, padx=5, pady=5, sticky="ew")
undo_button.grid(row=0, column=3, padx=5, pady=5, sticky="ew")
highlight_button.grid(row=0, column=4, padx=5, pady=5, sticky="ew")
line_width_label.grid(row=1, column=0, padx=5, pady=5)
line_width_slider.grid(row=1, column=1, columnspan=4, padx=5, pady=5, sticky="ew")

# Load and display your logo/image
# Replace 'path_to_your_image.png' with the actual path or use a PhotoImage object if the image is within your project directory
logo_image = tk.PhotoImage(file='logo.png')
logo_label = tk.Label(photo_frame, image=logo_image, bg="white")
logo_label.pack(padx=10, pady=10)

text_widget_label = tk.Label(text_frame, text="Notes:", font=("Arial", 12))
text_widget_label.pack(side="top", anchor="w", padx=5, pady=5)
text_widget = tk.Text(text_frame, height=30, width=40, font=("Arial", 10), wrap=tk.WORD)
text_widget.pack(fill="both", expand=True, padx=5, pady=5)

canvas.bind("<Button-1>", start_drawing)
canvas.bind("<B1-Motion>", draw)
canvas.bind("<ButtonRelease-1>", stop_drawing)

text_widget.bind("<Key>", update_status_bar)
text_widget.bind("<Button-1>", update_status_bar)

# Configure column weights to make them responsive
root.grid_rowconfigure(1, weight=1)
root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=1)
root.grid_columnconfigure(2, weight=1)

root.mainloop()
