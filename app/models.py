"""
Definition of models.
"""

from django.db import models
from django.db.models import Max

# Create your models here.

class Organization (models.Model):
    class Meta:
        db_table = 'organization'
    code = models.CharField("Código",max_length=10,
                                help_text="´Designador curto da Organização (sem esppaços)")

    name = models.CharField("Nome",max_length=60,
                                help_text="Nome da Organização")
    comment = models.TextField("Comentário", default=None, blank=True, null=True,
                                help_text="Comentários ou Descrição da Organização")

    # This function appear, instead of the pk on fields associated with this model 
    def __str__(self):
        return self.name


class Activity_Model (models.Model):
    class Meta:
        db_table = 'activity_model'
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    prefix = models.CharField("Prefíxo",max_length=2,default="A0",
                                help_text="Código Prefixo para o modelo ex. 'A0'")
    description = models.TextField("Descrição", default="AS-IS", blank=True, null=True,
                                help_text="Descrição do model ex. 'AS-IS'")

    # This function appear, instead of the pk on fields associated with this model 
    def __str__(self):
        return self.prefix + " - " + self.description


def get_diagram_file_path(instance, filename): 
    ext = filename.split('.')[-1]
    organization = instance.activity_model.organization.code
    activity_model = instance.activity_model.prefix
    code = instance.code
    filename = "%s/%s/%s.%s" % (organization, activity_model, code, ext) 
    return 'diagrams/%s' % (filename)

  
class Activity (models.Model):
    class Meta:
        db_table = 'activity'
    activity_model = models.ForeignKey(Activity_Model, on_delete=models.CASCADE)
    code = models.CharField("Código",max_length=80, default=None, blank=True, null=True,
                                help_text="Código único identificador da atividade")
    name = models.CharField("Nome",max_length=80,
                                help_text="Nome da Atividade")
    definition = models.TextField("Definição da Atividade", default=None, blank=True, null=True,
                                help_text="Definição textual da Atividade")
    diagram = models.ImageField(upload_to=get_diagram_file_path, default='nodiagram.jpg', blank=True, null=True,
                                verbose_name="Diagram")
    object = models.CharField("Objeto", max_length=80, default=None, blank=True, null=True,
                                help_text="Objeto no Diagrama da atividade parent que corresponde a atividade")
    parent = models.ForeignKey('self', on_delete=models.CASCADE, default=None, blank=True, null=True,
                                help_text="Atividade parent no modelo")
    sequence = models.PositiveIntegerField("Número de Sequência", default=0, blank=True, null=True,
                                help_text="Número de sequência da atividade na atividade parent")

    def save(self, *args, **kwargs):
        if not Activity.objects.filter(id=self.id).exists():
            if self.parent is not None:
                if Activity.objects.filter(parent=self.parent).exists():
                    last = Activity.objects.filter(parent=self.parent.id).aggregate(last_sequence=Max('sequence'))
                    self.sequence = last['last_sequence'] + 1
                else:
                    self.sequence = 1
                parent = Activity.objects.get(id=self.parent.id)
                self.code = parent.code + '.' + str(self.sequence)
            else:
                model = Activity_Model.objects.get(id=self.activity_model.id)
                self.code = model.prefix
        super(Activity, self).save(*args, **kwargs)


    @property
    def get_activity_path(self):
        path = []
        current = self
        while current is not None:
            path.append(current)
            current = current.parent
        #optional return reversed list:
        return list(reversed(path))


    # This function appear, instead of the pk on fields associated with this model 
    def __str__(self):
        return self.code + " - " + self.name

