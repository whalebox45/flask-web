# Flask 部落格

## 版本
`python 3.11.0`
## 套件依賴
* `click==8.1.3`
* `colorama==0.4.6`
* `Flask==2.2.2`
* `flask-paginate==2022.1.8`
* `itsdangerous==2.1.2`
* `Jinja2==3.1.2`
* `MarkupSafe==2.1.1`
* `Werkzeug==2.2.2`
## 使用說明
### 初始化 SQLite 資料庫
`flask --app main init-db`
### 資料庫綱要
```SQL
CREATE TABLE IF NOT EXISTS post(
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  title TEXT NOT NULL,
  body TEXT NOT NULL
);
```
### 啟動
`flask --app main run`
### 路徑
```
/
|---/bloglist
|   |---/page/<page>
|---/blogpost/<id>
|---/about
```
### 模板
<https://themes.3rdwavemedia.com/>