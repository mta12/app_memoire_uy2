# Generated by Django 3.0.6 on 2020-06-07 17:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Personne',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom_complet', models.CharField(max_length=60)),
            ],
        ),
        migrations.CreateModel(
            name='Etudiant',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('matricule', models.CharField(max_length=10)),
                ('etudiant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.Personne')),
            ],
        ),
        migrations.CreateModel(
            name='Enseignant',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titre_enseignant', models.CharField(choices=[('ASS', 'Assistant'), ('CC', 'Chargé de cours'), ('MC', 'Maitre de Conférence'), ('PR', 'Professeur')], max_length=3)),
                ('role_enseignant', models.CharField(choices=[('JUR', 'Membre du Jury'), ('ENC', 'Encadreur'), ('SUP', 'Superviseur')], max_length=3)),
                ('enseignant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.Personne')),
            ],
        ),
        migrations.CreateModel(
            name='Document',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type_doc', models.CharField(choices=[('MAS', 'Mémoire de Master'), ('DOC', 'Thèse de Doctorat')], max_length=3, null=True)),
                ('titre_doc', models.CharField(max_length=50)),
                ('resume_doc', models.TextField(null=True)),
                ('date_selection', models.DateTimeField(null=True, verbose_name='Date de Selection')),
                ('est_soutenu', models.BooleanField(default=False)),
                ('date_soutenance', models.DateTimeField(null=True, verbose_name='Date de Soutenance')),
                ('note_soutenance', models.DecimalField(decimal_places=2, max_digits=3)),
                ('etablissement', models.CharField(choices=[('FSJP', 'Faculté des Sciences Juridiques et Politiques'), ('FSEG', 'Faculté des Sciences Economiques et de Gestion')], max_length=6, null=True)),
                ('type_formation', models.CharField(choices=[('ACC', 'Formation Académique'), ('PRO', 'Formation professionnelle')], max_length=3, null=True)),
                ('filiere', models.CharField(max_length=20, null=True)),
                ('fichier', models.FileField(null=True, upload_to='uploads/docs')),
                ('auteur', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.Etudiant')),
                ('encadreur', models.ManyToManyField(related_name='encadreur', to='main.Enseignant')),
                ('jury', models.ManyToManyField(related_name='jury', to='main.Enseignant')),
            ],
        ),
    ]
