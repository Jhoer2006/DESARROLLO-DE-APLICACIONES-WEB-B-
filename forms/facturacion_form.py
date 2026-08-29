from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, DateField, DecimalField, SubmitField
from wtforms.validators import DataRequired, Length, NumberRange


class FacturacionForm(FlaskForm):

    numero = StringField(
        "Número de factura",
        validators=[
            DataRequired(message="El número de factura es obligatorio."),
            Length(
                min=3,
                max=20,
                message="El número debe tener entre 3 y 20 caracteres."
            )
        ]
    )

    cliente = StringField(
        "Cliente",
        validators=[
            DataRequired(message="El cliente es obligatorio."),
            Length(
                min=3,
                max=100,
                message="El cliente debe tener entre 3 y 100 caracteres."
            )
        ]
    )

    servicio = StringField(
        "Servicio",
        validators=[
            DataRequired(message="El servicio es obligatorio."),
            Length(
                min=3,
                max=100,
                message="El servicio debe tener entre 3 y 100 caracteres."
            )
        ]
    )

    fecha = DateField(
        "Fecha",
        format="%Y-%m-%d",
        validators=[
            DataRequired(message="La fecha es obligatoria.")
        ]
    )

    total = DecimalField(
        "Total",
        places=2,
        validators=[
            DataRequired(message="El total es obligatorio."),
            NumberRange(
                min=0,
                message="El total debe ser mayor o igual a 0."
            )
        ]
    )

    estado = SelectField(
        "Estado",
        choices=[
            ("", "Seleccione un estado"),
            ("Pagada", "Pagada"),
            ("Pendiente", "Pendiente")
        ],
        validators=[
            DataRequired(message="Debe seleccionar un estado.")
        ]
    )

    submit = SubmitField("Guardar")