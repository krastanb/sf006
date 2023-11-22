
from django import template

register = template.Library()

badwords = ['украина',
            'украине',
            'украины']

# Регистрируем наш фильтр под именем currency, чтоб Django понимал,
# что это именно фильтр для шаблонов, а не простая функция.
@register.filter()
def censor(value):
   """
   value: значение, к которому нужно применить фильтр
   """
   # Возвращаемое функцией значение подставится в шаблон.
   if type(value) != str: 
      raise TypeError

   for word in badwords:
      temp = value.lower().find(word) 
      while temp!=-1:
        count = (len(word)-1)
        value = value[:temp+1] + '*'*count + value[temp+count+1:]
        temp = value.lower().find(word) 
   return f'{value}'