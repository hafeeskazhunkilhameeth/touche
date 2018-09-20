from frappe import _

def get_data():
   return {
      'heatmap': True,
	  'fieldname': 'fall',
      'transactions': [
         {
            'label': _('Referenzen'),
            'items': ['Touche Beratung']
         }
      ]
   }