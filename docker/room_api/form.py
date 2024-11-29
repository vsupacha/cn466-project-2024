from flask_wtf import FlaskForm
from wtforms import StringField, HiddenField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, InputRequired, Optional

# Add User Form
class RoomForm(FlaskForm):
    room_id = StringField('Room ID', validators=[Optional()])  # Optional field for room_id
    rooms_list = HiddenField('Rooms List')  # A hidden field to hold the list of rooms (if needed)
    submit = SubmitField('Submit')

    def __init__(self, rooms=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if rooms:
            # Assuming `rooms` is a list of room identifiers or objects
            self.rooms_list.data = ','.join(str(room) for room in rooms)  # You can store it as a comma-separated string or any format you need

