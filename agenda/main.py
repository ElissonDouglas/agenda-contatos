from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from csv import reader



contatos = []

with open('contatos.csv', 'r') as arquivo:
    leitor = reader(arquivo)
    next(leitor)
    for linha in leitor:
        contatos.append(linha)
        

class Painel(Tk):
    
    def __init__(self: object) -> None:
        super().__init__()
        self.title('Agenda de Contatos')
        self.resizable(False, False)
        self.geometry('700x550')
        self.configure(background='#45a8f7')
        
        # Tela dos contatos
        self.frame_contatos = Frame(self)
        self.frame_contatos.place(relx=0.14, rely=0.5, width=499, height=217)
        
        # Botões
        self.adicionar = Button(self, text='Adicionar aos Contatos', command=lambda: self.adicionar_contato())
        self.adicionar.place(width=170, height=25, x=85, y=220)
        
        self.remover = Button(self, text='Remover contato', command=lambda: self.remover_contato(), fg='red')
        self.remover.place(width=170, height=25, x=500, y=160)
        
        self.sair = Button(self, text='Sair', command=lambda: self.sair_app(), fg='red').place(relx=0.4, rely=0.94, width=130, height=25)
        
        # colunas
        colunas = ('#1', '#2', '#3')
        self.tree = ttk.Treeview(self.frame_contatos, columns=colunas, show='headings')
        self.tree.grid(row=0, column=0, sticky='nsew')
        self.tree.heading('#1', text='Nome')
        self.tree.heading('#2', text='Telefone')
        self.tree.heading('#3', text='Email')
        
        # tamanho das colunas
        self.tree.column('#1', width=120)
        self.tree.column('#2', width=150)
        self.tree.column('#3', width=210)
        
        # inserindo contatos na self.treeview
        for contato in contatos:
            contato[0] = str(contato[0])
            self.tree.insert('', END, values=contato)
            
        # barra scroll
        barra_scroll = ttk.Scrollbar(self.frame_contatos, orient=VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=barra_scroll.set)
        barra_scroll.grid(row=0, column=1, sticky='ns')
        
        # Adicionar novo contato
        Label(self, text='AGENDA DE CONTATOS', fg='black', bg='#0471c9', font='Arial, 25').place(relx=0.5, rely=0.08, anchor=CENTER, width=1000, height=100)
        Label(self, text='Nome:', font=('Arial', 12, 'bold'), bg='#45a8f7', fg='white').place(width=80, height=21, x=13, y=130)
        Label(self, text='Tel.:', font=('Arial', 12, 'bold'), bg='#45a8f7', fg='white').place(width=80, height=21, x=4, y=160)
        Label(self, text='Email:', font=('Arial', 12, 'bold'), bg='#45a8f7', fg='white').place(width=80, height=21, x=13, y=190)
        Label(self, text='Nome:', font=('Arial', 12, 'bold'), bg='#45a8f7', fg='white').place(width=80, height=21, x=420, y=130)
        
        # Entrada do usuário
        self.nome_input = StringVar()
        self.nome_input.set('')
        self.nome_remover_input = StringVar()
        self.nome_remover_input.set('')
        self.telefone_input = StringVar()
        self.telefone_input.set('')
        self.email_input = StringVar()
        self.email_input.set('')
        
        
        self.nome_entrada = Entry(self, background='white', textvariable=self.nome_input).place(width=170, height=20, x=85, y=130)
        self.nome_remover = Entry(self, background='white', textvariable=self.nome_remover_input).place(width=170, height=20, x=500, y=130)
        self.telefone_entrada = Entry(self, background='white', textvariable=self.telefone_input).place(width=170, height=20, x=85, y=160)
        self.email_entrada = Entry(self, background='white', textvariable=self.email_input).place(width=170, height=20, x=85, y=190)
        
        
        # Funções
             
    def adicionar_contato(self: object) -> None:
        if self.nome_input.get() != '' and self.telefone_input.get() != '' and self.email_input.get() != '':
            contatos.append([self.nome_input.get(), self.telefone_input.get(), self.email_input.get()])
            self.nome_input.set('')
            self.telefone_input.set('')
            self.email_input.set('')
        else:
            messagebox.showerror('Erro', 'Preencha todos os campos')
        self.atualizar()       
    
    def remover_contato(self: object) -> None:
        encontrei = False
        preenchido = False
        if self.nome_remover_input.get() != '':
            preenchido = True
            remover = self.nome_remover_input.get()
            for contato in contatos:
                if contato[0] == remover:
                    contatos.pop(contatos.index(contato))
                    self.nome_remover_input.set('')
                    messagebox.showinfo('Sucesso', 'Contato removido com sucesso')
                    encontrei = True
                    self.atualizar()
                    break
        else:
            messagebox.showerror('Erro', 'Preencha o nome do contato.')
        if preenchido == True and encontrei == False:
            messagebox.showerror('Erro', 'Contato não encontrado')
            self.nome_remover_input.set('')   
    
    def atualizar(self: object) -> None:
        self.tree.delete(*self.tree.get_children())
        for contato in contatos:
            contato[0] = str(contato[0])
            self.tree.insert('', END, values=contato)
        with open('contatos.csv', 'w') as arquivo:
            arquivo.write('Nome,Telefone,Email\n')
            for contato in contatos:
                if contato[0] != '':
                    arquivo.write(f'{contato[0]},{contato[1]},{contato[2]}\n')
        messagebox.showinfo('Agenda atualizada', 'Agenda atualizada com sucesso')   
        
    
    def sair_app(self: object) -> None:
        pergunta = messagebox.askyesno('Sair', 'Deseja salvar os dados da agenda antes de sair?')
        if pergunta:
            self.atualizar()
            self.destroy()
        else:
            self.destroy()
            

if __name__ == '__main__':
    app = Painel()
    app.mainloop()
