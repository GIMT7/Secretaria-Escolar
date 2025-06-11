from django.db import models
from django.http import HttpResponse
from reportlab.pdfgen import canvas
from .validators import cep_validator, cpf_validator, phone_validator, validate_nota
from django.core.validators import FileExtensionValidator

# Modelo para representar as turmas da escola
class Class(models.Model):
    CLASS_CHOICES = (
        ("1A", "1° Ano A"),
        ("1B", "1° Ano B"),
        ("1C", "1° Ano C"),
        ("2A", "2° Ano A"),
        ("2B", "2° Ano B"),
        ("2C", "2° Ano C"),
        ("3A", "3° Ano A"),
        ("3B", "3° Ano B"),
        ("3C", "3° Ano C"),
    )

    ITINERARY_CHOICES = (
        ("DS", "Desenvolvimento de Sistemas"),
        ("CN", "Ciencias da Natureza"),
        ("JG", "Desenvolvimento de Jogos"),
    )
    # Campo para a turma #test
    class_choices = models.CharField(max_length=50, choices=CLASS_CHOICES, blank=False, null=True,)
    # Campo para o itinerário
    itinerary_choices = models.CharField(max_length=50, choices=ITINERARY_CHOICES, blank=False, null=True,)
  
    def __str__(self):
        # Exibe a turma e o itinerário de forma legível
        return f"{self.get_class_choices_display()} - {self.get_itinerary_choices_display()}"

# Modelo para representar as matérias
class Matter(models.Model):
    MATTER_CHOICES = (
        ("CH", "Ciencias Humanas"),
        ("L", "Linguagens"),
        ("M", "Matematica"),
        ("CN", "Ciencias da Natureza"),
    )
    # Campo para a matéria
    matter_choices = models.CharField(max_length=50, choices=MATTER_CHOICES, blank=False, null=True,)

    def __str__(self):
        # Exibe o nome da matéria de forma legível
        return f"{self.get_matter_choices_display()}"

# Modelo para representar os alunos
class Student(models.Model):
    full_name = models.CharField(
        max_length=200, verbose_name="Student's full name", null=True
    )

    registration_number = models.CharField(
        max_length=6, unique=True, verbose_name="Student's registration"
    )
    phone_number = models.CharField(
        max_length=15,
        verbose_name="Student's phone number (XX) 9XXXX-XXXX",
        validators=[phone_validator],
    )
    email = models.EmailField(max_length=100, verbose_name="Student's email")
    cpf = models.CharField(
        max_length=11,
        verbose_name="Student's CPF",
        unique=True,
        validators=[cpf_validator],
    )
    birthday = models.DateField(max_length=10)
    adress = models.CharField(max_length=100, validators=[cep_validator])
    class_choice = models.ForeignKey(
        Class,
        on_delete=models.CASCADE,
        verbose_name="Student's class",
        related_name="student_class",
        blank=False,
        null=True,
    )


    def __str__(self):
        return self.full_name


# Modelo para representar os responsáveis
class Guardian(models.Model):
    full_name = models.CharField(
        max_length=200, verbose_name="Guardian's full name", null=True
    )
    student = models.ForeignKey(
        Student,
        on_delete=models.CASCADE,
        verbose_name="Guardian's student",
        related_name="guardian_student",
        blank=False,
        null=True,
    )
    phone_number = models.CharField(
        max_length=15,
        verbose_name="Guardian's phone number (XX) 9XXXX-XXXX",
        validators=[phone_validator],
    )
    email = models.EmailField(max_length=100, verbose_name="Guardian's email")
    cpf = models.CharField(
        max_length=11,
        verbose_name="Guardian's CPF",
        unique=True,
        validators=[cpf_validator],
    )
    birthday = models.DateField(max_length=10)
    adress = models.CharField(max_length=100, validators=[cep_validator])

    def __str__(self):
        return self.full_name


# Modelo para representar os professores
class Professor(models.Model):
    full_name = models.CharField(
        max_length=200, verbose_name="Professor's full name", null=True
    )
    phone_number = models.CharField(
        max_length=15,
        verbose_name="Professor's phone number (XX) 9XXXX-XXXX",
        validators=[phone_validator],
    )
    email = models.EmailField(max_length=100, verbose_name="Professor's email")
    cpf = models.CharField(
        max_length=11,
        verbose_name="Professor's CPF",
        unique=True,
        validators=[cpf_validator],
    )
    birthday = models.DateField(max_length=10)
    adress = models.CharField(max_length=100, validators=[cep_validator])
    class_choice = models.ForeignKey(
        Class,
        on_delete=models.CASCADE,
        verbose_name="Student's class",
        related_name="professor_class",
        blank=False,
        null=True,
    )
    matter_choice = models.ForeignKey(
        Matter,
        on_delete=models.CASCADE,
        verbose_name="Student's matter",
        related_name="professor_matter",
        blank=False,
        null=True,
    )

    def __str__(self):
        return self.full_name


# Modelo para representar os contratos
class Contract(models.Model):
    guardian = models.ForeignKey(
        Guardian,
        on_delete=models.CASCADE,
        verbose_name="Guardian's name",
        related_name="contract_guardian",
        blank=False,
        null=True,
    )

    student = models.ForeignKey(
        Student,
        on_delete=models.CASCADE,
        verbose_name="Student's name",
        related_name="contract_student",
        blank=False,
        null=True,
    )

    uploaded_pdf = models.FileField(
        upload_to="contracts/",
        null=True,
        blank=True,
        validators=[FileExtensionValidator(allowed_extensions=["pdf"])]
    )

    def generate_contract_pdf(self):
        response = HttpResponse(content_type="application/pdf")
        response["Content-Disposition"] = (
            f'attachment; filename="contract_{self.id}_{self.guardian.full_name}-{self.student.full_name}.pdf"'
        )

        p = canvas.Canvas(response)
        p.drawString(100, 800, f"Contract ID: {self.id}")
        p.drawString(100, 780, f"Guardian Name: {self.guardian.full_name}")
        p.drawString(100, 760, f"Guardian Phone: {self.guardian.phone_number}")
        p.drawString(100, 740, f"Guardian Email: {self.guardian.email}")
        p.drawString(100, 720, f"Guardian CPF: {self.guardian.cpf}")
        p.drawString(100, 700, f"Guardian Birthday: {self.guardian.birthday}")
        p.drawString(100, 680, f"Guardian Address: {self.guardian.adress}")
        p.drawString(100, 640, f"Student Name: {self.student.full_name}")
        p.drawString(100, 620, f"Student Phone: {self.student.phone_number}")
        p.drawString(100, 600, f"Student Email: {self.student.email}")
        p.drawString(100, 580, f"Student CPF: {self.student.cpf}")
        p.drawString(100, 560, f"Student Birthday: {self.student.birthday}")
        p.drawString(100, 540, f"Student Address: {self.student.adress}")
        p.drawString(
            100, 500, f"Assinatura: _______________________________________________X"
        )
        p.showPage()
        p.save()

        return response

    def __str__(self):
        return f"Contract for {self.student.full_name} and {self.guardian.full_name}"


# Modelo para representar as notas
class Grade(models.Model):
    student = models.ForeignKey(
        Student,
        on_delete=models.CASCADE,
        verbose_name="student",
        related_name="grade_student",
        blank=False,
        null=True,
    )

    classs = models.ForeignKey(
        Class,
        on_delete=models.CASCADE,
        verbose_name="class",
        related_name="grade_class",
        blank=False,
        null=True,
    )
    matter = models.ForeignKey(
        Matter,
        on_delete=models.CASCADE,
        verbose_name="matter",
        related_name="grade_matter",
        blank=False,
        null=True,
    )
    grade_presence = models.FloatField(
         verbose_name="Grade of Presence",
         default=0,
         validators=[validate_nota],
    )
    grade_activity = models.FloatField(
         verbose_name="Grade of Activity",
         default=0,
         validators=[validate_nota],
    )
    grade_evaluative = models.FloatField(
         verbose_name="Grade of Evaluative",
         default=0,
         validators=[validate_nota],
    )
    grade_final = models.FloatField(
         verbose_name="Final Grade",
         default=0,
         validators=[validate_nota],
         editable=False
    )
    class Meta:
        unique_together = (
            "student",
            "classs",
            "matter",
        )
    
    def save(self, *args, **kwargs):
        self.grade_final = (
            self.grade_presence + self.grade_activity + self.grade_evaluative
        ) / 3
        super().save(*args, **kwargs)

        # Emit performance alert after saving
        performance_alert = self.check_performance()
        if performance_alert:
            print(performance_alert)

    def check_performance(self):
        if self.grade_final < 6:
            return f"Alert: {self.student.full_name} has a low performance with a final grade of {self.grade_final}."
        return None

    def __str__(self):
        return f"Grades for {self.student.full_name} in {self.classs} - {self.matter}"


# Modelo para representar as faltas
class Absence(models.Model):
    student = models.ForeignKey(
        Student,
        on_delete=models.CASCADE,
        verbose_name="Student",
        related_name="absence_student",
        blank=False,
        null=True,
    )
    classs = models.ForeignKey(
        Class,
        on_delete=models.CASCADE,
        verbose_name="Class",
        related_name="absence_class",
        blank=False,
        null=True,
    )
    matter = models.ForeignKey(
        Matter,
        on_delete=models.CASCADE,
        verbose_name="Matter",
        related_name="absence_matter",
        blank=False,
        null=True,
    )
    date = models.DateField(verbose_name="Date of Absence")
    justification = models.TextField(
        verbose_name="Justification",
        blank=True,
        null=True,
    )

    class Meta:
        unique_together = (
            "student",
            "classs",
            "matter",
            "date",
        )

    def __str__(self):
        return f"Absence of {self.student.full_name} in {self.classs} - {self.matter} on {self.date}"


# Modelo para representar o histórico acadêmico
class AcademicHistory(models.Model):
    student = models.ForeignKey(
        Student,
        on_delete=models.CASCADE,
        verbose_name="Student",
        related_name="academic_history",
    )
    classs = models.ForeignKey(
        Class,
        on_delete=models.CASCADE,
        verbose_name="Class",
        related_name="academic_history_class",
    )
    matter = models.ForeignKey(
        Matter,
        on_delete=models.CASCADE,
        verbose_name="Matter",
        related_name="academic_history_matter",
    )
    grade_final = models.FloatField(
        verbose_name="Final Grade",
        default=0.0,
    )
    total_absences = models.PositiveIntegerField(
        verbose_name="Total Absences",
        default=0,
    )

    def update_history(self):
        grades = Grade.objects.filter(student=self.student, classs=self.classs, matter=self.matter).first()
        absences = Absence.objects.filter(student=self.student, classs=self.classs, matter=self.matter)

        self.grade_final = grades.grade_final if grades else 0.0
        self.total_absences = absences.count()
        self.save()

    def generate_history_pdf(self):
        response = HttpResponse(content_type="application/pdf")
        response["Content-Disposition"] = (
            f'attachment; filename="academic_history_{self.student.full_name}_{self.classs}_{self.matter}.pdf"'
        )
        p = canvas.Canvas(response)
        p.setFont("Helvetica-Bold", 16)
        p.drawString(100, 800, "Histórico Acadêmico")
        p.setFont("Helvetica", 12)
        p.drawString(100, 780, f"Aluno: {self.student.full_name}")
        p.drawString(100, 760, f"Classe: {self.classs}")
        p.drawString(100, 740, f"Matéria: {self.matter}")
        p.drawString(100, 720, f"Nota Final: {self.grade_final}")
        p.drawString(100, 700, f"Total de Faltas: {self.total_absences}")
        # Tabela de desempenho
        p.setFont("Helvetica-Bold", 14)
        p.drawString(100, 670, "Desempenho por Avaliação:")
        p.setFont("Helvetica", 12)
        p.drawString(100, 650, "Tipo")
        p.drawString(250, 650, "Nota")
        p.line(100, 645, 350, 645)
        from .models import Grade
        grade = Grade.objects.filter(student=self.student, classs=self.classs, matter=self.matter).order_by('-id').first()
        if grade:
            p.drawString(100, 630, "Presença")
            p.drawString(250, 630, f"{grade.grade_presence:.2f}")
            p.drawString(100, 610, "Atividade")
            p.drawString(250, 610, f"{grade.grade_activity:.2f}")
            p.drawString(100, 590, "Avaliação")
            p.drawString(250, 590, f"{grade.grade_evaluative:.2f}")
            p.drawString(100, 570, "Média Final")
            p.drawString(250, 570, f"{grade.grade_final:.2f}")
            # Gráfico de barras
            y_base = 500  # Move o gráfico mais para baixo
            p.setFont("Helvetica-Bold", 12)
            p.drawString(100, y_base + 80, "Gráfico de Desempenho")
            bar_labels = ["Presença", "Atividade", "Avaliação", "Média"]
            bar_values = [grade.grade_presence, grade.grade_activity, grade.grade_evaluative, grade.grade_final]
            max_value = max(bar_values + [10])
            bar_width = 30
            for i, (label, value) in enumerate(zip(bar_labels, bar_values)):
                x = 100 + i * 60
                bar_height = int((value / max_value) * 100)
                p.setFillColorRGB(0.2, 0.4, 0.8)
                p.rect(x, y_base, bar_width, bar_height, fill=1)
                p.setFillColorRGB(0, 0, 0)
                p.drawString(x, y_base - 15, label)
                p.drawString(x, y_base + bar_height + 5, f"{value:.1f}")
        p.showPage()
        p.save()
        return response

    def __str__(self):
        return f"Academic History for {self.student.full_name} in {self.classs} - {self.matter}"


# Modelo para representar os boletins
class ReportCard(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name="report_cards")
    classs = models.ForeignKey(Class, on_delete=models.CASCADE, related_name="report_cards", null=True, blank=True)  # Permitir valores nulos
    matter = models.ForeignKey(Matter, on_delete=models.CASCADE, related_name="report_cards")
    grade_final = models.FloatField(verbose_name="Final Grade", default=0.0)
    comments = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"ReportCard for {self.student.full_name} in {self.classs} - {self.matter}"

# Modelo para representar os eventos escolares
class SchoolEvent(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    date = models.DateField()
    file = models.FileField(upload_to="event_files/", blank=True, null=True)
    created_by = models.ForeignKey('auth.User', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.title} ({self.date})"

# Modelo para representar a grade de horários
class ClassSchedule(models.Model):
    professor = models.ForeignKey('Professor', on_delete=models.CASCADE)
    classs = models.ForeignKey('Class', on_delete=models.CASCADE)
    matter = models.ForeignKey('Matter', on_delete=models.CASCADE)
    weekday = models.CharField(max_length=10, choices=[
        ("SEG", "Segunda-feira"),
        ("TER", "Terça-feira"),
        ("QUA", "Quarta-feira"),
        ("QUI", "Quinta-feira"),
        ("SEX", "Sexta-feira"),
    ])
    start_time = models.TimeField()
    end_time = models.TimeField()

    def __str__(self):
        return f"{self.classs} - {self.matter} ({self.weekday} {self.start_time}-{self.end_time})"
