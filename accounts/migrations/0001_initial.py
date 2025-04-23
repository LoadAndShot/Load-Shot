migrations.CreateModel(
    name='CustomUser',
    fields=[
        ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
        ('username', models.CharField(max_length=150, unique=True)),
        ('can_access_catalogue1', models.BooleanField(default=True)),
        ('can_access_catalogue2', models.BooleanField(default=True)),
        # ... les autres champs ...
    ],
)
