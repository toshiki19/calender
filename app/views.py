from fastapi import FastAPI, Request, Form, Cookie
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from starlette.status import HTTP_302_FOUND
from fastapi.staticfiles import StaticFiles
from app.configs import Config
from app.utilities.session import Session
from app.models.auth import AuthModel
from app.models.articles import ArticleModel
from app.models.events import EventModel
from app.utilities.check_login import check_login
import copy
app = FastAPI()
app.mount("/app/statics", StaticFiles(directory="app/statics"), name="static")
templates = Jinja2Templates(directory="/app/templates")
config = Config()
session = Session(config)


@app.get("/")
def index(request: Request):
    """
    トップページを返す
    :param request: Request object
    :return:
    """
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/register")
def register(request: Request):
    """
    新規登録ページ
    :param request:
    :return:
    """
    return templates.TemplateResponse("register.html", {"request": request})


@app.post("/login")
def login(request: Request, username: str = Form(...), password: str = Form(...)):
    """
    ログイン処理
    :param request:
    :param username:
    :param password:
    :return:
    """
    auth_model = AuthModel(config)
    [result, user] = auth_model.login(username, password)
    if not result:
        # ユーザが存在しなければトップページへ戻す
        return templates.TemplateResponse("index.html", {"request": request, "error": "ユーザ名またはパスワードが間違っています"})
    response = RedirectResponse("/calender", status_code=HTTP_302_FOUND)
    session_id = session.set("user", user)
    response.set_cookie("session_id", session_id)
    return response


@app.post("/register")
def create_user(request: Request, username: str = Form(...), password: str = Form(...)):
    """
    ユーザ登録をおこなう
    フォームから入力を受け取る時は，`username=Form(...)`のように書くことで受け取れる
    :param username: 登録するユーザ名
    :param password: 登録するパスワード
    :return: 登録が完了したら/blogへリダイレクト
    """

    auth_model = AuthModel(config)

    existed_sameuser = auth_model.fetch_user_by_name(username)

    if existed_sameuser:
        return templates.TemplateResponse("register.html", {
        "request": request,
        "error": "すでに同じ名前の利用者がいます"
        })

    # auth_model = AuthModel(config)
    auth_model.create_user(username, password)
    user = auth_model.find_user_by_name_and_password(username, password)
    response = RedirectResponse(url="/calender", status_code=HTTP_302_FOUND)
    session_id = session.set("user", user)
    response.set_cookie("session_id", session_id)
    return response


@app.get("/calender")
# check_loginデコレータをつけるとログインしていないユーザをリダイレクトできる
@check_login
def calender(request: Request, session_id=Cookie(default=None)):
    user_id = session.get(session_id).get("user").get("id")
    event_model = EventModel(config)
    events = event_model.fetch_recent_events(user_id)
    # print(events)

    events_new = []
    for event in events:
        # events_new = copy.deepcopy(events)
        # dates_str = str(event['dates'])
        event_new = {}
        if event['start'] is None:
            event_new['start'] = str(event['dates'])
        else:
            event_new['start'] = str(event['start'])

        event_new['id'] = event['id']
        event_new['title'] = event['title']
        event_new['body'] = event['body']

        if event['end'] != None:
            event_new['end'] = str(event['end'])

        events_new.append(event_new)
       
    return templates.TemplateResponse("calender.html", {
        "request": request,
        "events": events_new,
        "user_id": user_id
    })

@app.get("/articles")
# check_loginデコレータをつけるとログインしていないユーザをリダイレクトできる
@check_login
def articles_index(request: Request, session_id=Cookie(default=None)):
    user = session.get(session_id).get("user")
    article_model = ArticleModel(config)
    articles = article_model.fetch_recent_articles()
    # print(articles)
    return templates.TemplateResponse("article-index.html", {
        "request": request,
        "articles": articles,
        "user": user
    })

# @app.get("/articles")
# # check_loginデコレータをつけるとログインしていないユーザをリダイレクトできる
# @check_login
# def schedule_index(request: Request, session_id=Cookie(default=None)):
#     user = session.get(session_id).get("user")
#     article_model = ArticleModel(config)
#     articles = article_model.fetch_recent_articles()
#     return templates.TemplateResponse("schedule-index.html", {
#         "request": request,
#         "articles": articles,
#         "user": user
#     })


@app.get("/article/create")
@check_login
def create_article_page(request: Request, session_id=Cookie(default=None)):
    user = session.get(session_id).get("user")
    return templates.TemplateResponse("create-article.html", {"request": request, "user": user})

@app.get("/article/create")
@check_login
def create_schedule_page(request: Request, session_id=Cookie(default=None)):
    user = session.get(session_id).get("user")
    return templates.TemplateResponse("create-article.html", {"request": request, "user": user})


@app.post("/article/create")
@check_login
def post_article(title: str = Form(...), body: str = Form(...), start: str = Form(...), end: str = Form(...), session_id=Cookie(default=None)):
    article_model = ArticleModel(config)
    user_id = session.get(session_id).get("user").get("id")
    article_model.create_article(user_id, title, body, start, end)
    events_model = EventModel(config)
    events_model.create_events(user_id, title, body, start, end)
    return RedirectResponse("/articles", status_code=HTTP_302_FOUND)




@app.get("/article/{article_id}")
@check_login
def article_detail_page(request: Request, article_id: int, session_id=Cookie(default=None)):
    article_model = ArticleModel(config)
    article = article_model.fetch_article_by_id(article_id)
    user = session.get(session_id).get("user")
    return templates.TemplateResponse("article-detail.html", {
        "request": request,
        "article": article,
        "user": user
    })

@app.get("/schedule")
@check_login
def schedule_detail_page(request: Request, session_id=Cookie(default=None)):
    user_id = session.get(session_id).get("user").get("id")
    article_model = ArticleModel(config)
    
    article = article_model.fetch_article_by_id_all(user_id)
    # user_id = session.get(session_id).get("user").get("id")
    print(article)
    return templates.TemplateResponse("schedule-detail.html", {
        "request": request,
        "user_id": user_id,
        "articled": article
        
    })


@app.post("/event/create")
@check_login
def post_event(title: str = Form(...), body: str = Form(...), start: str = Form(...), end: str = Form(...), session_id=Cookie(default=None)):
    events_model = EventModel(config)
    user_id = session.get(session_id).get("user").get("id")
    events_model.create_events(user_id, title, body, start, end)
    return RedirectResponse("/calender", status_code=HTTP_302_FOUND)

@app.post("/article/change")
@check_login
def post_article_change(title: str = Form(...), body: str = Form(...), id: str = Form(...), start: str = Form(...), end: str = Form(...), session_id=Cookie(default=None)):
    
    article_model = ArticleModel(config)
    user_id = session.get(session_id).get("user").get("id")
    article_model.change_article(user_id, title, body, start, end, id)
    # events_model = EventModel(config)
    # events_model.change_events(user_id, title, body, start, end, id)
    return RedirectResponse("/articles", status_code=HTTP_302_FOUND)


@app.post("/event/change")
@check_login
def post_event_change(title: str = Form(...), body: str = Form(...), id: str = Form(...), start: str = Form(...), end: str = Form(...),  session_id=Cookie(default=None)):
    
    events_model = EventModel(config)
    user_id = session.get(session_id).get("user").get("id")
    events_model.change_events(user_id, title, body, start, end, id)
    return RedirectResponse("/calender", status_code=HTTP_302_FOUND)

@app.post("/article/delete")
@check_login
def post_article_delete(id: str = Form(...), session_id=Cookie(default=None)):
    
    article_model = ArticleModel(config)
    user_id = session.get(session_id).get("user").get("id")
    article_model.delete_article(id)
    # events_model = EventModel(config)
    # events_model.delete_events(id)
    return RedirectResponse("/articles", status_code=HTTP_302_FOUND)


@app.post("/event/delete")
@check_login
def post_event_delete(id: str = Form(...), session_id=Cookie(default=None)):
    
    events_model = EventModel(config)
    user_id = session.get(session_id).get("user").get("id")
    events_model.delete_events(id)
    return RedirectResponse("/calender", status_code=HTTP_302_FOUND)

# @app.get("/event/{event_id}")
# @check_login
# def event_detail_page(request: Request, event_id: int, session_id=Cookie(default=None)):
#     event_model = EventModel(config)
#     event = article_model.fetch_article_by_id(event_id)
#     user = session.get(session_id).get("user")
#     return templates.TemplateResponse("article-detail.html", {
#         "request": request,
#         "article": article,
#         "user": user
#     })


@app.get("/logout")
@check_login
def logout(session_id=Cookie(default=None)):
    session.destroy(session_id)
    response = RedirectResponse(url="/")
    response.delete_cookie("session_id")
    return response
