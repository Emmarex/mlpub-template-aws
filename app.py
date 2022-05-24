import json
import pickle
from pre_processor import input_parser

classifier_folder_path = ""


def lambda_handler(event, context):
    try:
        query_params = event.get("queryStringParameters", {})
        movie_review = query_params.get("movie_review", "")
        if not movie_review:
            return {
                "statusCode": 401,
                "body": json.dumps({"error": "1", "message": "Invalid parameter"}),
            }
        movie_review = [movie_review]
        is_successful, msg, return_data = input_parser(movie_review)
        if is_successful:
            movie_classifier = pickle.load(open(classifier_folder_path, "rb"))
            prediction = movie_classifier.predict(return_data)
            review_sentiment = "Positive" if prediction[0] == 1 else "Negative"
            return_data = {
                "error": "0",
                "message": "Successful",
                "data": review_sentiment,
            }
            return {"statusCode": 200, "body": json.dumps(return_data)}
        else:
            return {
                "statusCode": 500,
                "body": json.dumps({"error": "1", "message": msg}),
            }
    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"error": "1", "message": str(e)}),
        }
