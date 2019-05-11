
import xmlrpc.client
import xmlrpc.server


'''
This method is designed just for two digits

This is how translation services work

MAYA = 1
SPANISH = 2
ENGLISH = 3
WIXARIKA = 4
FRENCH = 5

This means 
SPANISH-MAYA TRANSLATOR SERVICE MUST LISTEN ON PORT : 8021
MAYA-SPANISH TRANSLATOR SERVICE MUST LISTEN ON PORT : 8012

SPANISH-WIXARIKA TRANSLATOR SERVICE MUST LISTEN ON PORT : 8024
WIXARIKA-SPANISH TRANSLATOR SERVICE MUST LISTEN ON PORT : 8042  AND SO ON

The third digit of the port matches to the number of the first language and the fourth to the number of the second language



'''


def translate(text, first_lang, second_lang):

    '''

    :param text: the text to translate
    :param first_lang: the primary language of the text
    :param second_lang: the language in which the text should be translated
    :return: the translation of the text given

    this service is called from the view "/ocr/traduct/" in file "az_app/views/admin_views_route.py"

    '''

    print(first_lang)
    print(second_lang)


    proxy = xmlrpc.client.ServerProxy("http://localhost:8" + first_lang + second_lang[-1:] + "/RPC2")

    print(proxy)

    params = {"text": text, "align": "false", "report-all-factors": "false"}

    text_translated = proxy.translate(params)

    print('The service is working !!!')
    return text_translated['text']
