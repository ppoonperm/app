# main.py
import kivy
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.screenmanager import ScreenManager, Screen
from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.textfield import MDTextField
from kivymd.uix.card import MDCard
from kivymd.uix.boxlayout import MDBoxLayout

import sqlite3
import pandas as pd
from datetime import datetime, date
import json
import os

# ใช้โค้ดเดิมจาก app.py แต่ปรับเป็น Kivy UI
class LoginScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = 'login'
        
        layout = MDBoxLayout(orientation='vertical', padding=20, spacing=20)
        
        # Title
        title = Label(text='💰 Personal Financial App', font_size='24sp')
        layout.add_widget(title)
        
        # Username input
        self.username_input = MDTextField(
            hint_text="ชื่อผู้ใช้",
            mode="rectangle"
        )
        layout.add_widget(self.username_input)
        
        # Password input
        self.password_input = MDTextField(
            hint_text="รหัสผ่าน",
            password=True,
            mode="rectangle"
        )
        layout.add_widget(self.password_input)
        
        # Login button
        login_btn = MDRaisedButton(
            text="เข้าสู่ระบบ",
            on_release=self.login
        )
        layout.add_widget(login_btn)
        
        # Register button
        register_btn = MDRaisedButton(
            text="สมัครสมาชิก",
            on_release=self.go_to_register
        )
        layout.add_widget(register_btn)
        
        self.add_widget(layout)
    
    def login(self, instance):
        # ใช้ function authentication จากโค้ดเดิม
        username = self.username_input.text
        password = self.password_input.text
        
        if authenticate_user(username, password):
            app = App.get_running_app()
            app.root.current = 'dashboard'
        else:
            # แสดง error message
            pass
    
    def go_to_register(self, instance):
        app = App.get_running_app()
        app.root.current = 'register'

class DashboardScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = 'dashboard'
        
        layout = MDBoxLayout(orientation='vertical', padding=20, spacing=20)
        
        # Title
        title = Label(text='📊 Dashboard', font_size='20sp')
        layout.add_widget(title)
        
        # Balance display
        self.balance_label = Label(text='ยอดคงเหลือ: ฿0.00', font_size='18sp')
        layout.add_widget(self.balance_label)
        
        # Navigation buttons
        transaction_btn = MDRaisedButton(
            text="💳 รายการธุรกรรม",
            on_release=self.go_to_transactions
        )
        layout.add_widget(transaction_btn)
        
        stock_btn = MDRaisedButton(
            text="📈 Stock Tracker",
            on_release=self.go_to_stocks
        )
        layout.add_widget(stock_btn)
        
        self.add_widget(layout)
        
    def on_enter(self):
        # อัพเดทยอดเงินเมื่อเข้าหน้า
        self.update_balance()
    
    def update_balance(self):
        # ใช้ function calculate_balance จากโค้ดเดิม
        balance, income, expense = calculate_balance(1)  # user_id = 1 for demo
        self.balance_label.text = f'ยอดคงเหลือ: ฿{balance:,.2f}'
    
    def go_to_transactions(self, instance):
        app = App.get_running_app()
        app.root.current = 'transactions'
    
    def go_to_stocks(self, instance):
        app = App.get_running_app()
        app.root.current = 'stocks'

class FinancialApp(MDApp):
    def build(self):
        # สร้าง ScreenManager
        sm = ScreenManager()
        
        # เพิ่ม screens
        sm.add_widget(LoginScreen())
        sm.add_widget(DashboardScreen())
        # เพิ่ม screens อื่นๆ ตามต้องการ
        
        return sm

# เพิ่ม functions จากโค้ดเดิม
def init_database():
    # คัดลอกจากโค้ดเดิม
    pass

def authenticate_user(username, password):
    # คัดลอกจากโค้ดเดิม
    pass

def calculate_balance(user_id):
    # คัดลอกจากโค้ดเดิม
    pass

if __name__ == '__main__':
    FinancialApp().run()