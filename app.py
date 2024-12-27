from flask import Flask, render_template, request, session, url_for, redirect
import datetime

app = Flask(__name__)
app.secret_key = "super_secret_key"


@app.route("/", methods=['GET'])
def main():
    # Проверяем, установлена ли тема пользователем
    dark = session.get("dark")

    # Если пользователь ещё не выбрал тему, устанавливаем её на основе времени суток
    if dark is None:
        current_hour = datetime.datetime.now().hour
        # Темная тема ночью (с 19:00 до 7:00), светлая тема днём
        dark = 19 <= current_hour or current_hour < 7
        session["dark"] = dark

    lang = session.get("lang", "en")  # По умолчанию английский язык
    return render_template("index.html", dark=dark, lang=lang)


@app.route("/switch_theme/", methods=["POST"])
def switch_theme():
    # Меняем тему, выбранную пользователем, и сохраняем в сессии
    selected_theme = request.form.get("theme")
    session["dark"] = (selected_theme == "dark")
    return redirect(url_for("main"))


@app.route("/switch_language/", methods=["POST"])
def switch_language():
    selected_language = request.form.get("lang")
    session["lang"] = selected_language  # Сохраняем выбранный язык в сессии
    return redirect(url_for("main"))


@app.errorhandler(404)
def render_not_found(error):
    return "Ничего не нашлось! Вот неудача, отправляйтесь на главную!"


@app.errorhandler(500)
def render_server_error(error):
    return "Что-то не так, но мы все починим"


if __name__ == '__main__':
    app.run(port=5002, debug=True)
