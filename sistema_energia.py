import tkinter as tk
from tkinter import messagebox, simpledialog
import mysql.connector
import matplotlib.pyplot as plt
import tkinter.font as tkFont
import csv

# Função para conectar ao banco de dados MySQL
def connect_to_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",        # Coloque o seu usuário do MySQL
        password="",        # Coloque a sua senha do MySQL
        database="sistema_energia"  # Nome do seu banco de dados
    )

# Classe principal da aplicação
class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema ODS 7 - Energia Limpa e Acessível")
        self.root.geometry("500x400")
        self.root.configure(bg="#f0f0f0")  # Cor de fundo suave

        # Definindo uma fonte moderna
        self.font_style = tkFont.Font(family="Helvetica", size=12)

        # Conectar ao banco de dados
        self.db = connect_to_db()
        self.cursor = self.db.cursor()

        # Tela de Login
        self.create_login_screen()

    def create_login_screen(self):
        self.clear_window()

        tk.Label(self.root, text="Usuário", bg="#f0f0f0", font=self.font_style).pack(pady=10)
        self.user_entry = tk.Entry(self.root, font=self.font_style)
        self.user_entry.pack(pady=5)

        tk.Label(self.root, text="Senha", bg="#f0f0f0", font=self.font_style).pack(pady=10)
        self.pass_entry = tk.Entry(self.root, show="*", font=self.font_style)
        self.pass_entry.pack(pady=5)

        tk.Button(self.root, text="Login", command=self.verify_login, bg="#4CAF50", fg="white", font=self.font_style).pack(pady=10)
        tk.Button(self.root, text="Criar Usuário", command=self.create_user_screen, bg="#2196F3", fg="white", font=self.font_style).pack(pady=5)

    def verify_login(self):
        user = self.user_entry.get()
        password = self.pass_entry.get()

        query = "SELECT * FROM usuarios WHERE username=%s AND password=%s"  # Referenciando a tabela 'usuarios'
        self.cursor.execute(query, (user, password))
        result = self.cursor.fetchone()

        if result:
            messagebox.showinfo("Login", "Bem-vindo ao Sistema!")
            self.create_main_window()
        else:
            messagebox.showerror("Erro", "Usuário ou senha incorretos!")

    def create_main_window(self):
        self.clear_window()

        tk.Label(self.root, text="Bem-vindo ao Sistema de Energia Limpa!", bg="#f0f0f0", font=self.font_style).pack(pady=20)
        tk.Button(self.root, text="Gerenciamento de Energia", command=self.energy_management, bg="#4CAF50", fg="white", font=self.font_style).pack(pady=10)
        tk.Button(self.root, text="Monitoramento de Consumo", command=self.energy_monitor, bg="#2196F3", fg="white", font=self.font_style).pack(pady=10)
        tk.Button(self.root, text="Sair", command=self.root.quit, bg="#f44336", fg="white", font=self.font_style).pack(pady=10)

    def energy_management(self):
        self.clear_window()

        tk.Label(self.root, text="Gerenciamento de Energia", bg="#f0f0f0", font=self.font_style).pack(pady=10)
        tk.Label(self.root, text="Insira os dados para o gerenciamento:", bg="#f0f0f0", font=self.font_style).pack(pady=5)

        self.data_entry = tk.Entry(self.root, width=40, font=self.font_style)
        self.data_entry.pack(pady=5)

        tk.Button(self.root, text="Salvar Dados", command=self.save_energy_data, bg="#4CAF50", fg="white", font=self.font_style).pack(pady=10)
        tk.Button(self.root, text="Atualizar Dados", command=self.update_energy_data, bg="#FFC107", fg="black", font=self.font_style).pack(pady=5)
        tk.Button(self.root, text="Deletar Dados", command=self.delete_energy_data, bg="#FF5722", fg="white", font=self.font_style).pack(pady=5)
        tk.Button(self.root, text="Voltar", command=self.create_main_window, bg="#2196F3", fg="white", font=self.font_style).pack(pady=10)

    def save_energy_data(self):
        data = self.data_entry.get()

        if data:  # Verifica se o campo não está vazio
            try:
                query = "INSERT INTO gerenciamento_energia (descricao) VALUES (%s)"
                self.cursor.execute(query, (data,))
                self.db.commit()

                messagebox.showinfo("Sucesso", f"Dados de Gerenciamento de Energia '{data}' salvos com sucesso!")
                self.data_entry.delete(0, tk.END)  # Limpa o campo de entrada após salvar
            except mysql.connector.Error as err:
                messagebox.showerror("Erro", f"Erro ao salvar os dados: {err}")
        else:
            messagebox.showerror("Erro", "Por favor, insira uma descrição.")

    def update_energy_data(self):
        # Perguntar ao usuário qual ID ele deseja atualizar
        id_to_update = simpledialog.askinteger("Atualizar Dados", "Insira o ID do registro a ser atualizado:")
        if id_to_update is not None:
            # Pedir a nova descrição
            new_description = simpledialog.askstring("Atualizar Dados", "Insira a nova descrição:")
            if new_description:
                try:
                    query = "UPDATE gerenciamento_energia SET descricao=%s WHERE id=%s"
                    self.cursor.execute(query, (new_description, id_to_update))
                    self.db.commit()
                    messagebox.showinfo("Sucesso", f"Registro ID {id_to_update} atualizado com sucesso!")
                except mysql.connector.Error as err:
                    messagebox.showerror("Erro", f"Erro ao atualizar os dados: {err}")
            else:
                messagebox.showerror("Erro", "Por favor, insira uma nova descrição.")
        else:
            messagebox.showinfo("Info", "Atualização cancelada.")

    def delete_energy_data(self):
        # Perguntar ao usuário qual ID ele deseja deletar
        id_to_delete = simpledialog.askinteger("Deletar Dados", "Insira o ID do registro a ser deletado:")
        if id_to_delete is not None:
            try:
                query = "DELETE FROM gerenciamento_energia WHERE id=%s"
                self.cursor.execute(query, (id_to_delete,))
                self.db.commit()
                messagebox.showinfo("Sucesso", f"Registro ID {id_to_delete} deletado com sucesso!")
            except mysql.connector.Error as err:
                messagebox.showerror("Erro", f"Erro ao deletar os dados: {err}")
        else:
            messagebox.showinfo("Info", "Exclusão cancelada.")

    def energy_monitor(self):
        self.clear_window()
        
        tk.Label(self.root, text="Monitoramento de Consumo", bg="#f0f0f0", font=self.font_style).pack(pady=10)

        # Recuperar dados do banco de dados
        query = "SELECT * FROM gerenciamento_energia"
        self.cursor.execute(query)
        records = self.cursor.fetchall()

        if records:
            # Criar um gráfico com os dados
            ids = [record[0] for record in records]  # IDs
            descriptions = [record[1] for record in records]  # Descrições

            # Exibir as informações em um gráfico de barras
            plt.figure(figsize=(10, 5))
            plt.bar(ids, range(len(descriptions)), tick_label=descriptions)
            plt.xlabel('ID')
            plt.ylabel('Descrição')
            plt.title('Gerenciamento de Energia')
            plt.xticks(rotation=45, ha='right')
            plt.tight_layout()
            plt.show()  # Mostra o gráfico
        else:
            tk.Label(self.root, text="Nenhum dado encontrado.", bg="#f0f0f0", font=self.font_style).pack(pady=10)

        tk.Button(self.root, text="Voltar", command=self.create_main_window, bg="#2196F3", fg="white", font=self.font_style).pack(pady=10)

    def create_user_screen(self):
        self.clear_window()

        tk.Label(self.root, text="Criar Novo Usuário", bg="#f0f0f0", font=self.font_style).pack(pady=10)
        tk.Label(self.root, text="Novo Usuário", bg="#f0f0f0", font=self.font_style).pack(pady=5)
        self.new_user_entry = tk.Entry(self.root, font=self.font_style)
        self.new_user_entry.pack(pady=5)

        tk.Label(self.root, text="Nova Senha", bg="#f0f0f0", font=self.font_style).pack(pady=5)
        self.new_pass_entry = tk.Entry(self.root, show="*", font=self.font_style)
        self.new_pass_entry.pack(pady=5)

        tk.Button(self.root, text="Criar Usuário", command=self.create_user, bg="#4CAF50", fg="white", font=self.font_style).pack(pady=10)
        tk.Button(self.root, text="Voltar", command=self.create_login_screen, bg="#2196F3", fg="white", font=self.font_style).pack(pady=5)

    def create_user(self):
        new_user = self.new_user_entry.get()
        new_pass = self.new_pass_entry.get()

        if new_user and new_pass:
            query = "INSERT INTO usuarios (username, password) VALUES (%s, %s)"
            try:
                self.cursor.execute(query, (new_user, new_pass))
                self.db.commit()
                messagebox.showinfo("Sucesso", f"Usuário '{new_user}' criado com sucesso!")
                self.create_login_screen()
            except mysql.connector.Error as err:
                messagebox.showerror("Erro", f"Erro ao criar usuário: {err}")
        else:
            messagebox.showerror("Erro", "Preencha todos os campos!")

    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()

# Inicializar a aplicação
root = tk.Tk()
app = App(root)
root.mainloop()
