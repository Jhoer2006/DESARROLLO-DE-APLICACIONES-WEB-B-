from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, SubmitField
from wtforms.validators import DataRequired, Length


class ProductoForm(FlaskForm):

    nombre = StringField(
        "Nombre del producto o servicio",
        validators=[
            DataRequired(message="El nombre es obligatorio."),
            Length(
                min=3,
                max=100,
                message="El nombre debe tener entre 3 y 100 caracteres."
            )
        ]
    )

    descripcion = TextAreaField(
        "Descripción",
        validators=[
            DataRequired(message="La descripción es obligatoria."),
            Length(
                min=10,
                max=300,
                message="La descripción debe tener entre 10 y 300 caracteres."
            )
        ]
    )

    categoria = SelectField(
        "Categoría",
        choices=[
            ("", "Seleccione una categoría"),
            ("Desarrollo", "Desarrollo"),
            ("Diseño", "Diseño"),
            ("Aplicaciones", "Aplicaciones")
        ],
        validators=[
            DataRequired(message="Debe seleccionar una categoría.")
        ]
    )

    submit = SubmitField("Guardar")