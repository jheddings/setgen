import ui
import setgen

################################################################################
def gen_button_pressed(sender):
    set_length = int(app['size_text'].text)

    #for set_num in range(num_sets):
    set = builder.build_set(set_length)

    set_table = app['set_table']
    data_source = ui.ListDataSource(items=set)

    set_table.data_source = data_source
    set_table.reload_data()

################################################################################
## MAIN ENTRY

# XXX make items editable?
conf = setgen.load_config('setgen.yaml')
builder = setgen.Builder(conf['items'])

app = ui.load_view()
app.present('sheet')
