from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from azure.cognitiveservices.vision.computervision.models import VisualFeatureTypes
from msrest.authentication import CognitiveServicesCredentials

# Get endpoint and key from environment variables
import os
# endpoint = os.environ['https://southeastasia.api.cognitive.microsoft.com/vision/v2.0/analyze']
key = '88d296794b8d4067a7275ca9298b5e0e'
endpoint = 'https://southeastasia.api.cognitive.microsoft.com'


# Set credentials
credentials = CognitiveServicesCredentials(key)

# Create client
client = ComputerVisionClient(endpoint, credentials)

url = "https://upload.wikimedia.org/wikipedia/commons/0/01/Bill_Gates_July_2014.jpg"

image_analysis = client.analyze_image(
    url, visual_features=[VisualFeatureTypes.tags])

for tag in image_analysis.tags:
    print(tag)

models = client.list_models()

for x in models.models_property:
    print(x)

# type of prediction
domain = "landmarks"

# Public domain image of Eiffel tower
url = "https://images.pexels.com/photos/338515/pexels-photo-338515.jpeg"

# English language response
language = "en"

analysis = client.analyze_image_by_domain(domain, url, language)

for landmark in analysis.result["landmarks"]:
    print(landmark["name"])
    print(landmark["confidence"])


# domain = "landmarks"
# url = "http://www.public-domain-photos.com/free-stock-photos-4/travel/san-francisco/golden-gate-bridge-in-san-francisco.jpg"
# language = "en"
# max_descriptions = 3

# analysis = client.describe_image(url, max_descriptions, language)

# for caption in analysis.captions:
#     print(caption.text)
#     print(caption.confidence)
