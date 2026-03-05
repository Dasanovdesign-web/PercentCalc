import sys
import os
from PySide6.QtWidgets import QApplication, QMainWindow, QMessageBox
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import QFile

class DepositApp(QMainWindow):
    def __init__(self):
        super().__init__()
        
        # 1. Загружаем интерфейс
        self.load_ui()
        
        # 2. кнопки к функциям
        self.ui.btn_calculate.clicked.connect(self.calculate_logic)
        self.ui.btn_clear.clicked.connect(self.clear_fields)

        
        self.ui.input_rate.editingFinished.connect(self.add_percent_symbol)
        self.ui.input_inflation.editingFinished.connect(self.add_percent_symbol)

    def load_ui(self):
        """Метод для загрузки .ui файла"""
        ui_file_path = os.path.join(os.path.dirname(__file__), "calc_design.ui")
        ui_file = QFile(ui_file_path)
        
        if not ui_file.open(QFile.ReadOnly):
            print(f"Не удалось открыть файл: {ui_file_path}")
            sys.exit(-1)
            
        loader = QUiLoader()
        self.ui = loader.load(ui_file)
        ui_file.close()
        
        self.setCentralWidget(self.ui)
        self.setWindowTitle("Финансовый калькулятор v2.0")
        
        # Подсказки (Placeholder)
        
        self.ui.input_amount.setPlaceholderText("Сумма депозита")
        self.ui.input_rate.setPlaceholderText("Ставка банка %")
        self.ui.input_inflation.setPlaceholderText("Текущая инфляция %")
        
        # Фиксируем размер
        self.setFixedSize(self.ui.size()) 

    def add_percent_symbol(self):
        """Добавляет %, если его нет, и исправляет запятые"""
        field = self.sender()
        text = field.text().strip().replace(',', '.')
        if text and not text.endswith('%'):
            field.setText(f"{text}%")

    def calculate_logic(self):
        """Логика расчета для КР [cite: 2026-01-16, 2026-01-26]"""
        try:
            # Чистим ввод от всего, кроме цифр и точек
            def clean_val(text):
                # Оставляем только цифры и точку
                return "".join(c for c in text.replace(',', '.') if c.isdigit() or c == '.')

            val_amount = clean_val(self.ui.input_amount.text())
            val_rate = clean_val(self.ui.input_rate.text())
            val_inflation = clean_val(self.ui.input_inflation.text())

            if not val_amount or not val_rate:
                QMessageBox.warning(self, "Ошибка", "Заполните сумму и ставку")
                return

            amount = float(val_amount)
            deposit_rate = float(val_rate)
            inflation_rate = float(val_inflation) if val_inflation else 0.0

            if amount <= 0:
                QMessageBox.warning(self, "Ошибка", "Сумма должна быть больше нуля")
                return

            # Налоги (10% нерезидент, 0% резидент) 
            is_non_resident = self.ui.radio_nonresident.isChecked()
            effective_nominal_rate = deposit_rate * (0.90 if is_non_resident else 1.0)

            # Формула Фишера 
            real_rate = ((1 + effective_nominal_rate/100) / (1 + inflation_rate/100) - 1) * 100
            real_money_profit = amount * (real_rate / 100)

            status = "Нерезидент КР (10%)" if is_non_resident else "Резидент КР (0%)"
            result_text = (
                f"Статус: {status}\n"
                f"Реальная прибыль: {real_money_profit:.2f} сом\n"
                f"Реальная ставка: {real_rate:.2f}%"
            )
            
            self.ui.lbl_result.setText(result_text)
            
            # Цвет: зеленый для +, красный для -
            color = "#4caf50" if real_rate > 0 else "#D96060"
            self.ui.lbl_result.setStyleSheet(f"color: {color}; font-weight: bold; background: transparent;")

        except ValueError:
            QMessageBox.critical(self, "Ошибка", "Введите корректные числа")

    def clear_fields(self):
        """Очистка всех полей [cite: 2026-02-05]"""
        self.ui.input_amount.clear()
        self.ui.input_rate.clear()   
        self.ui.input_inflation.clear()
        self.ui.lbl_result.setText("Ожидание данных...")
        self.ui.lbl_result.setStyleSheet("color: #D1D1D1; background: transparent;")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = DepositApp()
    window.show()
    sys.exit(app.exec())