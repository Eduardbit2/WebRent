from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from tinymce.models import HTMLField
import os

User = get_user_model()


class Tenant(models.Model):
    """Модель арендатора"""
    name = models.CharField(
        max_length=255,
        verbose_name="Название компании"
    )
    tax_id = models.CharField(
        max_length=20,
        unique=True,
        verbose_name="ИНН"
    )
    address = models.TextField(
        verbose_name="Юридический адрес",
        blank=True,
        null=True
    )
    description = models.TextField(
        verbose_name="Общая информация",
        blank=True,
        null=True
    )
    bank_name = models.CharField(
        max_length=255,
        verbose_name="Банк",
        blank=True,
        null=True
    )
    bik = models.CharField(
        max_length=9,
        verbose_name="БИК",
        blank=True,
        null=True
    )
    account_number = models.CharField(
        max_length=20,
        verbose_name="Расчетный счет",
        blank=True,
        null=True
    )
    correspondent_account = models.CharField(
        max_length=20,
        verbose_name="Корреспондентский счет",
        blank=True,
        null=True
    )
    phone = models.CharField(
        max_length=20,
        verbose_name="Телефон",
        blank=True,
        null=True
    )
    email = models.EmailField(
        verbose_name="Email",
        blank=True,
        null=True
    )
    # HEX-код цвета
    color = models.ForeignKey(
        "TenantColor",
        on_delete=models.SET_NULL,
        null=True,
        verbose_name="Цвет арендатора"
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата создания"
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="Дата обновления"
    )

    class Meta:
        verbose_name = "Арендатор"
        verbose_name_plural = "Арендаторы"
        ordering = ['name']

    def __str__(self):
        return self.name


class Unit(models.Model):
    """Модель помещения"""
    STATUS_CHOICES = [
        ('rented', 'В аренде'),
        ('free', 'Свободно'),
        ('reserved', 'В резерве')
    ]

    FLOOR_CHOICES = [(str(i), f"{i} этаж") for i in range(1, 9)]  # 8 этажей

    number = models.CharField(
        max_length=10,
        unique=True,
        verbose_name="Номер помещения"
    )
    floor = models.CharField(
        max_length=2,
        choices=FLOOR_CHOICES,
        verbose_name="Этаж"
    )
    area = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        verbose_name="Площадь (кв.м)"
    )
    height = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        verbose_name="Высота (м)"
    )
    tenant = models.ForeignKey(
        Tenant,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Арендатор",
        related_name="units"
    )
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='free',
        verbose_name="Статус"
    )
    lease_start = models.DateField(
        null=True,
        blank=True,
        verbose_name="Дата начала аренды"
    )
    lease_end = models.DateField(
        null=True,
        blank=True,
        verbose_name="Дата окончания аренды"
    )

    class Meta:
        verbose_name = "Помещение"
        verbose_name_plural = "Помещения"
        ordering = ['floor', 'number']

    def clean(self):
        """Проверка дат"""
        cleaned_data = super().clean()
        status = cleaned_data.get('status')
        tenant = cleaned_data.get('tenant')
        lease_start = cleaned_data.get('lease_start')
        lease_end = cleaned_data.get('lease_end')

        if status == 'free':
            # Принудительно ставим None, чтобы очистить их при сохранении
            cleaned_data['tenant'] = None
            cleaned_data['lease_start'] = None
            cleaned_data['lease_end'] = None

        elif status == 'rented':
            if not tenant:
                self.add_error(
                    'tenant',
                    "Для статуса 'В аренде' необходимо указать Арендатора."
                )

        if lease_start and lease_end:
            if lease_start > lease_end:
                self.add_error(
                    'lease_start',
                    "Дата начала аренды не может быть позднее даты окончания."
                )
        return cleaned_data

    def __str__(self):
        return f"{self.number} ({self.get_floor_display()}) - {self.get_status_display()}"


class ContactPerson(models.Model):
    """Контактные лица арендатора"""
    tenant = models.ForeignKey(
        Tenant,
        on_delete=models.CASCADE,
        related_name="contacts"
    )
    name = models.CharField(
        max_length=255,
        verbose_name="ФИО"
    )
    position = models.CharField(
        max_length=255,
        verbose_name="Должность",
        blank=True,
        null=True
    )
    phone = models.CharField(
        max_length=20,
        verbose_name="Телефон",
        blank=True,
        null=True
    )
    email = models.EmailField(
        verbose_name="Email",
        blank=True,
        null=True
    )

    class Meta:
        verbose_name = "Контактное лицо"
        verbose_name_plural = "Контактные лица"

    def __str__(self):
        return f"{self.name} ({self.position})"


class TenantFile(models.Model):
    """Файлы, прикрепленные к арендатору"""
    tenant = models.ForeignKey(
        Tenant,
        on_delete=models.CASCADE,
        related_name="files"
    )
    name = models.CharField(
        max_length=255,
        verbose_name="Название файла"
    )
    description = models.TextField(
        verbose_name="Описание",
        blank=True,
        null=True
    )
    file = models.FileField(
        upload_to='tenants/files/',
        verbose_name="Файл"
    )
    uploaded_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name="Добавил"
    )
    uploaded_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата загрузки"
    )

    class Meta:
        verbose_name = "Файл арендатора"
        verbose_name_plural = "Файлы арендаторов"

    def __str__(self):
        return self.name


class TenantColor(models.Model):
    """Цвет арендатора, управляется через админку"""
    color = models.CharField(max_length=7, unique=True, verbose_name="Цвет (HEX)")

    class Meta:
        verbose_name = "Цвет арендатора"
        verbose_name_plural = "Цвета арендаторов"

    def __str__(self):
        return self.color


class Comment(models.Model):
    """Модель комментариев для арендаторов и помещений"""
    tenant = models.ForeignKey(
        "Tenant",
        on_delete=models.CASCADE,
        related_name="comments",
        null=True,
        blank=True
    )
    unit = models.ForeignKey(
        "Unit",
        on_delete=models.CASCADE,
        related_name="comments",
        null=True,
        blank=True
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="Автор"
    )
    text = models.TextField(verbose_name="Текст комментария")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")

    def __str__(self):
        return f"Комментарий от {self.author} ({self.created_at})"

    class Meta:
        verbose_name = "Комментарий"
        verbose_name_plural = "Комментарии"
        ordering = ['-created_at']


class CommentAttachment(models.Model):
    """Файлы, прикрепленные к комментариям"""
    comment = models.ForeignKey(
        Comment,
        on_delete=models.CASCADE, 
        related_name="attachments"
    )
    file = models.FileField(upload_to='comments/attachments/', verbose_name="Файл")
    uploaded_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата загрузки")

    @property
    def filename(self):
        return os.path.basename(self.file.name)

    def __str__(self):
        return f"Файл для комментария {self.comment.id}"


class Page(models.Model):
    title = models.CharField(max_length=200)
    content = HTMLField()
