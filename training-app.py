import logging
from logging.handlers import RotatingFileHandler
import os
import platform
import random
from flask import Flask, request, jsonify, render_template, render_template_string, send_from_directory
from log_config import setup_logging
from werkzeug.middleware.proxy_fix import ProxyFix
from werkzeug.utils import safe_join
from config import Config


app = Flask(__name__, static_folder="static")


def get_training_sets():
    if 'TRAINING_SETS' not in app.config:
        root_dir = app.config['TRAINING_SET_ROOT_DIR']
        try:
            app.logger.info("Scanning for available training sets...")
            sets = [
                s for s in os.listdir(root_dir)
                if os.path.isdir(os.path.join(root_dir, s))
            ]
            app.config['TRAINING_SETS'] = sets
        except FileNotFoundError:
            app.logger.error(f"Training set root directory '{root_dir}' not found.")
            app.config['TRAINING_SETS'] = []
        except PermissionError:
            app.logger.error(f"Permission denied accessing '{root_dir}'.")
            app.config['TRAINING_SETS'] = []
        except Exception as e:
            app.logger.exception(f"Unexpected error while scanning training sets: {e}")
            app.config['TRAINING_SETS'] = []
    return app.config['TRAINING_SETS']

def get_image_names(set_name):
    if 'IMAGE_SETS' not in app.config:
        app.config['IMAGE_SETS'] = {}
    image_sets = app.config['IMAGE_SETS']
    if set_name in image_sets:
        return image_sets[set_name]
    set_path = os.path.join(app.config['TRAINING_SET_ROOT_DIR'], set_name)
    try:
        files = os.listdir(set_path)
    except FileNotFoundError:
        app.logger.error(f"Directory '{set_name}' not found.")
        return []
    except PermissionError:
        app.logger.error(f"Permission denied accessing '{set_path}'.")
        return []
    except Exception as e:
        app.logger.exception(f"Unexpected error reading '{set_name}': {e}")
        return []
    images = [os.path.splitext(f)[0] for f in files if f.endswith('.jpg')]
    random.shuffle(images)
    if not images:
        app.logger.warning(f"No images found in '{set_name}'.")
        return []
    image_sets[set_name] = images
    return images

def startup_tasks():
    app.config.from_object(Config)
    setup_logging()
    app.logger.info("Running startup tasks...")
    app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1) # Apply ProxyFix middleware
    app.logger.info("LOG_LEVEL: " + app.config['LOG_LEVEL'])
    app.logger.info("TRAINING_SET_ROOT_DIR: " + app.config['TRAINING_SET_ROOT_DIR'])
    for set_name in get_training_sets():
        app.logger.info(f"{set_name}: {get_image_names(set_name)}")

with app.app_context():
    # do things before first request
    startup_tasks()

@app.route('/training_sets/<set_name>/<filename>')
def serve_media(set_name, filename):
    folder_path = safe_join(app.config['TRAINING_SET_ROOT_DIR'], set_name)
    return send_from_directory(folder_path, filename)

@app.route('/')
@app.route('/viewer')
def viewer():
    set_name = request.args.get('set')
    index = int(request.args.get('index', 0))
    root_dir = app.config['TRAINING_SET_ROOT_DIR']
    if not set_name or set_name not in get_training_sets():
        set_name = get_training_sets()[0]
    # Pick current image/audio pair
    images = get_image_names(set_name)
    current_base = images[index % len(images)]
    img_src = f"/{root_dir}/{set_name}/{current_base}.jpg"
    audio_src = f"/{root_dir}/{set_name}/{current_base}.m4a"
    audio_file = os.path.join(root_dir, set_name, f"{current_base}.m4a")
    # Prepare audio tag if file exists
    audio_tag = ""
    if os.path.isfile(audio_file):
        audio_tag = audio_src
    # determining next and previous indexes, ensuring to loop-around at the end of the list
    next_index = (index + 1) % len(images)
    previous_index = (index - 1) % len(images)
    return render_template('viewer.html', current_base=current_base, set_name=set_name, audio_tag=audio_tag, img_src=img_src, available_sets=get_training_sets(), next_index=next_index, previous_index=previous_index)
    
@app.route('/about')
def about():
    status_info = {
        'App Name': app.name,
        'Debug Mode': app.debug,
        'Platform': platform.system(),
        'Python Version': platform.python_version(),
        'Working Directory': os.getcwd(),
        'Training_Set Directory': app.config['TRAINING_SET_ROOT_DIR']
    }
    environment_variables_info = {
        'TRAINING_SET_ROOT_DIR': os.getenv("TRAINING_SET_ROOT_DIR"),
        'LOG_LEVEL': os.getenv("LOG_LEVEL")
    }
    return render_template('about.html', status_info=status_info, environment_variables_info=environment_variables_info)

if __name__ == '__main__':
    app.logger.info("training-app is starting up...")
    app.run(debug=True, host='0.0.0.0', port=5000)