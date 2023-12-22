from flask import Flask, request, jsonify
from flask_cors import CORS
from celery import Celery
from flashcard_generator.wikipedia_generator import get_flashcards

app = Flask(__name__)
CORS(app)

# Configure Celery
app.config['CELERY_broker_url'] = 'redis://localhost:6379/0'
app.config['result_backend'] = 'redis://localhost:6379/0'
app.config['worker_concurrency'] = 1

celery = Celery(app.name, broker=app.config['CELERY_broker_url'])
celery.conf.update(app.config)

@celery.task(bind=True)
def long_running_operation(self, topic, num_flashcards):
    # Update state
    flashcards = []
    for i,flashcard in enumerate(get_flashcards(topic, num_flashcards)):
        progress = int(100 * (i+1) / num_flashcards)
        self.update_state(state='PROGRESS', meta={'progress': progress})
        flashcards.append(flashcard)
    return {'result': flashcards, 'progress': 100}

@app.route('/start_operation', methods=['POST'])
def start_operation():
    data = request.get_json()
    topic = data.get('topic',"Python Programming")
    num_flashcards = int(data.get('num_flashcards', 10))
    task = long_running_operation.apply_async(args=[topic, num_flashcards])
    return jsonify({'task_id': task.id}), 202

@app.route('/operation_status/<task_id>', methods=['GET'])
def operation_status(task_id):
    task = long_running_operation.AsyncResult(task_id)
    if task.state == 'PENDING':
        response = {
            'state': task.state,
            'progress': 0
        }
    elif task.state != 'FAILURE':
        response = {
            'state': task.state,
            'progress': task.info.get('progress', 0)
        }
        if 'result' in task.info:
            response['result'] = task.info['result']
    else:
        # something went wrong in the background job
        response = {
            'state': task.state,
            'progress': 100,
            'status': str(task.info),  # this is the exception raised
        }
    return jsonify(response)


if __name__ == '__main__':
    CORS(app)  # This will enable CORS for all routes
    app.run(host="0.0.0.0",debug=True, port=5002)