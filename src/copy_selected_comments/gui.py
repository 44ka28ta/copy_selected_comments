
#!/usr/bin/env python3

import tkinter as tk
from tkinter import filedialog, messagebox
import pyperclip
import time
import pyautogui
from pathlib import Path
import os


class ClipboardSelector:

	def __init__(self, root):
		self.root = root
		self.root.title("Clipboard Item Selector")
		self.root.geometry("600x500")
		self.root.bind("<Control-c>", self.copy_selected)
		self.root.bind("<Control-C>", self.copy_selected)

		self.root.bind("<F5>", lambda e: self.reload_file())

		self.items = []
		self.variables = []
		self.current_file = None

		self.PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent

		self.create_widgets()

	def create_widgets(self):

		# Top area
		top_frame = tk.Frame(self.root)
		top_frame.pack(fill="x", padx=10, pady=5)

		tk.Button( top_frame, text="Open Text File", command=self.load_file).pack(side="left")

		tk.Button(top_frame, text="Reload", command=self.reload_file ).pack(side="left", padx=5)

		self.file_label = tk.Label( top_frame, text="No file loaded", anchor="w")
		self.file_label.pack(side="left", padx=10)

		# Action buttons
		action_frame = tk.Frame(self.root)
		action_frame.pack(fill="x", padx=10, pady=5)

		tk.Button(action_frame, text="Select All", command=self.select_all).pack(side="left", padx=2)

		tk.Button( action_frame, text="Clear All", command=self.clear_all).pack(side="left", padx=2)

		tk.Button( action_frame, text="Copy Selected (Ctrl+C)", command=self.copy_selected).pack(side="left", padx=20)

		# Scrollable checkbox area
		container = tk.Frame(self.root)
		container.pack(fill="both", expand=True, padx=10, pady=10)

		self.canvas = tk.Canvas(container)
		scrollbar = tk.Scrollbar( container, orient="vertical", command=self.canvas.yview)

		self.checkbox_frame = tk.Frame(self.canvas)

		self.checkbox_frame.bind( "<Configure>", lambda e: self.canvas.configure( scrollregion=self.canvas.bbox("all")))

		self.canvas.create_window( (0, 0), window=self.checkbox_frame, anchor="nw")

		self.canvas.configure( yscrollcommand=scrollbar.set)
		self.canvas.pack( side="left", fill="both", expand=True)

		scrollbar.pack( side="right", fill="y")

		self.status_label = tk.Label( self.root, text="Ready")
		self.status_label.pack(fill="x", pady=5)


        # Mouse wheel support
		self.canvas.bind_all("<MouseWheel>", self.on_mousewheel)      # Windows


		self.canvas.bind( "<Enter>", lambda e: self.canvas.focus_set())
		self.canvas.bind_all("<Button-4>", self.on_mousewheel_linux)  # Linux scroll up
		self.canvas.bind_all("<Button-5>", self.on_mousewheel_linux)  # Linux scroll down

		tk.Button(action_frame, text="Send To Teams", command=self.send_to_teams).pack(side="left", padx=5)

	def load_file_contents(self, filename):

		with open(filename, "r", encoding="utf-8") as f:
			items = [ line.strip() for line in f if line.strip() and not line.strip().startswith("#") ]

		self.populate_items(items)

		self.file_label.config( text=f"Loaded: {filename}")

		self.status_label.config( text=f"{len(items)} items loaded")

	def load_file(self):

		filename = filedialog.askopenfilename( title="Select Text File", filetypes=[ ("Text Files", "*.txt"), ("All Files", "*.*") ])

		if not filename:
			return

		try:
			self.current_file = filename
			self.load_file_contents(filename)

		except Exception as e:
			messagebox.showerror( "Error", f"Failed to load file:\n{e}")

	def populate_items(self, items):

		for widget in self.checkbox_frame.winfo_children():
			widget.destroy()

		self.items = items
		self.variables = []

		for item in items:
			var = tk.BooleanVar()

			chk = tk.Checkbutton( self.checkbox_frame, text=item, variable=var, anchor="w", justify="left")

			chk.pack( fill="x", anchor="w")

			self.variables.append(var)

	def reload_file(self):

		if not self.current_file:
			messagebox.showwarning( "Warning", "No file loaded.")
			return

		try:
			self.load_file_contents( self.current_file)

			self.status_label.config( text="File reloaded")

		except Exception as e:
			messagebox.showerror( "Error", f"Failed to reload file:\n{e}")

	def select_all(self):

		for var in self.variables:
			var.set(True)

		self.status_label.config( text="All items selected")

	def clear_all(self):

		for var in self.variables:
			var.set(False)

		self.status_label.config( text="Selection cleared")

	def copy_selected(self, event=None):

		selected_items = [ item for item, var in zip( self.items, self.variables) if var.get() ]

		if not selected_items:
			messagebox.showwarning( "Warning", "Please select at least one item.")
			return

		pyperclip.copy( "\n".join(selected_items))

		self.status_label.config( text=f"Copied {len(selected_items)} items to clipboard")

	def on_mousewheel(self, event):
		self.canvas.yview_scroll( int(-1 * (event.delta / 120)), "units")


	def on_mousewheel_linux(self, event):
		if event.num == 4:
			self.canvas.yview_scroll(-1, "units")
		elif event.num == 5:
			self.canvas.yview_scroll(1, "units")


	def send_to_teams(self):

		selected_items = [ item for item, var in zip( self.items, self.variables) if var.get() ]

		if not selected_items:
			messagebox.showwarning( "Warning", "Please select at least one item.")
			return

		feedback = "\n".join(selected_items)

		pyperclip.copy(feedback)

		self.status_label.config( text="Switch to Teams...")

		# Give user time to activate Teams
		self.root.after(100, lambda: self.perform_teams_actions())


	def perform_teams_actions(self):

		# Switch to Teams manually before calling if desired
		time.sleep(0.5)

		# Paste feedback
		pyautogui.hotkey("ctrl", "v")

		time.sleep(0.5)

		# Move to next field or button
		location = pyautogui.locateCenterOnScreen(os.path.join(self.PROJECT_ROOT, "img", "next_student.png"), confidence=0.9)

		if location:
			pyautogui.click(location)

		time.sleep(0.2)

		# Activate Next Student button
		pyautogui.press("enter")

		self.status_label.config( text="Feedback pasted and next student selected")



def main():

	root = tk.Tk()

	app = ClipboardSelector(root)

	root.mainloop()


if __name__ == "__main__":
	main()

