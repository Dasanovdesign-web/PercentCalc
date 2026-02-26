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
        
        # 2. Привязываем кнопки к функциям
        # Имена должны строго совпадать с ObjectName в Designer!
        self.ui.btn_calculate.clicked.connect(self.calculate_logic)
        self.ui.btn_clear.clicked.connect(self.clear_fields)

    def load_ui(self):
        """Метод для загрузки .ui файла"""
        ui_file_path = os.path.join(os.path.dirname(__file__), "calc_design.ui")
        ui_file = QFile(ui_file_path)
        
        if not ui_file.open(QFile.ReadOnly):
            print(f"Не удалось открыть файл: {ui_file_path}")
            sys.exit(-1)
            
        loader = QUiLoader()
        self.ui = loader.load(ui_file) # Загружаем UI как объект
        ui_file.close()
        
        # Устанавливаем загруженный UI как центральную часть окна
        self.setCentralWidget(self.ui)
        self.setWindowTitle("Инженерный калькулятор v2.0")
        
        # Подгоняем размер окна под размер дизайна из Designer
        self.setFixedSize(self.ui.size()) 

    def calculate_logic(self):
        """Вся твоя математика здесь [cite: 2026-01-26]"""
        try:
            # Считываем данные из QLineEdit
            amount = float(self.ui.input_amount.text())
            deposit_rate = float(self.ui.input_rate.text())
            inflation_rate = float(self.ui.input_inflation.text())

            if amount <= 0:
                QMessageBox.warning(self, "Ошибка", "Сумма должна быть больше нуля")
                return

            # Логика налогов (резидент/нерезидент КР) [cite: 2026-01-16]
            is_non_resident = self.ui.radio_nonresident.isChecked()
            effective_nominal_rate = deposit_rate * (0.90 if is_non_resident else 1.0)

            # Формула Фишера (Реальная ставка) [cite: 2026-01-26]
            real_rate = ((1 + effective_nominal_rate/100) / (1 + inflation_rate/100) - 1) * 100
            real_money_profit = amount * (real_rate / 100)

            # Вывод результата в QLabel
            status = "Нерезидент КР (10%)" if is_non_resident else "Резидент КР (0%)"
            result_text = (
                f"Статус: {status}\n"
                f"Реальная прибыль: {real_money_profit:.2f} сом\n"
                f"Реальная ставка: {real_rate:.2f}%"
            )
            
            self.ui.lbl_result.setText(result_text)
            
            # Меняем цвет текста (зеленый для прибыли, красный для убытка)
            if real_rate > 0:
                self.ui.lbl_result.setStyleSheet("color: #4caf50; font-weight: bold; background: transparent;")
            else:
                self.ui.lbl_result.setStyleSheet("color: #D96060; font-weight: bold; background: transparent;")

        except ValueError:
            QMessageBox.critical(self, "Ошибка", "Пожалуйста, введите корректные числа")

    def clear_fields(self):
        """Очистка всех полей [cite: 2026-02-05]"""
        self.ui.input_amount.clear()
        self.ui.input_rate.clear()
        self.ui.input_inflation.setText("9.5") 
        self.ui.lbl_result.setText("Ожидание данных...")
        self.ui.lbl_result.setStyleSheet("color: #D1D1D1; background: transparent;")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = DepositApp()
    window.show()
    sys.exit(app.exec())