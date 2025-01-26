import time
import hashlib
import customtkinter as ctk
from tkinter import messagebox

# Thiết lập giao diện toàn cục
ctk.set_appearance_mode("System")  # Giao diện sáng/tối dựa trên hệ điều hành
ctk.set_default_color_theme("blue")  # Chủ đề màu xanh Fluent

# Các hàm mã hóa và giải mã
def generate_dynamic_key(secret_key, context_factor):
    combined = f"{secret_key}{context_factor}"
    dynamic_key = hashlib.sha256(combined.encode("utf-8")).hexdigest()
    return dynamic_key


def chaos_encrypt(char, key, index, context):
    chaotic_value = (index * 7 + context) % 256
    key_value = ord(key[index % len(key)])
    return chr((ord(char) + key_value + chaotic_value) % 256)


def chaos_decrypt(char, key, index, context):
    chaotic_value = (index * 7 + context) % 256
    key_value = ord(key[index % len(key)])
    return chr((ord(char) - key_value - chaotic_value + 256) % 256)


def advanced_encrypt(message, secret_key):
    context_factor = int(time.time()) % 1000
    dynamic_key = generate_dynamic_key(secret_key, context_factor)

    encrypted_message = []
    for i, char in enumerate(message):
        encrypted_char = chaos_encrypt(char, dynamic_key, i, context_factor)
        encrypted_message.append(encrypted_char)

    return ''.join(encrypted_message), context_factor


def advanced_decrypt(encrypted_message, secret_key, context_factor):
    dynamic_key = generate_dynamic_key(secret_key, context_factor)

    decrypted_message = []
    for i, char in enumerate(encrypted_message):
        decrypted_char = chaos_decrypt(char, dynamic_key, i, context_factor)
        decrypted_message.append(decrypted_char)

    return ''.join(decrypted_message)

# Lớp giao diện chính
class CipherApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("CipherX beta")
        self.geometry("700x500")
        self.resizable(False, False)

        # Khung tiêu đề
        self.header_frame = ctk.CTkFrame(self, corner_radius=10)
        self.header_frame.pack(pady=10, padx=10, fill="x")
        self.title_label = ctk.CTkLabel(self.header_frame, text="Mã hóa Văn bản", font=("Arial", 24, "bold"))
        self.title_label.pack(pady=10)

        # Khung nhập liệu
        self.input_frame = ctk.CTkFrame(self, corner_radius=10)
        self.input_frame.pack(pady=10, padx=10, fill="both", expand=True)

        self.message_label = ctk.CTkLabel(self.input_frame, text="Nhập Văn Bản:")
        self.message_label.grid(row=0, column=0, pady=10, padx=10, sticky="w")
        self.message_entry = ctk.CTkEntry(self.input_frame, width=400)
        self.message_entry.grid(row=0, column=1, pady=10, padx=10)

        self.secret_label = ctk.CTkLabel(self.input_frame, text="Khóa bí mật:")
        self.secret_label.grid(row=1, column=0, pady=10, padx=10, sticky="w")
        self.secret_entry = ctk.CTkEntry(self.input_frame, width=400)
        self.secret_entry.grid(row=1, column=1, pady=10, padx=10)

        self.context_label = ctk.CTkLabel(self.input_frame, text="Yếu tố ngữ cảnh (dùng khi giải mã):")
        self.context_label.grid(row=2, column=0, pady=10, padx=10, sticky="w")
        self.context_entry = ctk.CTkEntry(self.input_frame, width=400)
        self.context_entry.grid(row=2, column=1, pady=10, padx=10)

        # Nút chức năng
        self.button_frame = ctk.CTkFrame(self, corner_radius=10)
        self.button_frame.pack(pady=10, padx=10)

        self.encrypt_button = ctk.CTkButton(self.button_frame, text="Mã hóa", command=self.encrypt_message)
        self.encrypt_button.grid(row=0, column=0, padx=20, pady=10)

        self.decrypt_button = ctk.CTkButton(self.button_frame, text="Giải mã", command=self.decrypt_message)
        self.decrypt_button.grid(row=0, column=1, padx=20, pady=10)

        self.clear_button = ctk.CTkButton(self.button_frame, text="Xóa", command=self.clear_fields)
        self.clear_button.grid(row=0, column=2, padx=20, pady=10)

        # Khung kết quả
        self.result_frame = ctk.CTkFrame(self, corner_radius=10)
        self.result_frame.pack(pady=10, padx=10, fill="x")
        self.result_label = ctk.CTkLabel(self.result_frame, text="Kết quả:", font=("Arial", 16))
        self.result_label.pack(pady=10)
        self.result_text = ctk.CTkTextbox(self.result_frame, height=100)
        self.result_text.pack(padx=10, pady=10)

    def encrypt_message(self):
        message = self.message_entry.get().strip()
        secret_key = self.secret_entry.get().strip()
        if not message or not secret_key:
            messagebox.showerror("Lỗi", "Vui lòng nhập thông điệp và khóa bí mật!")
            return

        encrypted_message, context = advanced_encrypt(message, secret_key)
        self.result_text.delete("1.0", "end")
        self.result_text.insert("1.0", f"Thông điệp mã hóa: {encrypted_message}\n")
        self.result_text.insert("2.0", f"Yếu tố ngữ cảnh: {context}")

    def decrypt_message(self):
        encrypted_message = self.message_entry.get().strip()
        secret_key = self.secret_entry.get().strip()
        context = self.context_entry.get().strip()

        if not encrypted_message or not secret_key or not context:
            messagebox.showerror("Lỗi", "Vui lòng nhập đầy đủ thông điệp, khóa bí mật và yếu tố ngữ cảnh!")
            return

        try:
            context = int(context)
            decrypted_message = advanced_decrypt(encrypted_message, secret_key, context)
            self.result_text.delete("1.0", "end")
            self.result_text.insert("1.0", f"Thông điệp gốc: {decrypted_message}")
        except ValueError:
            messagebox.showerror("Lỗi", "Yếu tố ngữ cảnh phải là một số nguyên hợp lệ!")

    def clear_fields(self):
        self.message_entry.delete(0, "end")
        self.secret_entry.delete(0, "end")
        self.context_entry.delete(0, "end")
        self.result_text.delete("1.0", "end")


if __name__ == "__main__":
    app = CipherApp()
    app.mainloop()
