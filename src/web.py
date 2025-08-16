# Импорт встроенной библиотеки для работы веб-сервера
from http.server import BaseHTTPRequestHandler, HTTPServer
import time
from pathlib import Path
base_dir = Path(__file__).resolve().parent.parent

# Для начала определим настройки запуска
hostName = "localhost"  # Адрес для доступа по сети
serverPort = 8080  # Порт для доступа по сети


class MyServer(BaseHTTPRequestHandler):
    """
        Специальный класс, который отвечает за
        обработку входящих запросов от клиентов
    """

    def do_GET(self):
        """ Метод для обработки входящих GET-запросов """
        try:
            # Читаем HTML-файл
            # with open(f'{base_dir}\\customers_data.csv', newline='') as file:
            with open(f'{base_dir}\\contacts.html', 'r', encoding='utf-8') as file:
                html_content = file.read()

            # Кодируем содержимое в bytes
            encoded_content = html_content.encode('utf-8')

            self.send_response(200)  # Отправка кода ответа
            self.send_header("Content-type", "text/html; charset=utf-8")  # Отправка типа данных, который будет передаваться
            self.send_header("Content-Length", str(len(encoded_content))) # Добавляем длину контент
            self.end_headers()  # Завершение формирования заголовков ответа
            self.wfile.write(encoded_content)  # Тело ответа

        except FileNotFoundError:
            self.send_error(404, "File not found")
        except Exception as e:
            self.send_error(500, f"Server error: {str(e)}")

    def do_POST(self):
        """ Метод для обработки входящих POST-запросов """
        content_length = int(self.headers['Content-Length'])
        body = self.rfile.read(content_length)
        print(body)
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()


if __name__ == "__main__":
    # Инициализация веб-сервера, который будет по заданным параметрах в сети
    # принимать запросы и отправлять их на обработку специальному классу, который был описан выше
    webServer = HTTPServer((hostName, serverPort), MyServer)
    print("Server started http://%s:%s" % (hostName, serverPort))

    try:
        # Cтарт веб-сервера в бесконечном цикле прослушивания входящих запросов
        webServer.serve_forever()
    except KeyboardInterrupt:
        # Корректный способ остановить сервер в консоли через сочетание клавиш Ctrl + C
        pass

    # Корректная остановка веб-сервера, чтобы он освободил адрес и порт в сети, которые занимал
    webServer.server_close()
    print("Server stopped.")
