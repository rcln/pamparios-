
from az_app.models import applicationModel

import os
import tempfile


from pdf2image import convert_from_path


from PIL import Image

from pytesseract import image_to_string, pytesseract, image_to_data, Output


def show_each_file_pages_images(filename):

    name_with_extension = filename + '.pdf'

    doc_owner = applicationModel.DocumentAdded.query.filter_by(name_doc=name_with_extension).first()

    doc_page_progr = applicationModel.DocAddedPageProgress.query.filter_by(id_fk_doc_added=doc_owner.id_doc)

    return doc_page_progr


def show_each_file_images(filename):


    name_with_extension = filename+'.pdf'

    upl_doc = applicationModel.DocumentAdded.query.filter_by(name_doc=name_with_extension).first()

    strt_page = upl_doc.scan_start_doc

    end_page = upl_doc.scan_end_doc + 1

    tabl_pages = []

    for page_incr in range(strt_page, end_page):

        print(filename + '__page_'+str(page_incr)+'.jpg')

        tabl_pages.append(filename + '__page_'+str(page_incr)+'.jpg')


    return tabl_pages


def show_cover_pages_name():

    upl_docs = applicationModel.DocumentAdded.query.all()

    img_path = '/app_ressources/translator_ressources/app_files_cover_page/'

    tableau = []

    for docu in upl_docs:
        tableau.append(img_path+os.path.splitext(docu.name_doc)[0] + '__COVER_PAGE.jpg')

    return tableau


def create_first_page_images():

    upl_docs = applicationModel.DocumentAdded.query.all()

    output_path = 'az_app/app_ressources/translator_ressources/app_files_cover_page/'

    input_path = 'az_app/app_ressources/translator_ressources/uploaded_files'

    for doc in upl_docs:

        filename = input_path + '/' + doc.name_doc

        with tempfile.TemporaryDirectory() as path:

            pdf_to_convert = convert_from_path(filename, output_folder=path, last_page=1, first_page=1)

        print(filename)

        for page in pdf_to_convert:

            convers_resul_image = os.path.splitext(os.path.basename(filename))[0] + '__COVER_PAGE.jpg'

            page.save(os.path.join(output_path, convers_resul_image), 'JPEG')

            print(convers_resul_image)

    return True


def create_respective_dir():
    upl_docs = applicationModel.DocumentAdded.query.all()

    output_path = 'az_app/app_ressources/translator_ressources/converted_files'

    extracted_path = 'az_app/app_ressources/translator_ressources/txt_extracted_files'

    for doc in upl_docs:

        convers_each_dir = output_path + '/' + doc.name_doc
        path_relative_image = os.path.splitext(convers_each_dir)[0]

        extracted_each_dir = extracted_path + '/' + doc.name_doc
        path_relative_txt_extracted = os.path.splitext(extracted_each_dir)[0]

        try:

            os.mkdir(path_relative_image)
            os.mkdir(path_relative_txt_extracted)
        except OSError:

            print("Creation of the directory %s failed" % path_relative_image)
        else:

            print("Creation of the directory %s Succeed" % path_relative_image)

    return True


def transform_to_images():

    upl_docs = applicationModel.DocumentAdded.query.all()

    output_path = 'az_app/app_ressources/translator_ressources/converted_files'

    input_path = 'az_app/app_ressources/translator_ressources/uploaded_files'

    for doc in upl_docs:

        convers_start_page = doc.scan_start_doc
        convers_end_page = doc.scan_end_doc

        filename = input_path + '/' + doc.name_doc

        convers_each_dir = output_path + '/' + doc.name_doc
        path_relative_image = os.path.splitext(convers_each_dir)[0]

        with tempfile.TemporaryDirectory() as path:

            pdf_to_convert = convert_from_path(filename, output_folder=path, last_page=convers_end_page, first_page=convers_start_page)

        page_incr = convers_start_page

        print(filename)

        for page in pdf_to_convert:

            convers_resul_image = os.path.splitext(os.path.basename(filename))[0] + '__page_' + str(page_incr) + '.jpg'

            page_name = os.path.splitext(doc.name_doc)[0] + '__page_' + str(page_incr) + '.jpg'

            doc_page_progress = applicationModel.DocAddedPageProgress(doc.id_doc, page_name, 0)

            # --------------
            applicationModel.db_con.session.add(doc_page_progress)

            applicationModel.db_con.session.commit()
            # --------------

            page.save(os.path.join(path_relative_image, convers_resul_image), 'JPEG')

            page_incr = page_incr + 1

            print(convers_resul_image)

    return True


def extract_words_from_images():

    tesseract_cmd = '../../../azenv/lib/python3.6/site-packages/pytesseract'

    upl_docs = applicationModel.DocumentAdded.query.all()

    for doc in upl_docs:

        convers_start_page = doc.scan_start_doc
        convers_end_page = doc.scan_end_doc

        path_relative_image = os.path.splitext('az_app/app_ressources/translator_ressources/converted_files/' + doc.name_doc)[0]

        path_relative_txt_extracted = os.path.splitext('az_app/app_ressources/translator_ressources/txt_extracted_files/' + doc.name_doc)[0]

        for img_incr in range(convers_start_page, convers_end_page+1):

            all_text_extracted = ""

            image_name = os.path.splitext(doc.name_doc)[0]+'__page_'+str(img_incr)+'.jpg'
            text_file_name = os.path.splitext(doc.name_doc)[0]+'__page_'+str(img_incr)+'.txt'

            the_image_to_extract = path_relative_image+'/'+image_name

            opened_image = Image.open(the_image_to_extract)

            extraction_to_data_result = image_to_data(opened_image, output_type=Output.DICT)

            progress_percent = 0

            pre_line_number = 0

            for i in range(len(extraction_to_data_result['text'])):

                line_number = extraction_to_data_result['block_num'][i]

                if pre_line_number == line_number:

                    all_text_extracted = all_text_extracted + " " + extraction_to_data_result['text'][i]

                elif pre_line_number == line_number - 1:

                    all_text_extracted = all_text_extracted + "\n" + extraction_to_data_result['text'][i]

                    pre_line_number = extraction_to_data_result['block_num'][i]

                progress_percent = round((i/(len(extraction_to_data_result['text'])))*100)

                print('PROGRESSION = '+str(progress_percent)+'%')

                if extraction_to_data_result['text'][i] != '':

                    if applicationModel.ExtractedWords.query.filter_by(word=extraction_to_data_result['text'][i]).first() is None:

                        extracted_data = applicationModel.ExtractedWords(id_fk_doc_added=doc.id_doc, word=extraction_to_data_result['text'][i],
                                                                         w_height=extraction_to_data_result['height'][i], w_width=extraction_to_data_result['width'][i],
                                                                         w_pos_top=extraction_to_data_result['top'][i], w_pos_left=extraction_to_data_result['left'][i])
                        applicationModel.db_con.session.add(extracted_data)
                        applicationModel.db_con.session.commit()

            final_progress = progress_percent

            doc_added_page_progress = applicationModel.DocAddedPageProgress.query.filter_by(doc_added_page_name=image_name).first()

            doc_added_page_progress.page_progress = final_progress

            applicationModel.db_con.session.commit()

            txt_to_create = open(path_relative_txt_extracted+'/'+text_file_name, 'w+')

            txt_to_create.write(all_text_extracted)

            print('Ecriture reussi '+the_image_to_extract+ ' LA PROGRESSION FINALE EST : '+str(final_progress)+'%')

    return True
