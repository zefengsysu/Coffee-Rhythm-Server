#!/usr/bin/env python3
# -*- coding: utf-8 -*-

' url handlers '

import re, time, json, logging, hashlib, base64, asyncio, os
logging.basicConfig(filename='CoffeeRhythm.log', filemode='a', level = logging.INFO)

from aiohttp import web

from coroweb import get, post
from apis import APIValueError, APIResourceNotFoundError, APIPermissionError, APIError
from models import next_id, User, Cafe, Activity, Course, Article, CommentArticle, CollectArticle, LikeArticle, Coffee, Follow, HaveCoffee, Enjoy, Join, LikeCafe, CommentCafe, CollectCafe, CollectActivity, NoteTag, HaveNoteTag, CourseTag, HaveCourseTag, Read, Look, CommentCourse, CollectCourse, LikeCourse
from config import configs

COOKIE_NAME = 'CoffeeRhythm'
_COOKIE_KEY = configs.session.secret

def check_admin(request):
    if request.__user__ is None or not request.__user__.isadmin:
        raise APIPermissionError()

# user -> user/cafe
def user2cookie(user):
    '''
    Generate cookie str by user.
    '''
    # build cookie string by: cookieKey-email-sha1
    s = '%s-%s' % (user.email, user.password)
    L = [_COOKIE_KEY, user.email, hashlib.sha1(s.encode('utf-8')).hexdigest()]
    return '-'.join(L)

async def cookie2user(cookie_str):
    '''
    Parse cookie and load user if cookie is valid.
    '''
    if not cookie_str:
        return None
    try:
        L = cookie_str.split('-')
        if len(L) != 3:
            return None
        cookieKey, email, sha1 = L
        if cookieKey != _COOKIE_KEY:
            return None
        user = await User.find([email])
        if user is None:
            return None
        s = '%s-%s' % (user.email, user.password)
        if sha1 != hashlib.sha1(s.encode('utf-8')).hexdigest():
            logging.info('invalid sha1')
            return None
        user.password = '******'
        return user
    except Exception as e:
        logging.exception(e)
        return None

async def cookie2cafe(cookie_str):
    '''
    Parse cookie and load user if cookie is valid.
    '''
    if not cookie_str:
        return None
    try:
        L = cookie_str.split('-')
        if len(L) != 3:
            return None
        cookieKey, email, sha1 = L
        if cookieKey != _COOKIE_KEY:
            return None
        cafe = await Cafe.find([email])
        if cafe is None:
            return None
        s = '%s-%s' % (cafe.email, cafe.password)
        if sha1 != hashlib.sha1(s.encode('utf-8')).hexdigest():
            logging.info('invalid sha1')
            return None
        cafe.password = '******'
        return cafe
    except Exception as e:
        logging.exception(e)
        return None

# 排序方式待修改
# 今日最佳 [ip]/api/todayBest
# 返回：增加了播放量字段looks(阅读量字段reads)、点赞量字段likes、热度heat的今日最佳详细信息
@get('/api/todayBest')
async def api_todayBest():
    contentsDict = dict()
    articles = await Article.findAll(str(time.time()) + '- created_at <= 604800.0') #
    for article in articles:
        reads = await Read.findAll('article=?', [article.idarticle])
        article.reads = len(reads)
        likes = await LikeArticle.findAll('article=?', [article.idarticle])
        article.likes = len(likes)
        article.heat = article.reads * 5 + article.likes * 5
        contentsDict[article.heat] = article
    courses = await Course.findAll(str(time.time()) + '- created_at <= 604800.0') #
    for course in courses:
        looks = await Look.findAll('course=?', [course.idcourse])
        course.looks = len(looks)
        likes = await LikeCourse.findAll('course=?', [course.idcourse])
        course.likes = len(likes)
        course.heat = course.looks * 5 + course.likes * 5
        contentsDict[course.heat] = course
    contents = sorted(contentsDict.items(), key=lambda d:d[0], reverse=True)
    todayBest = dict()
    for content in contents:
        author = await User.find([content[1].author])
        if not author.isadmin:
            todayBest = content
            break
    r = web.Response()
    r.content_type = 'application/json'
    r.body = json.dumps(todayBest, ensure_ascii=False).encode('utf-8')
    return r

# 排序方式待修改
# 精选咖啡教室 [ip]/api/courseBest
# 返回：增加了播放量字段looks、点赞量字段likes、热度heat的课程详细信息列表（最多10项）
@get('/api/courseBest')
async def api_courseBest():
    coursesDict = dict()
    courses = await Course.findAll()
    for course in courses:
        looks = await Look.findAll('course=?', [course.idcourse])
        course.looks = len(looks)
        likes = await LikeCourse.findAll('course=?', [course.idcourse])
        course.likes = len(likes)
        course.heat = course.looks * 5 + course.likes * 5
        coursesDict[course.heat] = course
    courses = sorted(coursesDict.items(), key=lambda d:d[0], reverse=True)
    if len(courses) > 10:
        courses = courses[:10]
    r = web.Response()
    r.content_type = 'application/json'
    r.body = json.dumps(courses, ensure_ascii=False).encode('utf-8')
    return r

# 排序方式待修改
# 新手必备 [ip]/api/rawBest
# 返回：课程详细信息列表（最多10项）
@get('/api/rawBest')
async def api_rawBest():
    courses = await Course.findAll('israwbest=true')
    if len(courses) > 10:
        courses = courses[:10]
    r = web.Response()
    r.content_type = 'application/json'
    r.body = json.dumps(courses, ensure_ascii=False).encode('utf-8')
    return r

# 排序方式待修改
# 最佳手记 [ip]/api/noteBest
# 返回：增加了阅读量字段reads、点赞量字段likes、热度heat的手记详细信息列表（最多10项）
@get('/api/noteBest')
async def api_noteBest():
    notesDict = dict()
    notes = await Article.findAll()
    for note in notes:
        reads = await Read.findAll('article=?', [note.idarticle])
        note.reads = len(reads)
        likes = await LikeArticle.findAll('article=?', [note.idarticle])
        note.likes = len(likes)
        note.heat = note.reads * 5 + note.likes * 5
        notesDict[note.heat] = note
    notes = sorted(notesDict.items(), key=lambda d:d[0], reverse=True)
    if len(notes) > 10:
        notes = notes[:10]
    r = web.Response()
    r.content_type = 'application/json'
    r.body = json.dumps(notes, ensure_ascii=False).encode('utf-8')
    return r

# 用户/咖啡馆退出登录 [ip]/api/signout
# 返回："Sign out successfully.", 响应头cookie行用于替换原来客户端保存cookie值, 断开会话连接
# 出错则返回json格式错误信息
@get('/api/signout')
def api_signout(request):
    user = request.__user__
    if user is None:
        raise APIPermissionError('Please signin first.')
    r = web.Response(text='Sign out successfully.')
    r.set_cookie(COOKIE_NAME, '-deleted-', httponly=True)
    logging.info('user signed out.')
    return r

# 获取课程的所有标签 [ip]/api/tag/course
# 返回：课程的所有标签的列表
@get('/api/tag/course')
async def api_tag_course():
    courseTags = await CourseTag.findAll()
    courseTags = list(map(lambda t:t.name, courseTags))
    r = web.Response()
    r.content_type = 'application/json'
    r.body = json.dumps(courseTags, ensure_ascii=False).encode('utf-8')
    return r

# 获取手记的标签 [ip]/api/tag/article
# 前端: get queryParam: article
# article -> article.idarticle
# 返回：该手记的标签列表
@get('/api/tag/article/{article}')
async def api_tag_article(article):
    haveNoteTags = await HaveNoteTag.findAll('note=?', [article])
    noteTags = list(map(lambda t: t.tag, haveNoteTags))
    r = web.Response()
    r.content_type = 'application/json'
    r.body = json.dumps(noteTags, ensure_ascii=False).encode('utf-8')
    return r

# 获取课程播放量、点赞量、评论量 [ip]/api/number/course
# 前端: get queryParam: course
# course -> course.idcourse
# 返回：增加了播放量字段looks、点赞量字段likes和评论量comments和的课程信息
# 出错则返回json格式错误信息
@get('/api/number/course/{course}')
async def api_number_course(course):
    theCourse = await Course.find([course])
    if theCourse is None:
        raise APIResourceNotFoundError('course', course)
    looks = await Look.findAll('course=?', [course])
    likes = await LikeCourse.findAll('course=?', [course])
    comments = await CommentCourse.findAll('about=?', [course])
    theCourse.looks = len(looks)
    theCourse.likes = len(likes)
    theCourse.comments = len(comments)
    r = web.Response()
    r.content_type = 'application/json'
    r.body = json.dumps(theCourse, ensure_ascii=False).encode('utf-8')
    return r

# 获取文章阅读量、点赞量、评论量 [ip]/api/number/article
# 前端: get queryParam: article
# article -> article.idarticle
# 返回：增加了阅读量字段reads、点赞量字段likes和评论量comments的文章信息
# 出错则返回json格式错误信息
@get('/api/number/article/{article}')
async def api_number_article(article):
    theArticle = await Article.find([article])
    if theArticle is None:
        raise APIResourceNotFoundError('article', article)
    reads = await Read.findAll('article=?', [article])
    likes = await LikeArticle.findAll('article=?', [article])
    comments = await CommentArticle.findAll('about=?', [article])
    theArticle.reads = len(reads)
    theArticle.likes = len(likes)
    theArticle.comments = len(comments)
    r = web.Response()
    r.content_type = 'application/json'
    r.body = json.dumps(theArticle, ensure_ascii=False).encode('utf-8')
    return r

# 获取课程评论 [ip]/api/comment/course
# 前端: get queryParam: course
# course -> course.idcourse
# 返回：该课程评论详细信息的列表, 从最新到最老排序
# 出错则返回json格式错误信息
@get('/api/comment/course/{course}')
async def api_comment_course(course):
    theCourse = await Course.find([course])
    if theCourse is None:
        raise APIResourceNotFoundError('course', course)
    comments = await CommentCourse.findAll('about=?', [course], orderBy='created_at desc')
    r = web.Response()
    r.content_type = 'application/json'
    r.body = json.dumps(comments, ensure_ascii=False).encode('utf-8')
    return r

# 获取文章评论 [ip]/api/comment/article
# 前端: get queryParam: article
# article -> article.idarticle
# 返回：该文章评论详细信息的列表, 从最新到最老排序
# 出错则返回json格式错误信息
@get('/api/comment/article/{article}')
async def api_comment_article(article):
    theArticle = await Article.find([article])
    if theArticle is None:
        raise APIResourceNotFoundError('article', article)
    comments = await CommentArticle.findAll('about=?', [article], orderBy='created_at desc')
    r = web.Response()
    r.content_type = 'application/json'
    r.body = json.dumps(comments, ensure_ascii=False).encode('utf-8')
    return r

# 排序方式待修改
# 获取课程相关手记 [ip]/api/relative/course
# 前端: get queryParam: course
# course -> course.idcourse
# 返回：该课程相关手记详细信息的列表, 从阅读量最高到最低排序
# 出错则返回json格式错误信息
@get('/api/relative/course/{course}')
async def api_relative_course(course):
    theCourse = await Course.find([course])
    if theCourse is None:
        raise APIResourceNotFoundError('course', course)
    notes = await Article.findAll('about_course=?', [course])
    notesDict = dict()
    for note in notes:
        reads = await Read.findAll('article=?', [note.idarticle])
        note.reads = len(reads)
        notesDict[note.reads] = note
    notes = sorted(notesDict.items(), key=lambda d:d[0], reverse=True)
    r = web.Response()
    r.content_type = 'application/json'
    r.body = json.dumps(notes, ensure_ascii=False).encode('utf-8')
    return r

# 获取手记相关课程 [ip]/api/relative/note
# 前端: get queryParam: note
# note -> article.idarticle
# 返回：该手记相关课程
# 出错则返回json格式错误信息
@get('/api/relative/note/{note}')
async def api_relative_note(note):
    note = await Article.find([note])
    if note is None:
        raise APIResourceNotFoundError('note', note)
    if not note.about_course:
        raise APIPermissionError('Relative course not exist.')
    course = await Course.find([note.about_course])
    r = web.Response()
    r.content_type = 'application/json'
    r.body = json.dumps(course, ensure_ascii=False).encode('utf-8')
    return r

# 排序方式待修改
# 获取标签相关课程 [ip]/api/relative/tag
# 前端: get queryParam: tag
# tag -> tag.name
# 返回：该标签相关课程详细信息的列表, 从播放量最高到最低排序
# 出错则返回json格式错误信息
@get('/api/relative/tag/{tag}')
async def api_relative_tag(tag):
    theTag = await CourseTag.find([tag])
    if theTag is None:
        raise APIResourceNotFoundError('tag', tag)
    haveCourseTags = await HaveCourseTag.findAll('tag=?', [tag])
    coursesDict = dict()
    for haveCourseTag in haveCourseTags:
        course = await Course.find([haveCourseTag.course])
        looks = await Look.findAll('course=?', [haveCourseTag.course])
        course.looks = len(looks)
        coursesDict[course.looks] = course
    courses = sorted(coursesDict.items(), key=lambda d:d[0], reverse=True)
    r = web.Response()
    r.content_type = 'application/json'
    r.body = json.dumps(courses, ensure_ascii=False).encode('utf-8')
    return r

# 获取内容作者 [ip]/api/author
# 前端: get queryParam: email
# email -> user.email
# 返回：作者详细信息
# 出错则返回json格式错误信息
@get('/api/author/{email}')
async def api_author(email):
    author = await User.find([email])
    if author is None:
        raise APIResourceNotFoundError('user', email)
    r = web.Response()
    r.content_type = 'application/json'
    r.body = json.dumps(author, ensure_ascii=False).encode('utf-8')
    return r

_RE_EMAIL = re.compile(r'^[a-z0-9\.\-\_]+\@[a-z0-9\-\_]+(\.[a-z0-9\-\_]+){1,4}$')
_RE_SHA1 = re.compile(r'^[0-9a-f]{40}$')

# 用户注册 [ip]/api/register/user
# 前端: post formData: email, password(sha1加密), nickname, city
# email, password值不能为空
# Content-Type:application/x-www-form-urlencoded
# 交互: 默认用户昵称，默认用户头像
# 返回：用户信息, 响应头cookie行用于会话保持
# 出错则返回json格式错误信息
# 测试：/static/register_user.html
@post('/api/register/user')
async def api_register_user(*, email, password, nickname, city):
    if not email or not _RE_EMAIL.match(email):
        raise APIValueError('email')
    if not password or not _RE_SHA1.match(password):
        raise APIValueError('password')
    users = await User.findAll('email=?', [email])
    if len(users) > 0:
        raise APIError('register:failed', 'email', 'Email is already in use.')
    user = User(email=email, password=password, 
                nickname=nickname or '咖友', city=city, 
                avatar='/static/img/user.png')
    await user.save()
    # make session cookie:
    r = web.Response()
    r.set_cookie(COOKIE_NAME, user2cookie(user), httponly=True)
    user.password = '******'
    r.content_type = 'application/json'
    r.body = json.dumps(user, ensure_ascii=False).encode('utf-8')
    return r

# 咖啡馆注册 [ip]/api/register/cafe
# 前端: post formData: email, password(sha1加密), name, city, address
# 参数值皆不能为空
# Content-Type:application/x-www-form-urlencoded
# 交互: 默认咖啡馆图片
# 返回：咖啡馆信息, 响应头cookie行用于会话保持
# 出错则返回json格式错误信息
# 测试：/static/register_cafe.html
@post('/api/register/cafe')
async def api_register_cafe(*, email, password, name, city, address):
    if not email or not _RE_EMAIL.match(email):
        raise APIValueError('email')
    if not password or not _RE_SHA1.match(password):
        raise APIValueError('password')
    if not name:
        raise APIValueError('name')
    if not city:
        raise APIValueError('city')
    if not address:
        raise APIValueError('address')
    cafes = await Cafe.findAll('email=?', [email])
    if len(cafes) > 0:
        raise APIError('register:failed', 'email', 'Email is already in use.')
    cafe = Cafe(email=email, password=password,
                name=name, city=city, address=address, 
                image='/static/img/cafe.png')
    await cafe.save()
    # make session cookie:
    r = web.Response()
    r.set_cookie(COOKIE_NAME, user2cookie(cafe), httponly=True)
    cafe.password = '******'
    r.content_type = 'application/json'
    r.body = json.dumps(cafe, ensure_ascii=False).encode('utf-8')
    return r

# 用户登录 [ip]/api/signin/user
# 前端: post formData: email, password(sha1加密)
# Content-Type:application/x-www-form-urlencoded
# 返回：用户信息, 响应头cookie行用于会话保持
# 出错则返回json格式错误信息
# 测试：/static/signin_user.html
@post('/api/signin/user')
async def api_signin_user(*, email, password):
    if not email or not _RE_EMAIL.match(email):
        raise APIValueError('email')
    if not password or not _RE_SHA1.match(password):
        raise APIValueError('password')
    users = await User.findAll('email=?', [email])
    if len(users) == 0:
        raise APIValueError('email', 'Email not exist.')
    user = users[0]
    # check password:
    if user.password != password:
        raise APIValueError('password', 'Invalid password.')
    # authenticate ok, set cookie:
    r = web.Response()
    r.set_cookie(COOKIE_NAME, user2cookie(user), httponly=True)
    user.passwd = '******'
    r.content_type = 'application/json'
    r.body = json.dumps(user, ensure_ascii=False).encode('utf-8')
    return r

# 咖啡馆登录 [ip]/api/signin/cafe
# 前端: post formData: email, password(sha1加密)
# Content-Type:application/x-www-form-urlencoded
# 返回：用户信息, 响应头cookie行用于会话保持
# 出错则返回json格式错误信息
# 测试：/static/signin_cafe.html
@post('/api/signin/cafe')
async def api_signin_cafe(*, email, password):
    if not email or not _RE_EMAIL.match(email):
        raise APIValueError('email')
    if not password or not _RE_SHA1.match(password):
        raise APIValueError('password')
    cafes = await Cafe.findAll('email=?', [email])
    if len(cafes) == 0:
        raise APIValueError('email', 'Email not exist.')
    cafe = cafes[0]
    # check password:
    if cafe.password != password:
        raise APIValueError('password', 'Invalid password.')
    # authenticate ok, set cookie:
    r = web.Response()
    r.set_cookie(COOKIE_NAME, user2cookie(cafe), httponly=True)
    cafe.passwd = '******'
    r.content_type = 'application/json'
    r.body = json.dumps(cafe, ensure_ascii=False).encode('utf-8')
    return r

# 图片上传 [ip]/api/upload/image
# 前端: post formData: image
# Content-Type:multipart/form-data
# 返回：上传的image对应的url
# 出错则返回json格式错误信息
# 测试：/static/upload_image.html
@post('/api/upload/image')
async def api_upload_image(request):
    check_admin(request)
    user = request.__user__
    if user is None:
        raise APIPermissionError('Please signin first.')
    reader = await request.multipart()
    image = await reader.next()
    with open(os.path.join('../Coffee Rhythm Server/static/img/', image.filename), 'wb') as f:
        while True:
            chunk = await image.read_chunk()  # 8192 bytes by default.
            if not chunk:
                break
            f.write(chunk)
    return web.Response(text='/static/img/' + image.filename)

# 视频上传 [ip]/api/upload/video
# 前端: post formData: video
# Content-Type:multipart/form-data
# 返回：上传的video对应的url
# 出错则返回json格式错误信息
# 测试：/static/upload_video.html
@post('/api/upload/video')
async def api_upload_video(request):
    check_admin(request)
    user = request.__user__
    if user is None:
        raise APIPermissionError('Please signin first.')
    reader = await request.multipart()
    video = await reader.next()
    with open(os.path.join('../Coffee Rhythm Server/static/video/', video.filename), 'wb') as f:
        while True:
            chunk = await video.read_chunk()  # 8192 bytes by default.
            if not chunk:
                break
            f.write(chunk)
    return web.Response(text='/static/video/' + video.filename)

# 修改用户信息 [ip]/api/update/userInfo
# 前端: post formData: nickname, avatar, introduction, city
# 参数值皆可为空
# Content-Type:application/x-www-form-urlencoded
# 请求头携带cookie信息
# 返回：用户信息
# 出错则返回json格式错误信息
# 测试：/static/update_userInfo.html
@post('/api/update/userInfo')
async def api_update_userInfo(request, *, nickname, avatar, introduction, city):
    user = request.__user__
    if user is None:
        raise APIPermissionError('Please signin first.')
    if avatar and not os.path.exists('../Coffee Rhythm Server' + avatar):
        raise APIResourceNotFoundError('avatar', avatar)
    user.nickname = nickname or '咖友'
    user.avatar = avatar or '/static/img/user.png'
    user.introduction = introduction
    user.city = city
    await user.update() 
    r = web.Response()
    user.password = '******'
    r.content_type = 'application/json'
    r.body = json.dumps(user, ensure_ascii=False).encode('utf-8')
    return r

# 修改咖啡馆信息 [ip]/api/update/cafeInfo
# 前端: post formData: image, introduction
# 参数值皆可为空
# Content-Type:application/x-www-form-urlencoded
# 请求头携带cookie信息
# 返回：咖啡馆信息
# 出错则返回json格式错误信息
# 测试：/static/update_cafeInfo.html
# 测试时需先缓存一次update_cafeInfo.html
@post('/api/update/cafeInfo')
async def api_update_cafeInfo(request, *, image, introduction):
    cafe, cookie_str = None, request.cookies.get(COOKIE_NAME)
    if cookie_str:
        cafe = await cookie2cafe(cookie_str)
    if cafe is None:
        raise APIPermissionError('Please signin first.')
    if image and not os.path.exists('../Coffee Rhythm Server' + image):
        raise APIResourceNotFoundError('image', image)
    cafe.image = image
    cafe.introduction = introduction
    await cafe.update() 
    r = web.Response()
    cafe.password = '******'
    r.content_type = 'application/json'
    r.body = json.dumps(cafe, ensure_ascii=False).encode('utf-8')
    return r

# 上传用户喜好 [ip]/api/update/userEnjoy
# 前端: post formData: enjoy_sugar, enjoy_milk, single_espresso
# 参数值皆不能为空
# Content-Type:application/x-www-form-urlencoded
# enjoy_sugar, enjoy_milk, single_espresso: '1' => true, '0' => false
# 请求头携带cookie信息
# 返回：用户信息
# 出错则返回json格式错误信息
# 测试：/static/update_userEnjoy.html
# 测试时需先缓存一次update_userEnjoy.html
@post('/api/update/userEnjoy')
async def api_update_userEnjoy(request, *, enjoy_sugar, enjoy_milk, single_espresso):
    user = request.__user__
    if user is None:
        raise APIPermissionError('Please signin first.')
    enjoy_sugar = True if enjoy_sugar == '1' else False
    enjoy_milk = True if enjoy_milk == '1' else False
    single_espresso = True if single_espresso == '1' else False
    user.enjoy_sugar = enjoy_sugar
    user.enjoy_milk = enjoy_milk
    user.single_espresso = single_espresso
    await user.update() 
    r = web.Response()
    user.password = '******'
    r.content_type = 'application/json'
    r.body = json.dumps(user, ensure_ascii=False).encode('utf-8')
    return r

# 上传课程 [ip]/api/upload/course
# 前端: post formData: image, name, introduction, video
# image, name, video值不能为空
# Content-Type:application/x-www-form-urlencoded
# image -> url, 从视频中截取的一帧图片
# video -> url
# 请求头携带cookie信息
# 交互：课程默认显示图片
# 返回：课程信息
# 出错则返回json格式错误信息
# 测试：/static/upload_course.html
# 测试时需先缓存一次upload_course.html
@post('/api/upload/course')
async def api_upload_course(request, *, image, name, introduction, video):
    user = request.__user__
    if user is None:
        raise APIPermissionError('Please signin first.')
    if image and not os.path.exists('../Coffee Rhythm Server' + image):
        raise APIResourceNotFoundError('image', image)
    if not video or not os.path.exists('../Coffee Rhythm Server' + video):
        raise APIResourceNotFoundError('video', video)
    course = Course(image=image or '/static/img/course.png', name=name, author=user.email, introduction=introduction, video=video)
    await course.save()
    r = web.Response()
    r.content_type = 'application/json'
    r.body = json.dumps(course, ensure_ascii=False).encode('utf-8')
    return r

# 超级用户发布百科 [ip]/api/publish/knowledge
# 前端: post formData: image, name, content, family
# name, content, family值不能为空
# Content-Type:multipart/form-data
# image -> url
# content -> html文件
# 请求头携带cookie信息
# 交互：百科文章默认显示图片
# 返回：百科信息
# 出错则返回json格式错误信息
# 测试：/static/publish_knowledge.html
# 测试时需先缓存一次publish_knowledge.html
@post('/api/publish/knowledge')
async def api_publish_knowledge(request):
    data = await request.post()
    image, name, content, family = data['image'], data['name'], data['content'], data['family']
    user = request.__user__
    if user is None:
        raise APIPermissionError('Please signin first.')
    check_admin(request)
    if not os.path.exists('../Coffee Rhythm Server' + image):
        raise APIResourceNotFoundError('image', image)
    with open(os.path.join('../Coffee Rhythm Server/static/article/', content.filename), 'wb') as f:
        f.write(content.file.read())
    content = '/static/article/' + content.filename
    article = Article(image=image or '/static/img/knowledge.png', name=name, author=user.email, content=content, family=family, isknowledge=True)
    await article.save()
    r = web.Response()
    r.content_type = 'application/json'
    r.body = json.dumps(article, ensure_ascii=False).encode('utf-8')
    return r

# 发布手记 [ip]/api/publish/note
# 前端: post formData: image, name, content, about_cafe, about_course
# name, content值不能为空
# Content-Type:multipart/form-data
# image -> url
# content -> html文件
# about_cafe -> cafe.email
# about_course -> course.idcourse
# 请求头携带cookie信息
# 交互：手记文章默认显示图片
# 返回：手记信息
# 出错则返回json格式错误信息
# 测试：/static/publish_note.html
# 测试时需先缓存一次publish_note.html
@post('/api/publish/note')
async def api_publish_note(request):
    data = await request.post()
    image, name, content, about_cafe, about_course = data['image'], data['name'], data['content'], data['about_cafe'], data['about_course']
    user = request.__user__
    if user is None:
        raise APIPermissionError('Please signin first.')
    if not os.path.exists('../Coffee Rhythm Server' + image):
        raise APIResourceNotFoundError('image', image)
    if about_cafe and Cafe.find([about_cafe]) is None:
        raise APIResourceNotFoundError('about_cafe', about_cafe)
    if about_course and Course.find([about_course]) is None:
        raise APIResourceNotFoundError('about_course', about_course)
    with open(os.path.join('../Coffee Rhythm Server/static/article/', content.filename), 'wb') as f:
        f.write(content.file.read())
    content = '/static/article/' + content.filename
    if about_cafe:
        article = Article(image=image or '/static/img/note.png', name=name, author=user.email, content=content, about_cafe=about_cafe, isnote=True)
    elif about_course:
        article = Article(image=image or '/static/img/note.png', name=name, author=user.email, content=content, about_course=about_course, isnote=True)
    else:
        article = Article(image=image or '/static/img/note.png', name=name, author=user.email, content=content, isnote=True)
    await article.save()
    r = web.Response()
    r.content_type = 'application/json'
    r.body = json.dumps(article, ensure_ascii=False).encode('utf-8')
    return r

# 发布需求 [ip]/api/publish/demand
# 前端: post formData: image, name, content, about_drink
# 参数皆不能为空值
# Content-Type:multipart/form-data
# image -> url
# content -> html文件
# about_drink: 喝咖啡 -> true, 做咖啡 -> false '1' => true, '0' => false  
# 请求头携带cookie信息
# 交互：需求文章默认显示图片
# 返回：需求信息
# 出错则返回json格式错误信息
# 测试：/static/publish_demand.html
# 测试时需先缓存一次publish_demand.html
@post('/api/publish/demand')
async def api_publish_demand(request):
    data = await request.post()
    image, name, content, about_drink = data['image'], data['name'], data['content'], data['about_drink']
    user = request.__user__
    if user is None:
        raise APIPermissionError('Please signin first.')
    if not os.path.exists('../Coffee Rhythm Server' + image):
        raise APIResourceNotFoundError('image', image)
    with open(os.path.join('../Coffee Rhythm Server/static/article/', content.filename), 'wb') as f:
        f.write(content.file.read())
    content = '/static/article/' + content.filename
    article = Article(image=image or '/static/img/demand.png', name=name, author=user.email, content=content, about_drink=about_drink, isdemand=True)
    await article.save()
    r = web.Response()
    r.content_type = 'application/json'
    r.body = json.dumps(article, ensure_ascii=False).encode('utf-8')
    return r

# 课程添加标签 [ip]/api/add/courseTag
# 前端: post formData: course, tag
# 参数皆不能为空值
# Content-Type:application/x-www-form-urlencoded
# course -> course.idcourse
# tag -> courseTag.name
# 请求头携带cookie信息
# 返回：添加标签信息
# 出错则返回json格式错误信息
# 测试：/static/add_courseTag.html
# 测试时需先缓存一次add_courseTag.html
@post('/api/add/courseTag')
async def api_add_courseTag(request, *, course, tag):
    user = request.__user__
    if user is None:
        raise APIPermissionError('Please signin first.')
    theTag = await CourseTag.find([tag])
    if theTag is None:
        raise APIResourceNotFoundError('tag', tag)
    theCourse = await Course.find([course])
    if theCourse is None:
        raise APIResourceNotFoundError('course', course)
    elif theCourse.author != user.email:
        raise APIPermissionError('Adding tag to other\'s course is not permitted.')
    haveCourseTag = HaveCourseTag(course=course, tag=tag)
    await haveCourseTag.save()
    r = web.Response()
    r.content_type = 'application/json'
    r.body = json.dumps(haveCourseTag, ensure_ascii=False).encode('utf-8')
    return r

# 手记添加标签 [ip]/api/add/noteTag
# 前端: post formData: note, tag
# 参数皆不能为空值
# Content-Type:application/x-www-form-urlencoded
# note -> article.idarticle
# tag -> noteTag.name
# 请求头携带cookie信息
# 返回：添加标签信息
# 出错则返回json格式错误信息
# 测试：/static/add_noteTag.html
# 测试时需先缓存一次add_noteTag.html
@post('/api/add/noteTag')
async def api_add_noteTag(request, *, note, tag):
    user = request.__user__
    if user is None:
        raise APIPermissionError('Please signin first.')
    article = await Article.find([note])
    if article is None or article.isnote == False:
        raise APIResourceNotFoundError('note', note)
    theTag = await NoteTag.find([tag])
    if theTag is None:
        raise APIResourceNotFoundError('tag', tag)
    elif article.author != user.email:
        raise APIPermissionError('Adding tag to other\'s note is not permitted.')
    haveNoteTag = HaveNoteTag(note=note, tag=tag)
    await haveNoteTag.save()
    r = web.Response()
    r.content_type = 'application/json'
    r.body = json.dumps(haveNoteTag, ensure_ascii=False).encode('utf-8')
    return r

# 发布课程评论 [ip]/api/publish/commentCourse
# 前端: post formData: reply_to, content, about
# content, about不能为空值
# Content-Type:application/x-www-form-urlencoded
# reply_to -> commentCourse.idcomment_course
# about -> course.idcourse
# 请求头携带cookie信息
# 返回：课程评论信息
# 出错则返回json格式错误信息
# 测试：/static/publish_commentCourse.html
# 测试时需先缓存一次publish_commentCourse.html
@post('/api/publish/commentCourse')
async def api_publish_commentCourse(request, *, reply_to, content, about):
    user = request.__user__
    if user is None:
        raise APIPermissionError('Please signin first.')
    comment = await CommentCourse.find([reply_to])
    if reply_to and comment is None:
        raise APIResourceNotFoundError('comment', reply_to)
    if reply_to and comment.about != about:
        raise APIValueError('course', about)
    theCourse = await Course.find([about])
    if theCourse is None:
        raise APIResourceNotFoundError('course', about)
    if reply_to:
        commentCourse = CommentCourse(created_from=user.email, reply_to=reply_to, content=content, about=about)
    else:
        commentCourse = CommentCourse(created_from=user.email, content=content, about=about)
    await commentCourse.save()
    r = web.Response()
    r.content_type = 'application/json'
    r.body = json.dumps(commentCourse, ensure_ascii=False).encode('utf-8')
    return r

# 发布文章评论 [ip]/api/publish/commentArticle
# 前端: post formData: reply_to, content, about
# content, about不能为空值
# Content-Type:application/x-www-form-urlencoded
# reply_to -> commentArticle.idcomment_article
# about -> article.idarticle
# 请求头携带cookie信息
# 返回：文章评论信息
# 出错则返回json格式错误信息
# 测试：/static/publish_commentArticle.html
# 测试时需先缓存一次publish_commentCourse.html
@post('/api/publish/commentArticle')
async def api_publish_commentArticle(request, *, reply_to, content, about):
    user = request.__user__
    if user is None:
        raise APIPermissionError('Please signin first.')
    comment = await CommentArticle.find([reply_to])
    if reply_to and comment is None:
        raise APIResourceNotFoundError('comment', reply_to)
    if reply_to and comment.about != about:
        raise APIValueError('article', about)
    theArticle = await Article.find([about])
    if theArticle is None:
        raise APIResourceNotFoundError('article', about)
    if reply_to:
        commentArticle = CommentArticle(created_from=user.email, reply_to=reply_to, content=content, about=about)
    else:
        commentArticle = CommentArticle(created_from=user.email, content=content, about=about)
    await commentArticle.save()
    r = web.Response()
    r.content_type = 'application/json'
    r.body = json.dumps(commentArticle, ensure_ascii=False).encode('utf-8')
    return r

# 增加文章点赞量 [ip]/api/like/article
# 前端: post formData: article
# 参数不能为空值
# Content-Type:application/x-www-form-urlencoded
# article -> article.idarticle
# 请求头携带cookie信息
# 返回：增加文章点赞量信息
# 出错则返回json格式错误信息
# 测试：/static/like_article.html
# 测试时需先缓存一次like_article.html
@post('/api/like/article')
async def api_like_article(request, *, article):
    user = request.__user__
    if user is None:
        raise APIPermissionError('Please signin first.')
    theArticle = await Article.find([article])
    if theArticle is None:
        raise APIResourceNotFoundError('article', article)
    likeArticle = LikeArticle(user=user.email, article=article)
    await likeArticle.save()
    r = web.Response()
    r.content_type = 'application/json'
    r.body = json.dumps(likeArticle, ensure_ascii=False).encode('utf-8')
    return r

# 增加课程点赞量 [ip]/api/like/course
# 前端: post formData: course
# 参数不能为空值
# Content-Type:application/x-www-form-urlencoded
# course -> course.idcourse
# 请求头携带cookie信息
# 返回：增加课程点赞量信息
# 出错则返回json格式错误信息
# 测试：/static/like_course.html
# 测试时需先缓存一次like_course.html
@post('/api/like/course')
async def api_like_course(request, *, course):
    user = request.__user__
    if user is None:
        raise APIPermissionError('Please signin first.')
    theCourse = await Course.find([course])
    if theCourse is None:
        raise APIResourceNotFoundError('course', course)
    likeCourse = LikeCourse(user=user.email, course=course)
    await likeCourse.save()
    r = web.Response()
    r.content_type = 'application/json'
    r.body = json.dumps(likeCourse, ensure_ascii=False).encode('utf-8')
    return r

# 增加文章阅读量 [ip]/api/read
# 前端: post formData: article
# 参数不能为空值
# Content-Type:application/x-www-form-urlencoded
# article -> article.idarticle
# 请求头携带cookie信息
# 返回：增加文章阅读量信息
# 出错则返回json格式错误信息
# 测试：/static/read.html
# 测试时需先缓存一次read.html
@post('/api/read')
async def api_read(request, *, article):
    user = request.__user__
    if user is None:
        raise APIPermissionError('Please signin first.')
    theArticle = await Article.find([article])
    if theArticle is None:
        raise APIResourceNotFoundError('article', article)
    read = Read(user=user.email, article=article)
    await read.save()
    r = web.Response()
    r.content_type = 'application/json'
    r.body = json.dumps(read, ensure_ascii=False).encode('utf-8')
    return r

# 增加课程播放量 [ip]/api/look
# 前端: post formData: course
# 参数不能为空值
# Content-Type:application/x-www-form-urlencoded
# course -> course.idcourse
# 请求头携带cookie信息
# 返回：增加课程播放量信息
# 出错则返回json格式错误信息
# 测试：/static/look.html
# 测试时需先缓存一次look.html
@post('/api/look')
async def api_look(request, *, course):
    user = request.__user__
    if user is None:
        raise APIPermissionError('Please signin first.')
    theCourse = await Course.find([course])
    if theCourse is None:
        raise APIResourceNotFoundError('course', course)
    look = Look(user=user.email, course=course)
    await look.save()
    r = web.Response()
    r.content_type = 'application/json'
    r.body = json.dumps(look, ensure_ascii=False).encode('utf-8')
    return r
