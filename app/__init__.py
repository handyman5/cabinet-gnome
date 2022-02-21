from flask import Flask, Blueprint, render_template, send_from_directory, request, redirect, url_for
#from flask_bootstrap import Bootstrap

from flask_peewee.rest import RestAPI

from flask_admin import Admin
from flask_admin.contrib.peewee import ModelView

import playhouse.flask_utils

from playhouse.shortcuts import model_to_dict, dict_to_model


from peewee import *
import datetime

db = SqliteDatabase('my_database.db', pragmas={'foreign_keys': 1})



frontend = Blueprint('frontend', __name__)

class BaseModel(Model):
    class Meta:
        database = db

    
class Item(BaseModel):
    name = CharField(unique=True)
    perishable = BooleanField(default=False)
    last_purchased = DateTimeField(default=datetime.datetime.now())
    times_purchased = IntegerField(default=0)

    def __str__(self):
        return self.name
    
class Store(BaseModel):
    name = CharField(unique=True)

    def __str__(self):
        return self.name

class ItemStore(BaseModel):
    item = ForeignKeyField(Item)
    store = ForeignKeyField(Store)

    class Meta:
        indexes = (
            (("item", "store"), True),
        )
    
    
class Cabinet(BaseModel):
    item = ForeignKeyField(Item, backref='cabinet', to_field='name')
    need = BooleanField(default=False)


    
@frontend.before_request
def before_request():
    db.connect()

@frontend.after_request
def after_request(response):
    db.close()
    return response

db.connect()
db.create_tables([Store, Item, ItemStore, Cabinet])


def create_app(configfile=None):
    app = Flask(__name__)
#    Bootstrap(app)

    app.config['SECRET_KEY'] = '12345'

    api = RestAPI(app)

    # register our models so they are exposed via /api/<model>/
    api.register(Item)
    api.register(Store)
    api.register(ItemStore)
    api.register(Cabinet)

    # configure the urls
    api.setup()

    admin = Admin(app)
    admin.add_view(ModelView(Store))
    admin.add_view(ModelView(Item))
    admin.add_view(ModelView(ItemStore))
    admin.add_view(ModelView(Cabinet))

    app.register_blueprint(frontend)

    
    i = Item.get_or_create(name='Milk')
    s1 = Store.get_or_create(name='Safeway')
    s2 = Store.get_or_create(name="Trader Joe's")

#    ItemStore.create(item=i, store=s1)
    
    ItemStore.get_or_create(item=i, store=s1)
    ItemStore.get_or_create(item=i, store=s2)
    
    
    
    return app


# do something with app...

@frontend.route('/')
def index():
    return render_template('index.html')

@frontend.route('/static/<path:path>')
def send_static(path):
    return send_from_directory('static', path)

# @frontend.route('/fonts/<path:path>')
# def send_fonts(path):
#     return send_from_directory('static/fonts', path)

# @frontend.route('/css/<path:path>')
# def send_css(path):
#     return send_from_directory('static/css', path)


@frontend.route('/items')
def contents():
    output = '''
<h1>Known Items</h1>
'''
    return playhouse.flask_utils.object_list('items.html', Item.select())
#    return json.dumps(model_to_dict(items), indent=4, default=str)


@frontend.route('/stores')
def stores():
    output = '''
<h1>Stores</h1>
'''
    stores = Store.select()
    return stores


@frontend.route('/cabinet')
def cabinet():
    output = '''
<h1>Cabinet</h1>
'''
    cab = Cabinet.select()
    return cab

@frontend.route('/shopping_list')
def shopping_list():
    output = '''
<h1>Shopping List</h1>
'''

    sl = Cabinet.select().where(Cabinet.need == True)

    return sl

@frontend.route('/add')
def add_to_cabinet():
    output = '''
<h1>Add Item to Cabinet</h1>
'''

    return output


@frontend.route('/add_item', methods=['GET', 'POST'])
def add_item():
    if request.method == 'POST':
        item = Item.create(
            name=request.form.name,
            perishable=request.form.get('perishable', False),
            store_id=1
        )
        return redirect(url_for('.contents'))
    return render_template('create.html')

@frontend.route('/edit_item/<item_id>', methods=['GET', 'POST'])
def edit_item(item_id):
    item = playhouse.flask_utils.get_object_or_404(Item, Item.id == item_id)
    if request.method == 'POST':
        item.name = request.form['name']
        item.perishable = request.form.get('perishable', False)
        item.save()
        return redirect(url_for('.contents'))
    return render_template('edit_item.html', item=item)
