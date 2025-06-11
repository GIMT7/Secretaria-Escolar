from django.core.exceptions import ValidationError
import re
from validate_docbr import CPF

# Validador de CPF: utiliza a biblioteca validate_docbr para verificar se o CPF é válido.
# Se o CPF não for válido, lança um ValidationError.
def cpf_validator(value):
    cpf = CPF()
    if not cpf.validate(value):
        raise ValidationError(
            ("%(value)s is not valid"),
            params={"value": value},
        )

# Validador de CEP: verifica se o CEP possui 8 dígitos e se está no formato numérico correto.
def cep_validator(value):
    # Verifica se o CEP tem exatamente 8 caracteres
    if not len(value) == 8:
        raise ValidationError(
            ("%(value)s is not valid"),
            params={"value": value},
        )
    # Expressão regular para garantir que o CEP tenha apenas números
    pattern = re.compile(r"(\d){5}(\d){3}")
    if not re.match(pattern, value):
        raise ValidationError(
            ("%(value)s is not valid"),
            params={"value": value},
        )

# Validador de telefone: exige o formato (XX) 9XXXX-XXXX, onde XX é o DDD e o número começa com 9.
def phone_validator(value):
    pattern = r"^\(\d{2}\) 9\d{4}-\d{4}$"
    # Verifica se o telefone está no formato correto
    if not re.match(pattern, value):
        raise ValidationError(
            ("%(value)s is not valid"),
            params={"value": value},
        )

# Validador de nota escolar: garante que a nota esteja entre 0 e 10.
def validate_nota(value):
    # Se a nota não estiver no intervalo permitido, lança um erro
    if not (0 <= value <= 10):
        raise ValidationError(
            f"Nota inválida: {value}. A nota deve estar entre 0 e 10."
        )
