import tkinter as tk
from tkinter import messagebox

def calculate():
    try:
        # Получаем данные из полей
        amount = float(entry_amount.get())
        deposit_rate = float(entry_deposit.get())
        inflation_rate = float(entry_inflation.get())
        
        # 1. Считаем «грязную» прибыль
        nominal_profit = (amount * deposit_rate) / 100

        # 2. Логика налогов (Ветка пользователя)
        if tax_var.get() == 1: # Нерезидент
            tax_value = nominal_profit * 0.10
            profit_after_tax = nominal_profit - tax_value
            status_text = "Статус: Нерезидент КР (налог 10%)"
        else: # Резидент
            profit_after_tax = nominal_profit
            status_text = "Статус: Резидент КР (налог 0%)"

        # 3. Учитываем инфляцию 
        inflation_loss = (amount * inflation_rate) / 100
        real_money_profit = profit_after_tax - inflation_loss
        
        # 4. Считаем реальную процентную ставку 
        real_rate = (real_money_profit / amount) * 100

        # Формируем итоговый текст
        result_text = f"{status_text}\n"
        result_text += f"Чистая прибыль: {real_money_profit:.2f} сом\n"
        result_text += f"Реальная ставка: {real_rate:.2f}%"
        
        # Визуальный фидбек (Цвета)
        if real_rate > 0:
            label_result.config(fg="green")
            result_text += "\nВаши деньги приумножились! 📈"
        elif real_rate == 0:
            label_result.config(fg="blue")
            result_text += "\nЦенность денег сохранилась ⚖️"
        else:
            label_result.config(fg="red")
            result_text += "\nИнфляция съедает сбережения 📉"

        label_result.config(text=result_text)
        
    except ValueError:
        messagebox.showerror("Ошибка", "Введите числа во все поля")

def clear_fields():
    entry_amount.delete(0, tk.END)
    entry_deposit.delete(0, tk.END)
    entry_inflation.delete(0, tk.END)
    entry_inflation.insert(0, "9.5")
    label_result.config(text="", fg="black")        


root = tk.Tk()
root.title("Депозитный калькулятор")
root.geometry("400x600") 

tk.Label(root, text="Анализ депозита", font=("Inter", 14, "bold")).pack(pady=10)

# Поля ввода
tk.Label(root, text="Сумма депозита (сом):").pack()
entry_amount = tk.Entry(root)
entry_amount.pack(pady=5)

tk.Label(root, text="Ставка банка (%):").pack()
entry_deposit = tk.Entry(root)
entry_deposit.pack(pady=5)

tk.Label(root, text="Текущая инфляция (%):").pack()
entry_inflation = tk.Entry(root)
entry_inflation.insert(0, "9.5") 
entry_inflation.pack(pady=5)

# --- ВЫБОР СТАТУСА ---
tk.Label(root, text="Ваш статус:", font=("Inter", 10, "bold")).pack(pady=10)

tax_var = tk.IntVar() 
tax_var.set(0) # По умолчанию Резидент (0)

tk.Radiobutton(root, text="Резидент КР (0%)", variable=tax_var, value=0).pack()
tk.Radiobutton(root, text="Нерезидент (10%)", variable=tax_var, value=1).pack()

# Кнопки
btn_calc = tk.Button(root, text="Рассчитать", command=calculate, bg="#4caf50", fg="White", font=("Inter", 12, "bold"))
btn_calc.pack(pady=20)

btn_clear = tk.Button(root, text="Очистить", command=clear_fields, bg="#D96060", fg="white")
btn_clear.pack(pady=5)

# Результат
label_result = tk.Label(root, text="", font=("Inter", 11), justify="center")
label_result.pack(pady=10)

root.mainloop()