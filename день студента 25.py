import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from datetime import datetime, timedelta
import json
import os

class StudentDay25:
    def __init__(self, root):
        self.root = root
        self.root.title("День студента 25")
        self.root.geometry("800x600")
        
        # Инициализация данных
        self.tasks = []
        self.events = []
        self.notes = []
        self.load_data()
        
        # Стили
        self.style = ttk.Style()
        self.style.configure('TFrame', background='#f9ecec')
        self.style.configure('TButton', padding=5, relief='flat', background='#4CAF50', foreground='black')  # Черный текст
        self.style.map('TButton', background=[('active', '#45a049')])
        self.style.configure('TLabel', background='#f0f0f0', font=('Arial', 10), foreground='black')  # Черный текст
        self.style.configure('Header.TLabel', font=('Arial', 12, 'bold'), foreground='black')  # Черный текст
        
        # Главный контейнер
        self.main_frame = ttk.Frame(root)
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Создание виджетов
        self.create_widgets()
        
        # Запуск обновления времени
        self.update_time()
        
    def create_widgets(self):
        # Верхняя панель с датой и временем
        top_frame = ttk.Frame(self.main_frame)
        top_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.date_label = ttk.Label(top_frame, text="", style='Header.TLabel')
        self.date_label.pack(side=tk.LEFT)
        
        self.time_label = ttk.Label(top_frame, text="", style='Header.TLabel')
        self.time_label.pack(side=tk.RIGHT)
        
        # Панель вкладок
        self.notebook = ttk.Notebook(self.main_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True)
        
        # Вкладка Задачи
        self.tasks_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.tasks_tab, text="Задачи")
        self.create_tasks_tab()
        
        # Вкладка События
        self.events_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.events_tab, text="События")
        self.create_events_tab()
        
        # Вкладка Заметки
        self.notes_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.notes_tab, text="Заметки")
        self.create_notes_tab()
        
        # Вкладка Поиск
        self.search_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.search_tab, text="Поиск")
        self.create_search_tab()
        
        # Кнопка сохранения
        save_button = ttk.Button(self.main_frame, text="Сохранить все данные", command=self.save_data)
        save_button.pack(pady=10)
    
    def create_tasks_tab(self):
        # Панель управления задачами
        tasks_control_frame = ttk.Frame(self.tasks_tab)
        tasks_control_frame.pack(fill=tk.X, pady=(0, 10))
        
        add_task_button = ttk.Button(tasks_control_frame, text="Добавить задачу", command=self.add_task)
        add_task_button.pack(side=tk.LEFT, padx=(0, 5))
        
        edit_task_button = ttk.Button(tasks_control_frame, text="Редактировать", command=self.edit_task)
        edit_task_button.pack(side=tk.LEFT, padx=5)
        
        delete_task_button = ttk.Button(tasks_control_frame, text="Удалить", command=self.delete_task)
        delete_task_button.pack(side=tk.LEFT, padx=5)
        
        complete_task_button = ttk.Button(tasks_control_frame, text="Отметить выполненной", command=self.complete_task)
        complete_task_button.pack(side=tk.LEFT, padx=5)
        
        # Таблица задач
        self.tasks_tree = ttk.Treeview(self.tasks_tab, columns=('id', 'title', 'priority', 'deadline', 'status'), show='headings')
        self.tasks_tree.pack(fill=tk.BOTH, expand=True)
        
        self.tasks_tree.heading('id', text='ID')
        self.tasks_tree.heading('title', text='Название')
        self.tasks_tree.heading('priority', text='Приоритет')
        self.tasks_tree.heading('deadline', text='Срок выполнения')
        self.tasks_tree.heading('status', text='Статус')
        
        self.tasks_tree.column('id', width=50, anchor=tk.CENTER)
        self.tasks_tree.column('title', width=200)
        self.tasks_tree.column('priority', width=100, anchor=tk.CENTER)
        self.tasks_tree.column('deadline', width=150, anchor=tk.CENTER)
        self.tasks_tree.column('status', width=100, anchor=tk.CENTER)
        
        # Установка черного цвета текста в Treeview
        style = ttk.Style()
        style.configure("Treeview", foreground="black")
        style.configure("Treeview.Heading", foreground="black")
        
        self.update_tasks_list()
    
    def create_events_tab(self):
        # Панель управления событиями
        events_control_frame = ttk.Frame(self.events_tab)
        events_control_frame.pack(fill=tk.X, pady=(0, 10))
        
        add_event_button = ttk.Button(events_control_frame, text="Добавить событие", command=self.add_event)
        add_event_button.pack(side=tk.LEFT, padx=(0, 5))
        
        edit_event_button = ttk.Button(events_control_frame, text="Редактировать", command=self.edit_event)
        edit_event_button.pack(side=tk.LEFT, padx=5)
        
        delete_event_button = ttk.Button(events_control_frame, text="Удалить", command=self.delete_event)
        delete_event_button.pack(side=tk.LEFT, padx=5)
        
        # Таблица событий
        self.events_tree = ttk.Treeview(self.events_tab, columns=('id', 'title', 'date', 'time', 'location'), show='headings')
        self.events_tree.pack(fill=tk.BOTH, expand=True)
        
        self.events_tree.heading('id', text='ID')
        self.events_tree.heading('title', text='Название')
        self.events_tree.heading('date', text='Дата')
        self.events_tree.heading('time', text='Время')
        self.events_tree.heading('location', text='Место')
        
        self.events_tree.column('id', width=50, anchor=tk.CENTER)
        self.events_tree.column('title', width=200)
        self.events_tree.column('date', width=100, anchor=tk.CENTER)
        self.events_tree.column('time', width=100, anchor=tk.CENTER)
        self.events_tree.column('location', width=150)
        
        self.update_events_list()
    
    def create_notes_tab(self):
        # Панель управления заметками
        notes_control_frame = ttk.Frame(self.notes_tab)
        notes_control_frame.pack(fill=tk.X, pady=(0, 10))
        
        add_note_button = ttk.Button(notes_control_frame, text="Добавить заметку", command=self.add_note)
        add_note_button.pack(side=tk.LEFT, padx=(0, 5))
        
        edit_note_button = ttk.Button(notes_control_frame, text="Редактировать", command=self.edit_note)
        edit_note_button.pack(side=tk.LEFT, padx=5)
        
        delete_note_button = ttk.Button(notes_control_frame, text="Удалить", command=self.delete_note)
        delete_note_button.pack(side=tk.LEFT, padx=5)
        
        # Текстовое поле для заметок
        self.notes_text = tk.Text(self.notes_tab, wrap=tk.WORD, foreground='black')  # Черный текст
        self.notes_text.pack(fill=tk.BOTH, expand=True)
        
        self.update_notes_list()
    
    def create_search_tab(self):
        # Панель поиска
        search_control_frame = ttk.Frame(self.search_tab)
        search_control_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.search_entry = ttk.Entry(search_control_frame, foreground='black')  # Черный текст
        self.search_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))
        
        search_button = ttk.Button(search_control_frame, text="Поиск", command=self.perform_search)
        search_button.pack(side=tk.LEFT)
        
        # Результаты поиска
        self.search_results = tk.Text(self.search_tab, wrap=tk.WORD, state=tk.DISABLED, foreground='black')  # Черный текст
        self.search_results.pack(fill=tk.BOTH, expand=True)
    
    def update_time(self):
        now = datetime.now()
        self.date_label.config(text=now.strftime("%d.%m.%Y"))
        self.time_label.config(text=now.strftime("%H:%M:%S"))
        self.root.after(1000, self.update_time)
    
    # Методы для работы с задачами
    def add_task(self):
        dialog = TaskDialog(self.root, "Добавить задачу")
        if dialog.result:
            task = {
                'id': len(self.tasks) + 1,
                'title': dialog.result['title'],
                'description': dialog.result['description'],
                'priority': dialog.result['priority'],
                'deadline': dialog.result['deadline'],
                'status': 'Активная',
                'created_at': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            self.tasks.append(task)
            self.update_tasks_list()
    
    def edit_task(self):
        selected = self.tasks_tree.selection()
        if not selected:
            messagebox.showwarning("Предупреждение", "Выберите задачу для редактирования")
            return
        
        item = self.tasks_tree.item(selected[0])
        task_id = int(item['values'][0])
        task = next((t for t in self.tasks if t['id'] == task_id), None)
        
        if task:
            dialog = TaskDialog(self.root, "Редактировать задачу", task)
            if dialog.result:
                task.update({
                    'title': dialog.result['title'],
                    'description': dialog.result['description'],
                    'priority': dialog.result['priority'],
                    'deadline': dialog.result['deadline']
                })
                self.update_tasks_list()
    
    def delete_task(self):
        selected = self.tasks_tree.selection()
        if not selected:
            messagebox.showwarning("Предупреждение", "Выберите задачу для удаления")
            return
        
        if messagebox.askyesno("Подтверждение", "Вы уверены, что хотите удалить задачу?"):
            item = self.tasks_tree.item(selected[0])
            task_id = int(item['values'][0])
            self.tasks = [t for t in self.tasks if t['id'] != task_id]
            self.update_tasks_list()
    
    def complete_task(self):
        selected = self.tasks_tree.selection()
        if not selected:
            messagebox.showwarning("Предупреждение", "Выберите задачу для отметки выполнения")
            return
        
        item = self.tasks_tree.item(selected[0])
        task_id = int(item['values'][0])
        task = next((t for t in self.tasks if t['id'] == task_id), None)
        
        if task:
            task['status'] = 'Выполнена'
            task['completed_at'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            self.update_tasks_list()
    
    def update_tasks_list(self):
        for item in self.tasks_tree.get_children():
            self.tasks_tree.delete(item)
        
        for task in sorted(self.tasks, key=lambda x: (x['priority'], x['deadline'])):
            self.tasks_tree.insert('', tk.END, values=(
                task['id'],
                task['title'],
                task['priority'],
                task['deadline'],
                task['status']
            ))
    
    # Методы для работы с событиями
    def add_event(self):
        dialog = EventDialog(self.root, "Добавить событие")
        if dialog.result:
            event = {
                'id': len(self.events) + 1,
                'title': dialog.result['title'],
                'description': dialog.result['description'],
                'date': dialog.result['date'],
                'time': dialog.result['time'],
                'location': dialog.result['location'],
                'created_at': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            self.events.append(event)
            self.update_events_list()
    
    def edit_event(self):
        selected = self.events_tree.selection()
        if not selected:
            messagebox.showwarning("Предупреждение", "Выберите событие для редактирования")
            return
        
        item = self.events_tree.item(selected[0])
        event_id = int(item['values'][0])
        event = next((e for e in self.events if e['id'] == event_id), None)
        
        if event:
            dialog = EventDialog(self.root, "Редактировать событие", event)
            if dialog.result:
                event.update({
                    'title': dialog.result['title'],
                    'description': dialog.result['description'],
                    'date': dialog.result['date'],
                    'time': dialog.result['time'],
                    'location': dialog.result['location']
                })
                self.update_events_list()
    
    def delete_event(self):
        selected = self.events_tree.selection()
        if not selected:
            messagebox.showwarning("Предупреждение", "Выберите событие для удаления")
            return
        
        if messagebox.askyesno("Подтверждение", "Вы уверены, что хотите удалить событие?"):
            item = self.events_tree.item(selected[0])
            event_id = int(item['values'][0])
            self.events = [e for e in self.events if e['id'] != event_id]
            self.update_events_list()
    
    def update_events_list(self):
        for item in self.events_tree.get_children():
            self.events_tree.delete(item)
        
        for event in sorted(self.events, key=lambda x: (x['date'], x['time'])):
            self.events_tree.insert('', tk.END, values=(
                event['id'],
                event['title'],
                event['date'],
                event['time'],
                event['location']
            ))
    
    # Методы для работы с заметками
    def add_note(self):
        note_text = simpledialog.askstring("Добавить заметку", "Введите текст заметки:")
        if note_text:
            note = {
                'id': len(self.notes) + 1,
                'text': note_text,
                'created_at': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            self.notes.append(note)
            self.update_notes_list()
    
    def edit_note(self):
        if not self.notes:
            messagebox.showwarning("Предупреждение", "Нет заметок для редактирования")
            return
        
        # Простое редактирование последней заметки
        last_note = self.notes[-1]
        new_text = simpledialog.askstring("Редактировать заметку", "Измените текст заметки:", initialvalue=last_note['text'])
        if new_text:
            last_note['text'] = new_text
            self.update_notes_list()
    
    def delete_note(self):
        if not self.notes:
            messagebox.showwarning("Предупреждение", "Нет заметок для удаления")
            return
        
        if messagebox.askyesno("Подтверждение", "Удалить последнюю заметку?"):
            self.notes.pop()
            self.update_notes_list()
    
    def update_notes_list(self):
        self.notes_text.config(state=tk.NORMAL)
        self.notes_text.delete(1.0, tk.END)
        
        for note in self.notes:
            self.notes_text.insert(tk.END, f"{note['created_at']}\n{note['text']}\n\n")
        
        self.notes_text.config(state=tk.DISABLED)
    
    # Методы для работы с поиском
    def perform_search(self):
        query = self.search_entry.get().strip().lower()
        if not query:
            messagebox.showwarning("Предупреждение", "Введите поисковый запрос")
            return
        
        results = []
        
        # Поиск в задачах
        for task in self.tasks:
            if (query in task['title'].lower() or 
                query in task['description'].lower() or 
                query in task['priority'].lower()):
                results.append(f"Задача: {task['title']} (Приоритет: {task['priority']}, Срок: {task['deadline']})")
        
        # Поиск в событиях
        for event in self.events:
            if (query in event['title'].lower() or 
                query in event['description'].lower() or 
                query in event['location'].lower()):
                results.append(f"Событие: {event['title']} (Дата: {event['date']}, Место: {event['location']})")
        
        # Поиск в заметках
        for note in self.notes:
            if query in note['text'].lower():
                results.append(f"Заметка: {note['text'][:50]}...")
        
        # Отображение результатов
        self.search_results.config(state=tk.NORMAL)
        self.search_results.delete(1.0, tk.END)
        
        if results:
            self.search_results.insert(tk.END, f"Найдено {len(results)} результатов по запросу '{query}':\n\n")
            for result in results:
                self.search_results.insert(tk.END, f"- {result}\n")
        else:
            self.search_results.insert(tk.END, f"По запросу '{query}' ничего не найдено.")
        
        self.search_results.config(state=tk.DISABLED)
    
    # Работа с данными
    def save_data(self):
        data = {
            'tasks': self.tasks,
            'events': self.events,
            'notes': self.notes
        }
        
        try:
            with open('student_day_data.json', 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            messagebox.showinfo("Сохранение", "Данные успешно сохранены")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось сохранить данные: {str(e)}")
    
    def load_data(self):
        if os.path.exists('student_day_data.json'):
            try:
                with open('student_day_data.json', 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                self.tasks = data.get('tasks', [])
                self.events = data.get('events', [])
                self.notes = data.get('notes', [])
            except Exception as e:
                messagebox.showerror("Ошибка", f"Не удалось загрузить данные: {str(e)}")

class TaskDialog(tk.Toplevel):
    def __init__(self, parent, title, task=None):
        super().__init__(parent)
        self.title(title)
        self.geometry("400x300")
        self.resizable(False, False)
        
        self.task = task
        self.result = None
        
        self.create_widgets()
        
        self.transient(parent)
        self.grab_set()
        self.wait_window(self)
    
    def create_widgets(self):
        frame = ttk.Frame(self)
        frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Название задачи
        ttk.Label(frame, text="Название:").grid(row=0, column=0, sticky=tk.W, pady=(0, 5))
        self.title_entry = ttk.Entry(frame, foreground='black')  # Черный текст
        self.title_entry.grid(row=0, column=1, sticky=tk.EW, pady=(0, 5))
        
        # Описание
        ttk.Label(frame, text="Описание:").grid(row=1, column=0, sticky=tk.NW, pady=(0, 5))
        self.description_text = tk.Text(frame, height=5, width=30, foreground='black')  # Черный текст
        self.description_text.grid(row=1, column=1, sticky=tk.EW, pady=(0, 5))
        
        # Приоритет
        ttk.Label(frame, text="Приоритет:").grid(row=2, column=0, sticky=tk.W, pady=(0, 5))
        self.priority_var = tk.StringVar()
        self.priority_combobox = ttk.Combobox(frame, textvariable=self.priority_var, 
                                           values=["Высокий", "Средний", "Низкий"])
        self.priority_combobox.grid(row=2, column=1, sticky=tk.EW, pady=(0, 5))
        self.priority_combobox.current(1)
        
        # Срок выполнения
        ttk.Label(frame, text="Срок выполнения (дд.мм.гггг):").grid(row=3, column=0, sticky=tk.W, pady=(0, 5))
        self.deadline_entry = ttk.Entry(frame, foreground='black')  # Черный текст
        self.deadline_entry.grid(row=3, column=1, sticky=tk.EW, pady=(0, 5))
        
        # Кнопки
        button_frame = ttk.Frame(frame)
        button_frame.grid(row=4, column=0, columnspan=2, pady=(10, 0))
        
        save_button = ttk.Button(button_frame, text="Сохранить", command=self.on_save)
        save_button.pack(side=tk.RIGHT, padx=(5, 0))
        
        cancel_button = ttk.Button(button_frame, text="Отмена", command=self.destroy)
        cancel_button.pack(side=tk.RIGHT)
        
        # Заполнение данных, если редактирование
        if self.task:
            self.title_entry.insert(0, self.task['title'])
            self.description_text.insert(1.0, self.task.get('description', ''))
            self.priority_var.set(self.task['priority'])
            self.deadline_entry.insert(0, self.task['deadline'])
    
    def on_save(self):
        title = self.title_entry.get().strip()
        description = self.description_text.get(1.0, tk.END).strip()
        priority = self.priority_var.get()
        deadline = self.deadline_entry.get().strip()
        
        if not title:
            messagebox.showwarning("Ошибка", "Введите название задачи")
            return
        
        if not deadline:
            messagebox.showwarning("Ошибка", "Введите срок выполнения")
            return
        
        self.result = {
            'title': title,
            'description': description,
            'priority': priority,
            'deadline': deadline
        }
        
        self.destroy()

class EventDialog(tk.Toplevel):
    def __init__(self, parent, title, event=None):
        super().__init__(parent)
        self.title(title)
        self.geometry("400x350")
        self.resizable(False, False)
        
        self.event = event
        self.result = None
        
        self.create_widgets()
        
        self.transient(parent)
        self.grab_set()
        self.wait_window(self)
    
    def create_widgets(self):
        frame = ttk.Frame(self)
        frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Название события
        ttk.Label(frame, text="Название:").grid(row=0, column=0, sticky=tk.W, pady=(0, 5))
        self.title_entry = ttk.Entry(frame, foreground='black')  # Черный текст
        self.title_entry.grid(row=0, column=1, sticky=tk.EW, pady=(0, 5))
        
        # Описание
        ttk.Label(frame, text="Описание:").grid(row=1, column=0, sticky=tk.NW, pady=(0, 5))
        self.description_text = tk.Text(frame, height=5, width=30, foreground='black')  # Черный текст
        self.description_text.grid(row=1, column=1, sticky=tk.EW, pady=(0, 5))
        
        # Дата
        ttk.Label(frame, text="Дата (дд.мм.гггг):").grid(row=2, column=0, sticky=tk.W, pady=(0, 5))
        self.date_entry = ttk.Entry(frame, foreground='black')  # Черный текст
        self.date_entry.grid(row=2, column=1, sticky=tk.EW, pady=(0, 5))
        
        # Время
        ttk.Label(frame, text="Время (чч:мм):").grid(row=3, column=0, sticky=tk.W, pady=(0, 5))
        self.time_entry = ttk.Entry(frame, foreground='black')  # Черный текст
        self.time_entry.grid(row=3, column=1, sticky=tk.EW, pady=(0, 5))
        
        # Место
        ttk.Label(frame, text="Место:").grid(row=4, column=0, sticky=tk.W, pady=(0, 5))
        self.location_entry = ttk.Entry(frame, foreground='black')  # Черный текст
        self.location_entry.grid(row=4, column=1, sticky=tk.EW, pady=(0, 5))
        
        # Кнопки
        button_frame = ttk.Frame(frame)
        button_frame.grid(row=5, column=0, columnspan=2, pady=(10, 0))
        
        save_button = ttk.Button(button_frame, text="Сохранить", command=self.on_save)
        save_button.pack(side=tk.RIGHT, padx=(5, 0))
        
        cancel_button = ttk.Button(button_frame, text="Отмена", command=self.destroy)
        cancel_button.pack(side=tk.RIGHT)
        
        # Заполнение данных, если редактирование
        if self.event:
            self.title_entry.insert(0, self.event['title'])
            self.description_text.insert(1.0, self.event.get('description', ''))
            self.date_entry.insert(0, self.event['date'])
            self.time_entry.insert(0, self.event['time'])
            self.location_entry.insert(0, self.event['location'])
    
    def on_save(self):
        title = self.title_entry.get().strip()
        description = self.description_text.get(1.0, tk.END).strip()
        date = self.date_entry.get().strip()
        time = self.time_entry.get().strip()
        location = self.location_entry.get().strip()
        
        if not title:
            messagebox.showwarning("Ошибка", "Введите название события")
            return
        
        if not date:
            messagebox.showwarning("Ошибка", "Введите дату события")
            return
        
        if not time:
            messagebox.showwarning("Ошибка", "Введите время события")
            return
        
        self.result = {
            'title': title,
            'description': description,
            'date': date,
            'time': time,
            'location': location
        }
        
        self.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = StudentDay25(root)
    root.mainloop()