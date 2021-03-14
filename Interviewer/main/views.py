# response generate
from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse

# decorators
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

# auth
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.models import Group

# views
from django.views import View
# our forms
from .form import Register, CreateTestForm, CreateQuestion

# our models
from .models import Test, Question, Answer, UserAnswer
from pprint import pprint


# --------------------------------AUTH--------------------------------

@method_decorator(csrf_exempt, name='dispatch')
class LoginFormView(View):
    content = {}
    template_name = 'main/helpers/login.html'

    def get(self, request):
        return render(request, self.template_name, self.content)

    def post(self, request):
        user = authenticate(request, **request.POST.dict())
        if user is not None:
            login(request, user)
            return HttpResponseRedirect('/test/all')
        else:
            return HttpResponseRedirect('/register')


class LogoutView(View):
    def get(self, request):
        logout(request)
        return HttpResponseRedirect('/login')


@method_decorator(csrf_exempt, name='dispatch')
class RegisterFormView(View):
    context = {'form': Register()}

    def get(self, request):
        return render(request, 'main/helpers/register.html', self.context)

    def post(self, request):
        form = Register(request.POST)
        if form.is_valid():
            user = User.objects.create_user(**form.cleaned_data)
            user.save()
            group = Group.objects.get(name='users')
            user.groups.add(group)
        return HttpResponseRedirect('/login')


# --------------------------------TESTS--------------------------------

class TestAll(View):
    context = {'data': Test.objects.all()}

    def get(self, request):
        user_name = request.user.username
        user = User.objects.get(username=user_name)
        self.context['user_name'] = user_name
        if user.is_superuser!=1:
            self.context['group'] = 'users'
            return render(request, 'main/tests.html', self.context)
        else:
            self.context['group'] = 'admins'
            return render(request, 'main/tests.html', self.context)


@method_decorator(csrf_exempt, name='dispatch')
class TestCreatetView(View):
    context = {'form': CreateTestForm()}

    def get(self, request):
        user_name = request.user.username
        user = User.objects.get(username=user_name)
        self.context['user_name'] = user_name
        print(user.groups.filter(name='admins').exists())
        if user.is_superuser==1:
            return render(request, 'main/create_test.html', self.context)
        else:
            return HttpResponseRedirect('/test/all')

    def post(self, request):
        form = CreateTestForm(request.POST)
        if form.is_valid():
            print(form.cleaned_data)
            Test(**form.cleaned_data, is_active=True).save()
            return HttpResponseRedirect('/test/all')


@method_decorator(csrf_exempt, name='dispatch')
class TestEditView(View):
    context = {}

    def get(self, request, test_id):
        user_name = request.user.username
        user = User.objects.get(username=user_name)
        self.context['user_name'] = user_name
        if user.is_superuser==1:
            self.context['data'] = Test.objects.get(id=test_id)
            self.context['questions'] = Question.objects.filter(test_id=test_id)
            self.context['ans_lst'] = [Answer.objects.filter(q_id=an) for an in self.context['questions']]
            return render(request, 'main/change_test.html', self.context)
        else:
            return HttpResponseRedirect('/test/all')

    def post(self, request, test_id):
        form = CreateTestForm(request.POST)
        if form.is_valid():
            cleaned = form.cleaned_data
            test = Test.objects.get(id=test_id)
            test.title = cleaned['title']
            test.start_date = cleaned['start_date']
            test.end_date = cleaned['end_date']
            test.description = cleaned['description']
            test.save()
            return HttpResponseRedirect('/test/all')


@method_decorator(csrf_exempt, name='dispatch')
class TestDeliteView(View):
    def post(self, request, test_id):
        obj = Test.objects.get(id=test_id)
        obj.delete()
        return HttpResponseRedirect('/test/all')


@method_decorator(csrf_exempt, name='dispatch')
class QuestionDeliteView(View):
    def post(self, request, q_id):
        obj = Question.objects.get(id=q_id)
        t_id = obj.test_id.id
        obj.delete()
        return HttpResponseRedirect(f'/test/edit/{t_id}')


# --------------------------------Question--------------------------------


@method_decorator(csrf_exempt, name='dispatch')
class TestQuestionAdd(View):
    context = {'form': CreateQuestion()}

    def get(self, request, test_id):
        user_name = request.user.username
        user = User.objects.get(username=user_name)
        self.context['user_name'] = user_name
        if user.is_superuser==1:
            self.context['id'] = test_id
            self.context['test_name'] = Test.objects.get(id=test_id).title
            return render(request, 'main/add_question.html', self.context)
        else:
            return HttpResponseRedirect('/test/all')

    def post(self, request, test_id):
        r_text = request.POST.get('text')
        r_type = request.POST.get('type')
        answers = []
        counter = 1
        while request.POST.get(f'answer{counter}') != None:
            answers.append(request.POST.get(f'answer{counter}'))
            counter += 1
        t = Test.objects.get(id=test_id)
        if r_type == 'text':
            new_q = Question(test_id=t, text=r_text, type=r_type)
            new_q.save()
            Answer(q_id=new_q, text='text').save()
        else:
            new_q = Question(test_id=t, text=r_text, type=r_type)
            new_q.save()
            for ans in answers:
                if ans != '':
                    Answer(q_id=new_q, text=ans).save()
        return HttpResponseRedirect(f'/test/edit/{test_id}')


# --------------------------------UserAnswer--------------------------------


@method_decorator(csrf_exempt, name='dispatch')
class UserAnswerAdd(View):
    context = {}

    def get(self, request, test_id):
        user_name = request.user.username
        user = User.objects.get(username=user_name)
        self.context['user_name'] = user_name
        if user.is_superuser==1:
            self.context['test_id'] = test_id
            self.context['questions'] = Question.objects.filter(test_id=test_id)
            self.context['ans_lst'] = []
            self.context['test_name'] = Test.objects.get(id=test_id).title
            for qw in self.context['questions']:
                d_buf = {}
                d_buf['quest'] = qw
                d_buf['type'] = qw.type
                d_buf['answrs'] = Answer.objects.filter(q_id=qw)
                self.context['ans_lst'].append(d_buf)
            return render(request, 'main/user_answer.html', self.context)
        else:
            self.context['test_id'] = test_id
            self.context['questions'] = Question.objects.filter(test_id=test_id)
            self.context['ans_lst'] = []
            self.context['test_name'] = Test.objects.get(id=test_id).title
            for qw in self.context['questions']:
                d_buf = {}
                d_buf['quest'] = qw
                d_buf['type'] = qw.type
                d_buf['answrs'] = Answer.objects.filter(q_id=qw)
                self.context['ans_lst'].append(d_buf)
            return render(request, 'main/user_answer.html', self.context)

    def post(self, request, test_id):
        user_name = request.user.username
        answers = dict(list(request.POST.items()))
        print(answers)
        for key, value in answers.items():
            type = key.split('_')[0]
            ques_id = key.split('_')[1]
            ques = Question.objects.get(id=ques_id)
            UserAnswer(ques=ques, u_name=user_name, type=type, answer=value).save()
        return HttpResponseRedirect(f'/test/user/answer/show/{test_id}')


class UserAnswerShow(View):
    context = {}

    def get(self, request, test_id):
        user_name = request.user.username
        user = User.objects.get(username=user_name)
        self.context['user_name'] = user_name
        if user.is_superuser==1:
            cur_test = Test.objects.get(id=test_id)
            self.context['test_name'] = cur_test.title
            self.context['test_id'] = test_id
            ques = Question.objects.filter(test_id=test_id)
            self.context['ans_lst'] = []
            for q in ques:
                u_ans = UserAnswer.objects.get(ques=q, u_name=user_name)
                self.context['ans_lst'].append({'a': u_ans, 'q': q})
            return render(request, 'main/show_answers.html', self.context)
        else:
            cur_test = Test.objects.get(id=test_id)
            self.context['test_name'] = cur_test.title
            self.context['test_id'] = test_id
            ques = Question.objects.filter(test_id=test_id)
            self.context['ans_lst'] = []
            for q in ques:
                u_ans = UserAnswer.objects.get(ques=q, u_name=user_name)
                self.context['ans_lst'].append({'a': u_ans, 'q': q})
            return render(request, 'main/show_answers.html', self.context)

class UserController(View):
    def get(self, request, test_id):
        user_name = request.user.username
        user = User.objects.get(username=user_name)
        if user.is_superuser!=1:
            t=Test.objects.get(id=test_id)
            ques = Question.objects.filter(test_id=test_id)
            lis=[]
            for q in ques:
                try:
                    u_ans = UserAnswer.objects.get(ques=q, u_name=user_name)
                    lis.append(u_ans)
                except:
                    continue
            print(lis)
            if lis==[]:
                return HttpResponseRedirect(f'/test/user/answer/{test_id}')
            else:
                return HttpResponseRedirect(f'/test/user/answer/show/{test_id}')


def index(request):
    return render(request, 'main/index.html')
