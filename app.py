from flask import Flask, request, render_template, jsonify

app = Flask(__name__, static_folder='static', template_folder='templates')

@app.route('/', methods=['GET', 'POST'])
def calculator():
    result = None
    if request.method == 'POST':
        try:
            num1 = float(request.form.get('num1', 0))
            num2 = float(request.form.get('num2', 0))
            operation = request.form.get('operation', 'add')
            
            if operation == 'add':
                result = f"{num1} + {num2} = {num1 + num2}"
            elif operation == 'subtract':
                result = f"{num1} - {num2} = {num1 - num2}"
            elif operation == 'multiply':
                result = f"{num1} × {num2} = {num1 * num2}"
            elif operation == 'divide':
                if num2 == 0:
                    result = "Error: Division by zero"
                else:
                    result = f"{num1} ÷ {num2} = {num1 / num2}"
            elif operation == 'power':
                result = f"{num1}^{num2} = {num1 ** num2}"
        except ValueError:
            result = "Error: Please enter valid numbers"
    
    return render_template('index.html', result=result)

def lambda_handler(event, context):
    # Handle API Gateway/Lambda events
    if 'httpMethod' in event:
        # API Gateway proxy event
        from flask import Request
        with app.test_request_context(
            path=event['path'],
            method=event['httpMethod'],
            headers=event.get('headers', {}),
            query_string=event.get('queryStringParameters', {}),
            data=event.get('body', '')
        ):
            response = app.full_dispatch_request()
            return {
                'statusCode': response.status_code,
                'headers': dict(response.headers),
                'body': response.data.decode('utf-8')
            }
    else:
        # Direct Lambda invocation or test event
        with app.test_request_context():
            response = app.full_dispatch_request()
            return {
                'statusCode': response.status_code,
                'headers': dict(response.headers),
                'body': response.data.decode('utf-8')
            }

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
