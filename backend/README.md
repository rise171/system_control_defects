### Запуск серверной части:

Выполнить следующую последовательность команд:
1. cd \backend
2. python -m venv venv
3. venv\Scripts\activate
4. pip install -r requirements.txt
5. uvicorn main:app -reload