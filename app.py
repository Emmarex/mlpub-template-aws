import json
import pickle
from helper import vectorizer

classifier_folder_path = "model/movie_classifier.pkl"


def lambda_handler(event, context):
    try:
        query_params = event.get('queryStringParameters', {})
        movie_review = query_params.get('movie_review', '')
        if not movie_review:
            return {
                'statusCode': 401,
                'body': json.dumps({
                    "error": "1",
                    "message": "Invalid parameter"
                })
            }
        movie_review = [movie_review]
        vectorized_review = vectorizer.transform(movie_review)
        movie_classifier = pickle.load(open(classifier_folder_path, 'rb'))
        prediction = movie_classifier.predict(vectorized_review)
        review_sentiment = "Positive" if prediction[0] == 1 else "Negative"
        return_data = {
            "error": "0",
            "message": "Successful",
            "review_sentiment": review_sentiment
        }
        return {
            'statusCode': 200,
            'body': json.dumps(return_data)
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({
                "error": "1",
                "message": str(e)
            })
        }
