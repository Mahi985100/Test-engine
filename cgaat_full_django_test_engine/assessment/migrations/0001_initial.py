# Generated manually for working sample project
from django.db import migrations, models
import django.db.models.deletion
from django.conf import settings


def seed_data(apps, schema_editor):
    Section = apps.get_model('assessment','Section')
    Question = apps.get_model('assessment','Question')
    data = [
        ('Aptitude Section','Checks logical reasoning, number series and pattern recognition skills.',1,[
            ('Find the next number: 2, 4, 8, 16, ?', ['18','24','32','64'], [1,2,4,3], 'Number Series'),
            ('Which one is different: Apple, Banana, Carrot, Mango?', ['Apple','Banana','Carrot','Mango'], [2,2,4,2], 'Logical Reasoning'),
            ('If all roses are flowers and some flowers fade, what is true?', ['All roses fade','Some flowers are roses','No roses are flowers','All flowers are roses'], [1,4,1,1], 'Logical Reasoning'),
            ('Complete pattern: AB, CD, EF, ?', ['GH','FG','HI','IJ'], [4,1,2,1], 'Pattern Recognition'),
        ]),
        ('Personality Section','Understands leadership style, teamwork preference and confidence level.',2,[
            ('Do you enjoy leading a team?', ['Never','Sometimes','Often','Always'], [1,2,3,4], 'Leadership'),
            ('Do you prefer working alone or in groups?', ['Always alone','Mostly alone','Both are fine','Group work'], [1,2,3,4], 'Team Work'),
            ('How do you handle responsibility?', ['Avoid it','Need support','Manage well','Take ownership'], [1,2,3,4], 'Decision Making'),
            ('When a problem comes, you usually:', ['Panic','Wait for others','Think and try','Lead solution'], [1,2,3,4], 'Leadership'),
        ]),
        ('Career Interest Section','Finds interest areas like designing, coding, teaching, business and sales.',3,[
            ('Which activity do you enjoy most?', ['Selling','Teaching','Designing','Coding'], [2,3,4,4], 'Career Interest'),
            ('Which work environment do you like?', ['Fixed routine','Creative studio','Tech lab','Business office'], [2,4,4,3], 'Career Interest'),
            ('Which project would you choose?', ['Poster design','Website app','Class seminar','Business plan'], [4,4,3,3], 'Career Interest'),
            ('What motivates you more?', ['Money only','Learning','Helping people','Solving problems'], [2,3,3,4], 'Career Interest'),
        ]),
        ('Emotional Intelligence Section','Measures emotional control, empathy, communication and pressure handling.',4,[
            ('How do you react under pressure?', ['Angry','Confused','Stay calm','Plan and act'], [1,2,3,4], 'Emotional Control'),
            ('How do you handle criticism?', ['Ignore','Feel bad','Listen','Improve from it'], [1,2,3,4], 'Communication'),
            ('A friend is upset. What will you do?', ['Avoid','Give advice quickly','Listen carefully','Support and guide'], [1,2,3,4], 'Empathy'),
            ('In conflict, you prefer to:', ['Fight','Stay silent','Discuss','Find fair solution'], [1,2,3,4], 'Communication'),
        ]),
    ]
    for name, meaning, order, qs in data:
        sec, _ = Section.objects.get_or_create(name=name, defaults={'meaning':meaning,'order':order})
        for i,(text, opts, scores, tag) in enumerate(qs, start=1):
            Question.objects.get_or_create(section=sec, text=text, defaults={'option_a':opts[0],'option_b':opts[1],'option_c':opts[2],'option_d':opts[3],'score_a':scores[0],'score_b':scores[1],'score_c':scores[2],'score_d':scores[3],'order':i,'skill_tag':tag})

class Migration(migrations.Migration):
    initial = True
    dependencies = [migrations.swappable_dependency(settings.AUTH_USER_MODEL)]
    operations = [
        migrations.CreateModel(name='Section', fields=[('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),('name', models.CharField(max_length=120)),('meaning', models.TextField()),('order', models.PositiveIntegerField(default=1))]),
        migrations.CreateModel(name='Question', fields=[('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),('text', models.TextField()),('option_a', models.CharField(max_length=255)),('score_a', models.IntegerField(default=1)),('option_b', models.CharField(max_length=255)),('score_b', models.IntegerField(default=2)),('option_c', models.CharField(max_length=255)),('score_c', models.IntegerField(default=3)),('option_d', models.CharField(max_length=255)),('score_d', models.IntegerField(default=4)),('order', models.PositiveIntegerField(default=1)),('skill_tag', models.CharField(default='General', max_length=80)),('section', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='questions', to='assessment.section'))]),
        migrations.CreateModel(name='TestAttempt', fields=[('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),('started_at', models.DateTimeField(auto_now_add=True)),('submitted_at', models.DateTimeField(blank=True, null=True)),('total_score', models.IntegerField(default=0)),('analytical_score', models.IntegerField(default=0)),('leadership_score', models.IntegerField(default=0)),('communication_score', models.IntegerField(default=0)),('personality_type', models.CharField(blank=True, max_length=100)),('career_matches', models.CharField(blank=True, max_length=255)),('strengths', models.TextField(blank=True)),('weaknesses', models.TextField(blank=True)),('completed', models.BooleanField(default=False)),('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL))]),
        migrations.CreateModel(name='Answer', fields=[('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),('selected_option', models.CharField(max_length=1)),('score', models.IntegerField(default=0)),('attempt', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='answers', to='assessment.testattempt')),('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='assessment.question'))], options={'unique_together': {('attempt', 'question')}}),
        migrations.RunPython(seed_data),
    ]
