ALLOWED_EXTENSIONS = {'pdf', 'docx', 'xlsx', 'txt', 'jpg', 'png'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS