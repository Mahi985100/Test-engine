from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.utils import timezone
from django.contrib import messages
from django.contrib.auth.models import User
from .models import Section, Question, TestAttempt, Answer
from .forms import QuestionForm


def home(request):
    return render(request, 'assessment/home.html', {'sections': Section.objects.all().order_by('order')})


def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard')
    else:
        form = UserCreationForm()
    return render(request, 'assessment/register.html', {'form': form})

@login_required
def dashboard(request):
    attempts = TestAttempt.objects.filter(user=request.user).order_by('-started_at')
    context = {'attempts': attempts}
    
    if request.user.is_staff:
        context['total_users'] = User.objects.count()
        context['total_questions'] = Question.objects.count()
        context['total_attempts'] = TestAttempt.objects.count()
        context['completed_tests'] = TestAttempt.objects.filter(completed=True).count()
        
        from django.db.models import Avg
        avg_score = TestAttempt.objects.filter(completed=True).aggregate(Avg('total_score'))['total_score__avg'] or 0
        context['avg_score'] = round(avg_score, 2)
        
    return render(request, 'assessment/dashboard.html', context)

@login_required
def smart_dashboard(request):
    questions = Question.objects.all()
    total_questions = questions.count()
    sections_count = Section.objects.count()
    total_time = sections_count * 10
    
    # Get distinct skills from all questions
    skills = list(Question.objects.values_list('skill_tag', flat=True).distinct())
    # Remove empty or duplicate skills ignoring case (if needed, but simple distinct should be fine)
    skills = [s for s in skills if s.strip()]
    
    context = {
        'total_questions': total_questions,
        'total_time': total_time,
        'difficulty_level': 'Moderate', # Static as per model state
        'skills': skills,
    }
    return render(request, 'assessment/smart_dashboard.html', context)

@login_required
def start_test(request):
    if Question.objects.count() == 0:
        messages.error(request, 'Sample questions are not available. Run migrations correctly.')
        return redirect('home')
    attempt = TestAttempt.objects.create(user=request.user)
    return redirect('test_question', attempt_id=attempt.id, index=0)

@login_required
def test_question(request, attempt_id, index):
    attempt = get_object_or_404(TestAttempt, id=attempt_id, user=request.user)
    questions = list(Question.objects.select_related('section').order_by('section__order','order'))
    total = len(questions)
    if total == 0:
        return redirect('home')
    if index < 0: index = 0
    if index >= total: return redirect('submit_test', attempt_id=attempt.id)
    q = questions[index]
    
    # Mark as visited
    existing, created = Answer.objects.get_or_create(attempt=attempt, question=q)
    if created or not existing.is_visited:
        existing.is_visited = True
        existing.save()

    if request.method == 'POST':
        selected = request.POST.get('answer')
        is_marked = request.POST.get('is_marked') == 'true'
        scores = {'A': q.score_a, 'B': q.score_b, 'C': q.score_c, 'D': q.score_d}
        
        if selected in scores:
            existing.selected_option = selected
            existing.score = scores[selected]
        
        existing.is_marked = is_marked
        existing.save()
        
        if 'previous' in request.POST:
            return redirect('test_question', attempt_id=attempt.id, index=index-1)
        if 'submit' in request.POST:
            return redirect('submit_test', attempt_id=attempt.id)
        return redirect('test_question', attempt_id=attempt.id, index=index+1)
        
    all_answers = Answer.objects.filter(attempt=attempt)
    answered_count = all_answers.exclude(selected_option__isnull=True).exclude(selected_option='').count()
    questions_left = total - answered_count
    percent_completed = int((answered_count / total) * 100) if total > 0 else 0
    
    q_nav = []
    answers_dict = {a.question_id: a for a in all_answers}
    for i, q_obj in enumerate(questions):
        ans = answers_dict.get(q_obj.id)
        status = 'not_visited'
        if ans:
            if ans.is_marked:
                status = 'marked'
            elif ans.selected_option:
                status = 'answered'
            elif ans.is_visited:
                status = 'not_answered'
                
        q_nav.append({
            'index': i,
            'label': i + 1,
            'status': status,
            'is_current': i == index
        })

    return render(request, 'assessment/test.html', {
        'attempt': attempt,
        'question': q,
        'index': index,
        'total': total,
        'progress': percent_completed, 
        'existing': existing,
        'answered': answered_count,
        'questions_left': questions_left,
        'percent_completed': percent_completed,
        'q_nav': q_nav,
    })

@login_required
def submit_test(request, attempt_id):
    attempt = get_object_or_404(TestAttempt, id=attempt_id, user=request.user)
    answers = Answer.objects.filter(attempt=attempt).select_related('question','question__section')
    total = sum(a.score for a in answers)
    analytical = sum(a.score for a in answers if a.question.skill_tag in ['Logical Reasoning','Number Series','Pattern Recognition'])
    leadership = sum(a.score for a in answers if a.question.skill_tag in ['Leadership','Decision Making','Team Work'])
    communication = sum(a.score for a in answers if a.question.skill_tag in ['Communication','Emotional Control','Empathy'])
    if total >= 56:
        ptype = 'Confident Leader'
        career = 'Business Analyst, Project Manager, Entrepreneur, HR Manager'
        strengths = 'Leadership, decision making, confidence, communication, career clarity.'
        weaknesses = 'Avoid overconfidence and improve patience while working in a team.'
    elif total >= 42:
        ptype = 'Balanced Explorer'
        career = 'Data Analyst, Software Developer, Designer, Digital Marketer'
        strengths = 'Good learning ability, flexible mindset, practical thinking.'
        weaknesses = 'Need more focus on long-term career planning and presentation skills.'
    else:
        ptype = 'Supportive Learner'
        career = 'Teaching Assistant, Support Executive, Junior Developer, Operations Assistant'
        strengths = 'Calm nature, learning attitude, cooperative behavior.'
        weaknesses = 'Need to improve confidence, aptitude practice and communication.'
    attempt.total_score = total
    attempt.analytical_score = analytical
    attempt.leadership_score = leadership
    attempt.communication_score = communication
    attempt.personality_type = ptype
    attempt.career_matches = career
    attempt.strengths = strengths
    attempt.weaknesses = weaknesses
    attempt.completed = True
    attempt.submitted_at = timezone.now()
    attempt.save()
    return redirect('report', attempt_id=attempt.id)

@login_required
def report(request, attempt_id):
    if request.user.is_staff:
        attempt = get_object_or_404(TestAttempt, id=attempt_id)
    else:
        attempt = get_object_or_404(TestAttempt, id=attempt_id, user=request.user)
    answers = attempt.answers.select_related('question','question__section').all()
    section_scores = []
    for section in Section.objects.order_by('order'):
        s_answers = answers.filter(question__section=section)
        section_scores.append({'section': section, 'score': sum(a.score for a in s_answers), 'count': s_answers.count()})
    return render(request, 'assessment/report.html', {
        'attempt': attempt,
        'section_scores': section_scores,
        'answers': answers
    })

@staff_member_required(login_url='login')
def question_list(request):
    questions = Question.objects.select_related('section').order_by('section__order', 'order')
    return render(request, 'assessment/question_list.html', {'questions': questions})

@staff_member_required(login_url='login')
def question_create(request):
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Question added successfully.')
            return redirect('question_list')
    else:
        form = QuestionForm()
    return render(request, 'assessment/question_form.html', {'form': form, 'title': 'Add Question'})

@staff_member_required(login_url='login')
def question_update(request, pk):
    question = get_object_or_404(Question, pk=pk)
    if request.method == 'POST':
        form = QuestionForm(request.POST, instance=question)
        if form.is_valid():
            form.save()
            messages.success(request, 'Question updated successfully.')
            return redirect('question_list')
    else:
        form = QuestionForm(instance=question)
    return render(request, 'assessment/question_form.html', {'form': form, 'title': 'Edit Question'})

@staff_member_required(login_url='login')
def question_delete(request, pk):
    question = get_object_or_404(Question, pk=pk)
    if request.method == 'POST':
        question.delete()
        messages.success(request, 'Question deleted successfully.')
        return redirect('question_list')
    return render(request, 'assessment/question_confirm_delete.html', {'question': question})

@staff_member_required(login_url='login')
def test_attempt_list(request):
    attempts = TestAttempt.objects.select_related('user').order_by('-started_at')
    
    # Stats
    total_users = User.objects.count()
    total_questions = Question.objects.count()
    total_attempts = attempts.count()
    completed_tests = attempts.filter(completed=True).count()
    
    from django.db.models import Avg
    avg_score = attempts.filter(completed=True).aggregate(Avg('total_score'))['total_score__avg'] or 0
    
    context = {
        'attempts': attempts,
        'total_users': total_users,
        'total_questions': total_questions,
        'total_attempts': total_attempts,
        'completed_tests': completed_tests,
        'avg_score': round(avg_score, 2)
    }
    return render(request, 'assessment/test_attempt_list.html', context)
