import boto3
import joblib
from io import BytesIO

def lambda_handler(event, context):
            
    # Create S3 client
    s3 = boto3.client('s3')

    # Bucket name and path to Joblib file. Download Joblib file.
    s3 = boto3.resource('s3')
    bucket_name = 'my-bank-fraud-bucket-nwoncowocmic'
    key = 'LogisticRegressionModelFraudBankFinal.joblib'
    response = s3.Bucket(bucket_name).download_file(key, '/tmp/my-file')

    # Load the Joblib model form the downloaded data
    model = joblib.load('/tmp/my-file', mmap_mode=None)
    
    params = event['queryStringParameters']
    
    category = params['Category']
    amt = params['Amt']
    gender = params['Gender']
    zip = params['Zip']
    lat = params['Latitude']
    long = params['Longitude']
    
    categories = {'travel': 1, 'shopping_pos': 2, 'shopping_net': 3, 'personal_care': 4, 'misc_pos': 5, 'misc_net': 6, 'kids_pets': 7, 'home': 8, 'health_fitness': 9, 'grocery_pos': 10, 'grocery_net': 11, 'gas_transport': 12, 'food_dining': 13, 'entertainment': 14}
    category_value = categories[category]
    
    if (gender == 'M'):
        gender = 1
    else:
        gender = 0
    

    prediction = [[int(category_value), float(amt), int(gender), int(float(zip)), float(lat), float(long)]]
    result = model.predict(prediction)
    probabilities = model.predict_proba(prediction)
    
    result_dict = {'prediction': prediction ,'result': result.tolist(), 'fraud_probability': probabilities.tolist()} 
    return result_dict
