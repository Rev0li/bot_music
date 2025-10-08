#!/usr/bin/env python3
"""
Test simple de l'interface moderne
"""

import customtkinter as ctk
import sys
import os

# Configuration CustomTkinter
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

class SimpleModernApp:
    def __init__(self):
        self.root = ctk.CTk()
        self.root.title("Music Organizer Pro - Test")
        self.root.geometry("800x600")
        
        self.create_interface()
    
    def create_interface(self):
        # Titre
        title = ctk.CTkLabel(
            self.root,
            text="Music Organizer Pro - Modern Edition",
            font=ctk.CTkFont(size=20, weight="bold")
        )
        title.pack(pady=20)
        
        # Frame principal
        main_frame = ctk.CTkFrame(self.root)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Boutons de test
        btn_frame = ctk.CTkFrame(main_frame)
        btn_frame.pack(pady=20)
        
        # Bouton simple
        btn1 = ctk.CTkButton(
            btn_frame,
            text="Test Button",
            command=self.test_click
        )
        btn1.pack(side="left", padx=10)
        
        # Toggle button simple
        self.toggle_state = False
        self.toggle_btn = ctk.CTkButton(
            btn_frame,
            text="[OFF] Toggle",
            command=self.toggle_click,
            fg_color="#f44336"
        )
        self.toggle_btn.pack(side="left", padx=10)
        
        # Zone de logs
        self.log_text = ctk.CTkTextbox(
            main_frame,
            height=300,
            font=ctk.CTkFont(family="Consolas", size=10)
        )
        self.log_text.pack(fill="both", expand=True, padx=20, pady=20)
        
        self.log("Interface moderne chargee avec succes!")
    
    def test_click(self):
        self.log("Bouton test clique!")
    
    def toggle_click(self):
        self.toggle_state = not self.toggle_state
        
        if self.toggle_state:
            self.toggle_btn.configure(
                text="[ON] Toggle",
                fg_color="#4CAF50"
            )
        else:
            self.toggle_btn.configure(
                text="[OFF] Toggle", 
                fg_color="#f44336"
            )
        
        self.log(f"Toggle: {'ON' if self.toggle_state else 'OFF'}")
    
    def log(self, message):
        self.log_text.insert("end", f"{message}\n")
        self.log_text.see("end")
    
    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    print("Test de l'interface moderne...")
    app = SimpleModernApp()
    app.run()
