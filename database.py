from app import app, db

# Import your database model
from app import doctorData
from app import add_doctor
from app import contact
from app import Blog
from app import signup
# from app import UserData
from alembic import op
import sqlalchemy as sa
# You don't need to create the app object again, as it's already defined in app.py.
def upgrade():
    # Create the tables based on the defined models
    with op.batch_alter_table('add_doctors') as batch_op:
        batch_op.alter_column('photopath', type_=sa.LargeBinary(), using='photopath::bytea')

def downgrade():
    # If needed, provide a downgrade operation
    pass
# Create the tables based on the defined models
with app.app_context():
    db.create_all()

# error of flask_migration
# python app.py db revision --rev-id e39d16e62810  
# python app.py db migrate  
# python app.py db upgrade

####solution
# $ flask db stamp head
# $ flask db migrate

# $ flask db upgrade


# flask db init
# flask db migrate
# flask db upgrade


