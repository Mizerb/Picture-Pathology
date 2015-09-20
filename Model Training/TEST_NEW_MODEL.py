from clarifai_basic import ClarifaiCustomModel
import sys

clarifai = ClarifaiCustomModel()

result = clarifai.predict('http://comps.canstockphoto.com/can-stock-photo_csp10316699.jpg', 'test5')

print result

"http://pad2.whstatic.com/images/thumb/b/bb/Get-Rid-of-Skin-Moles-Step-2-Version-3.jpg/670px-Get-Rid-of-Skin-Moles-Step-2-Version-3.jpg"

result = clarifai.predict("http://pad2.whstatic.com/images/thumb/b/bb/Get-Rid-of-Skin-Moles-Step-2-Version-3.jpg/670px-Get-Rid-of-Skin-Moles-Step-2-Version-3.jpg", 'test5')

print result


result = clarifai.predict("http://cancerousmolepictures.com/large/6/Cancerous-Mole-Pictures-1.jpg" , 'test5')

print result