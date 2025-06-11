from django.contrib import admin
from school.models import Guardian, Student, Professor, Contract, Class, Matter, Grade, Absence, AcademicHistory, ReportCard, SchoolEvent, ClassSchedule
from django.http import HttpResponseRedirect
from django.utils.html import format_html
from django.urls import path

# Admin para estudantes
class StudentsAdmin(admin.ModelAdmin):
    # Define os campos exibidos na lista
    list_display = (
        "id",
        "full_name",
        "registration_number",
        "phone_number",
        "email",
        "adress",
        "cpf",
        "birthday",
        "class_choice",      
    )
    # Define os campos que são links
    list_display_links = (
        "full_name",
        "email",
        "adress",
    )
    # Campos de busca
    search_fields = (
        "full_name",
        "registration_number",
    )
    # Filtros laterais
    list_filter = ("full_name",)

# Admin para responsáveis
class GuardiansAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "full_name",
        "student",
        "phone_number",
        "email",
        "cpf",
        "birthday",
        "adress",
    )
    list_display_links = (
        "full_name",
        "email",
        "adress",
    )
    search_fields = ("full_name",)
    list_filter = ("full_name",)

# Admin para professores
class ProfessorsAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "full_name",
        "phone_number",
        "email",
        "cpf",
        "birthday",
        "adress",
        "class_choice",
        "matter_choice",
    )
    list_display_links = (
        "full_name",
        "email",
        "adress",
    )
    search_fields = ("full_name",)
    list_filter = ("full_name",)

# Admin para contratos
class ContractsAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "guardian",
        "student",
        "download_contract",
    )
    list_display_links = (
        "guardian",
        "student",
    )
    search_fields = (
        "guardian",
        "student",
    )

    # Link para download do contrato em PDF
    def download_contract(self, obj):
        return format_html(
            '<a href="{}">Download Contract</a>',
            f"/admin/school/contract/{obj.id}/generate-pdf/",
        )

    download_contract.short_description = "Download Contract"

    # Adiciona URL customizada para gerar PDF
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path(
                "<int:contract_id>/generate-pdf/",
                self.admin_site.admin_view(self.generate_pdf),
                name="contract-generate-pdf",
            ),
        ]
        return custom_urls + urls

    # Gera o PDF do contrato
    def generate_pdf(self, request, contract_id):
        try:
            contract = Contract.objects.get(pk=contract_id)
            return contract.generate_contract_pdf()
        except Contract.DoesNotExist:
            self.message_user(request, "Contract not found.")
            return HttpResponseRedirect(request.META.get("HTTP_REFERER"))

# Admin para turmas
class ClassesAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "class_choices",
        "itinerary_choices",
    )
    list_display_links = (
        "class_choices",
        "itinerary_choices",
    )
    search_fields = (
        "class_choices",
        "itinerary_choices",
    )
    list_filter = ("itinerary_choices",)

# Admin para matérias
class MattersAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "matter_choices",
    )
    list_display_links = (
        "matter_choices",
    )
    search_fields = (
        "matter_choices",
    )
    list_filter = ("matter_choices",)

# Admin para notas
class GradesAdmin(admin.ModelAdmin):
    list_display = (
        "student",
        "classs",
        "matter",
        "grade_presence",
        "grade_activity",
        "grade_evaluative",
        "display_final_grade",
    )
    search_fields = (
        "student__full_name",
        "classs__class_choices",
        "matter__matter_choices",
    )
    list_filter = ("classs", "matter",)

    # Exibe a nota final com destaque se for baixa
    def display_final_grade(self, obj):
        if obj.grade_final < 5:
            return format_html(
                '<span style="color: red;">{} (Low Performance)</span>',
                obj.grade_final
            )
        return obj.grade_final

    display_final_grade.short_description = "Final Grade"

# Admin para faltas
class AbsencesAdmin(admin.ModelAdmin):
    list_display = (
        "student",
        "classs",
        "matter",
        "date",
        "justification",
    )
    search_fields = (
        "student__full_name",
        "classs__class_choices",
        "matter__matter_choices",
    )
    list_filter = ("classs", "matter", "date")

# Admin para histórico acadêmico
class AcademicHistoryAdmin(admin.ModelAdmin):
    list_display = (
        "student",
        "classs",
        "matter",
        "grade_final",
        "total_absences",
        "download_history_pdf",
    )
    search_fields = (
        "student__full_name",
        "classs__class_choices",
        "matter__matter_choices",
    )
    list_filter = ("classs", "matter",)

    # Link para download do histórico em PDF
    def download_history_pdf(self, obj):
        return format_html(
            '<a href="{}">Download PDF</a>',
            f"/admin/school/academichistory/{obj.id}/generate-pdf/"
        )
    download_history_pdf.short_description = "PDF"

    # Adiciona URL customizada para gerar PDF do histórico
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path(
                '<int:history_id>/generate-pdf/',
                self.admin_site.admin_view(self.generate_pdf),
                name="academichistory-generate-pdf",
            ),
        ]
        return custom_urls + urls

    # Gera o PDF do histórico
    def generate_pdf(self, request, history_id):
        try:
            history = AcademicHistory.objects.get(pk=history_id)
            return history.generate_history_pdf()
        except AcademicHistory.DoesNotExist:
            self.message_user(request, "Academic History not found.")
            return HttpResponseRedirect(request.META.get("HTTP_REFERER"))

# Admin para eventos escolares
class SchoolEventAdmin(admin.ModelAdmin):
    list_display = ("title", "date", "created_by", "file")
    search_fields = ("title", "description", "created_by__username")
    list_filter = ("date",)

# Admin para grade de horários
class ClassScheduleAdmin(admin.ModelAdmin):
    list_display = ("professor", "classs", "matter", "weekday", "start_time", "end_time")
    search_fields = ("professor__full_name", "classs__class_choices", "matter__matter_choices")
    list_filter = ("professor", "classs", "matter", "weekday")

# Registro dos modelos no admin
admin.site.register(
    Guardian,
    GuardiansAdmin,
)

admin.site.register(
    Student,
    StudentsAdmin,
)

admin.site.register(
    Professor,
    ProfessorsAdmin,
)

admin.site.register(
    Contract,
    ContractsAdmin,
)

admin.site.register(
    Class,
    ClassesAdmin,
)
admin.site.register(
    Matter,
    MattersAdmin,
)
admin.site.register(
    Grade,
    GradesAdmin,
)
admin.site.register(
    Absence,
    AbsencesAdmin,
)
admin.site.register(
    AcademicHistory,
    AcademicHistoryAdmin,
)
admin.site.register(SchoolEvent, SchoolEventAdmin)
admin.site.register(ClassSchedule, ClassScheduleAdmin)
