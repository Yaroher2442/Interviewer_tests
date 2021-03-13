from django.urls import path
from . import views
from .views import *

urlpatterns = [
    # path('', views.index),
    path('login', LoginFormView.as_view()),
    path('register', RegisterFormView.as_view()),
    path('logout', LogoutView.as_view()),

    path('test/all', TestAll.as_view()),
    path('test/create', TestCreatetView.as_view()),
    path('test/edit/<str:test_id>', TestEditView.as_view()),
    path('test/delite/<str:test_id>', TestDeliteView.as_view()),

    path('test/question/delite/<str:q_id>', QuestionDeliteView.as_view()),
    path('test/question/add/<str:test_id>', TestQuestionAdd.as_view()),

    path('test/user/answer/<str:test_id>', UserAnswerAdd.as_view()),
    path('test/user/answer/show/<str:test_id>', UserAnswerShow.as_view()),

    path('test/user/<str:test_id>',UserController.as_view())

]
