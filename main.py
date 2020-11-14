import ui
import setgen

# XXX make items editable?
conf = setgen.load_config('setgen.yaml')
builder = setgen.Builder(conf['items'])

################################################################################
def gen_button_pressed(sender):
    set_length = int(form_size_text.text)
    set = builder.build_set(set_length)

    data_source = ui.ListDataSource(items=set)

    form_set_table.data_source = data_source
    form_set_table.reload_data()

################################################################################
## MAIN ENTRY

app = ui.load_view()
form_size_text = app['size_text']
form_set_table = app['set_table']

app.present('sheet')
