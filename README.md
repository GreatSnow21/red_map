# Красная карта Санкт-Петербурга 🗺️

Интерактивный ГИС-сервис для пространственного анализа и визуализации геоданных аварийных и утраченных домов на карте Санкт-Петербурга. Проект разработан в качестве практической реализации в рамках магистерской диссертации.

## 🛠 Технологический стек

* **Backend:** Python, Django, Django REST Framework (DRF)
* **GIS & Database:** PostgreSQL + PostGIS, Django GIS (GDAL/PROJ)
* **Frontend/Map:** Leaflet.js, Django Bootstrap 5
* **API:** RESTful API (rest_framework_gis)

## 📂 Структура проекта

```text
red_map/
├── map/                  # Основное приложение (ГИС-логика и интерфейс)
│   ├── migrations/       # Миграции базы данных
│   ├── templates/        # HTML-шаблоны (index, routes, assistant и др.)
│   ├── utils/            # Вспомогательные скрипты и логика
│   ├── api_views.py      # Обработчики REST API для отдачи GeoJSON
│   ├── forms.py          # Формы Django
│   ├── models.py         # Модели данных (в т.ч. геометрия PostGIS)
│   ├── serializers.py    # Сериализаторы DRF
│   ├── urls.py           # Маршрутизация приложения map
│   └── views.py          # Основные контроллеры (представления)
├── red_map/              # Главный конфигурационный модуль проекта
│   ├── asgi.py / wsgi.py # Точки входа для веб-серверов
│   ├── settings.py       # Настройки проекта (безопасная загрузка из .env)
│   └── urls.py           # Главный роутер проекта
├── .env                  # Локальные переменные окружения (исключен из Git)
├── .gitignore            # Файл исключений Git
├── GDAL-*.whl            # Предзагруженный бинарный пакет GDAL (для Windows)
└── manage.py             # Утилита управления Django-проектом

```

## 🚀 Локальный запуск (Разработка)

Для запуска проекта на вашем локальном компьютере выполните следующие шаги:

### 1. Клонирование репозитория

```bash
git clone [https://github.com/GreatSnow21/red_map.git](https://github.com/GreatSnow21/red_map.git)
cd red_map

```

### 2. Настройка виртуального окружения

```bash
python -m venv venv
# Для Windows:
venv\Scripts\activate
# Для Linux/macOS:
source venv/bin/activate

```

### 3. Установка зависимостей и GDAL (для Windows)

Для работы с геоданными на Windows необходимо установить библиотеку GDAL. В корне проекта уже находится нужный `whl` файл (версия для Python 3.11).
Установите его, а затем остальные зависимости:

```bash
pip install GDAL-3.4.3-cp311-cp311-win_amd64.whl
pip install -r requirements.txt

```

### 4. Настройка переменных окружения

Создайте файл `.env` в корневой директории проекта и добавьте в него следующие переменные:

```env
DEBUG=True
SECRET_KEY=your_secret_key_here
ALLOWED_HOSTS=127.0.0.1,localhost

DB_NAME=red_map
DB_USER=your_postgres_user
DB_PASSWORD=your_postgres_password
DB_HOST=127.0.0.1
DB_PORT=5432

```

### 5. Подготовка базы данных

Убедитесь, что у вас запущен PostgreSQL с расширением PostGIS. Затем примените миграции:

```bash
python manage.py migrate

```

### 6. Запуск сервера

```bash
python manage.py runserver

```

Сервис будет доступен по адресу: http://127.0.0.1:8000/map/

---

