import tkinter as tk
from tkinter import messagebox
import json
import os

# File to store contacts
CONTACTS_FILE = 'contacts.json'

# Load contacts from file or create an empty list
def load_contacts():
    if os.path.exists(CONTACTS_FILE):
        with open(CONTACTS_FILE, 'r') as file:
            return json.load(file)
    return []

# Save contacts to file
def save_contacts(contacts):
    with open(CONTACTS_FILE, 'w') as file:
        json.dump(contacts, file, indent=4)

# Add new contact function
def add_contact():
    name = name_var.get()
    phone = phone_var.get()
    email = email_var.get()

    if not name or not phone or not email:
        messagebox.showwarning("Input Error", "All fields are required!")
        return

    contacts.append({
        'name': name,
        'phone': phone,
        'email': email
    })
    save_contacts(contacts)
    messagebox.showinfo("Success", f"Contact {name} added successfully!")
    clear_inputs()
    refresh_contact_list()

# Clear input fields
def clear_inputs():
    name_var.set('')
    phone_var.set('')
    email_var.set('')

# Delete selected contact
def delete_contact():
    selected_contact = contact_listbox.curselection()
    if not selected_contact:
        messagebox.showwarning("Selection Error", "No contact selected!")
        return
    
    contact_index = selected_contact[0]
    deleted_contact = contacts.pop(contact_index)
    save_contacts(contacts)
    messagebox.showinfo("Success", f"Contact {deleted_contact['name']} deleted successfully!")
    refresh_contact_list()

# Edit selected contact
def edit_contact():
    selected_contact = contact_listbox.curselection()
    if not selected_contact:
        messagebox.showwarning("Selection Error", "No contact selected!")
        return
    
    contact_index = selected_contact[0]
    contact = contacts[contact_index]

    name_var.set(contact['name'])
    phone_var.set(contact['phone'])
    email_var.set(contact['email'])

    def update_contact():
        contact['name'] = name_var.get()
        contact['phone'] = phone_var.get()
        contact['email'] = email_var.get()
        save_contacts(contacts)
        messagebox.showinfo("Success", f"Contact {contact['name']} updated successfully!")
        clear_inputs()
        refresh_contact_list()
        update_button.destroy()

    update_button = tk.Button(root, text="Update Contact", command=update_contact)
    update_button.pack()

# Refresh contact list
def refresh_contact_list():
    contact_listbox.delete(0, tk.END)
    for contact in contacts:
        contact_listbox.insert(tk.END, f"{contact['name']} - {contact['phone']} - {contact['email']}")

# Initialize contacts
contacts = load_contacts()

# Create main application window
root = tk.Tk()
root.title("Contact Manager")

# Variables to hold user inputs
name_var = tk.StringVar()
phone_var = tk.StringVar()
email_var = tk.StringVar()

# UI Layout
tk.Label(root, text="Name:").pack()
tk.Entry(root, textvariable=name_var).pack()

tk.Label(root, text="Phone:").pack()
tk.Entry(root, textvariable=phone_var).pack()

tk.Label(root, text="Email:").pack()
tk.Entry(root, textvariable=email_var).pack()

tk.Button(root, text="Add Contact", command=add_contact).pack()
tk.Button(root, text="Delete Contact", command=delete_contact).pack()
tk.Button(root, text="Edit Contact", command=edit_contact).pack()

# Contact list
contact_listbox = tk.Listbox(root)
contact_listbox.pack(fill=tk.BOTH, expand=True)

# Populate contact list on startup
refresh_contact_list()

# Run the main loop
root.mainloop()
