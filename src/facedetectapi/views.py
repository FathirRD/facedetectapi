import os, json, base64, string, random , cv2

from django         import views
from django.http    import JsonResponse
from django.core.exceptions         import ValidationError
from django.views.decorators.csrf   import csrf_exempt
from django.utils.decorators        import method_decorator


class DetectFaceAPI(views.View):
    """
    Receive request and give response data in json
    Detect face from coming request with image data
    """
    
    module_dir = os.path.dirname(__file__)  # get current directory

    def post(self, request, *args, **kwargs):
        data = json.loads(request.body)
        if 'image' not in data:
            return JsonResponse({
                'status': 'fail',
                'message':'Image not provided'
            }, status=400)

        # Image convertion
        file_temp   = os.path.join(self.module_dir, 'temp/' + self.randStr(30) + ".png")
        img_data    = data['image']

        if ";base64," in img_data:
            header, img_data    = img_data.split(";base64,") 
            # file_mime_type      = header.replace("data:", "")

        try:
            with open(file_temp, "wb") as file:
                file.write(base64.b64decode(img_data))
        except (TypeError, ValueError):
            raise ValidationError("data not supported")

        # Face detection
        classifier  = cv2.CascadeClassifier(
            os.path.join(self.module_dir, 'classifiers/haarcascade_frontalface_default.xml')
        )
        img         = cv2.imread(file_temp)
        gray_img    = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces       = classifier.detectMultiScale(
                gray_img,
                scaleFactor=1.2,
                minNeighbors=5,
                minSize=(30, 30)
            )

        if len(faces) > 0:
            if 'detail' in data:
                for (x, y, w, h) in faces:
                    cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2)

                img_detail = os.path.join(self.module_dir, "temp/detail/" + self.randStr(30) + ".png") 
                cv2.imwrite(img_detail, img)

                with open(img_detail, "rb") as file:
                    file_data       = file.read()
                    encoded_data    = base64.b64encode(file_data)
                    img_str         = encoded_data.decode('utf-8')

                return JsonResponse({
                    'status': 'success',
                    'message': "face detected",
                    'total found': len(faces),
                    'faces': "data:image/png;base64," + img_str
                }, status=200)

            return JsonResponse({
                    'status': 'success',
                    'message': "face detected"
                }, status=200)
        
        return JsonResponse({
            'status': 'success',
            'message': "no face detected"
        }, status=200)

    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super(DetectFaceAPI, self).dispatch(*args, **kwargs)

    @staticmethod
    def randStr(length=10):
        return ''.join(random.choices(string.ascii_lowercase + string.digits, k=length))