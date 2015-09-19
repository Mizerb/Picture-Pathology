"""
Simple example showing Clarifai Custom Model training and prediction
This example trains a concept classifier that recognizes photos of the band Phish.
"""

from clarifai_basic import ClarifaiCustomModel
import sys





# ARGS need to be 'MODEL' 'POSITIVE IMAGE LIST.txt' 'NEGATIVE IMAGE LIST.txt'
Model_name = str(sys.argv[1])
Positive_File = str(sys.argv[2])
Negative_File = str(sys.argv[3])




# instantiate clarifai client
clarifai = ClarifaiCustomModel()

#[line.strip() for line in open("C:/name/MyDocuments/numbers", 'r')]

# add the positive example images to the model
for positive_example in [ line.strip() for line in (open(Positive_File)).readlines() ]:
  clarifai.positive(positive_example, Model_name)

# negatives are not required but will help if you want to discriminate between similar concepts


# add the negative example images to the model
for negative_example in [ line.strip() for line in (open(Negative_File)).readlines() ]:
  clarifai.negative(negative_example, Model_name)

# train the model
clarifai.train(Model_name)

""""
PHISH_EXAMPLES = [
  'https://clarifai-test.s3.amazonaws.com/photo-1-11-e1342391144673.jpg',
  'https://clarifai-test.s3.amazonaws.com/DSC01226-e1311293061704.jpg'
]

NOT_PHISH = [
  'https://clarifai-test.s3.amazonaws.com/2141620332_2b741028b3.jpg',
  'https://clarifai-test.s3.amazonaws.com/grateful_dead230582_15-52.jpg'
]

# If everything works correctly, the confidence that true positive images are of Phish should be
# significantly greater than 0.5, which is the same as choosing at random. The confidence that true
# negative images are Phish should be significantly less than 0.5.

# use the model to predict whether the test images are Phish or not
for test in PHISH_EXAMPLES + NOT_PHISH:
  result = clarifai.predict(test, 'Skin')
  print result['status']['message'], "%0.3f" % result['urls'][0]['score'], result['urls'][0]['url']

# Our output is the following. Your results will vary as there are some non-deterministic elements
# of the algorithms used.

# Success 0.797 http://phishthoughts.com/wp-content/uploads/2012/07/photo-1-11-e1342391144673.jpg
# Success 0.706 http://bobmarley.cdn.junip.com/wp-content/uploads/2014/10/DSC01226-e1311293061704.jpg
# Success 0.356 http://farm3.static.flickr.com/2161/2141620332_2b741028b3.jpg
# Success 0.273 http://www.mediaspin.com/joel/grateful_dead230582_15-52.jpg
"""