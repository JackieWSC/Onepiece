from io import BytesIO, StringIO
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa


def render_to_pdf(template_src, context_dict={}):
    template = get_template(template_src)
    html = template.render(context_dict)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return None


def render_to_pdf_file(template_src, context_dict={}):
    template = get_template(template_src)
    html = template.render(context_dict)
    #myfile = StringIO()
    #pisa.CreatePDF(html.encode("UTF-8"), myfile, encoding='UTF-8')
    pdfFile = open("temp.pdf", 'wb')

    pdf = pisa.pisaDocument(BytesIO(html.encode("UTF-8")), pdfFile)
    if not pdf.err:
        pdfFile.close()
        return pdfFile
    return None

