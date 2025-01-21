import os
from flask import Flask, render_template, redirect, url_for, request, flash, send_file, jsonify
from werkzeug.utils import secure_filename
from config import Config
from models import db, User, Product
from forms import UserForm
import io
from datetime import datetime
import base64

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)


with app.app_context():
    db.create_all()
    
save_username = ''

# 이미지를 Base64로 인코딩하는 함수
def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
    return encoded_string

def calculate_age(birth_date):
    today = datetime.today()
    age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
    return age

@app.route('/', methods=['GET', 'POST'])
def index():
    form = UserForm()
    if form.validate_on_submit():
        user_picture = form.user_picture.data.read() if form.user_picture.data else None
        new_user = User(name=form.name.data, user_password=form.user_password.data, user_name=form.user_name.data, user_age=form.user_age.data, user_picture=user_picture)
        db.session.add(new_user)
        db.session.commit()
        flash('User successfully added', 'success')
        return redirect(url_for('index'))
    users = User.query.all()
    return render_template('index.html', form=form, users=users)

# 안드로이드 회원가입할 때 실행되는 함수
@app.route('/android', methods=['POST'])
def get_user_detail():
    global save_username
    save_username = ''
    data = request.get_json()
    print(data)
    if User.query.filter_by(user_id=data['id']).first():
        if User.query.filter_by(user_id=data['id']).first().user_id == data['id']:
            return jsonify({'message': '중복된 아이디'})
    
    try:
        datetime_obj = datetime.strptime(data['birthDate'], '%Y-%m-%d')
    except:
        return jsonify({'message': '날짜 형식이 맞지않음'})
    new_user = User(user_id=data['id'], user_password=data['password'], user_name=data['name'], user_age=datetime_obj)
    new_user.set_password(data['password'])
    db.session.add(new_user)
    db.session.commit()

    save_username = data['id']
    
    return jsonify({'message': 'User successfully added', 'success':True}), 200

# 데이터베이스 내용을 지우기 위해 임의로 만든 것
@app.route('/delete_product', methods=['GET'])
def delete_product():
    # num_deleted = db.session.query(User).delete()
    mun_deleted = db.session.query(Product).delete()
    db.session.commit()
    return jsonify({'message': 'Success'})
@app.route('/delete_user', methods=['GET'])
def delete_user():
    num_deleted = db.session.query(User).delete()
    # mun_deleted = db.session.query(Product).delete()
    db.session.commit()
    return jsonify({'message': 'Success'})

# 안드로이드 로그인할 때 호출되는 함수
@app.route('/login', methods=['POST'])
def login():
    global save_username
    save_username = ''
    data = request.get_json()
    print(data)
    username = data['id']
    password = data['password']
    
    user = User.query.filter_by(user_id=username).first()

    if user and user.check_password(password):
        save_username = user.user_id
        return jsonify({'message': 'Login successful', 'success':True}), 200
    return jsonify({'message': '아이디 또는 비밀번호 틀림'})

# 안드로이드 사진 DB에 업로드할 때 실행되는 함수
@app.route('/upload-image', methods=['POST'])
def upload_image():
    global save_username
    print(save_username)

    file = request.files['image']
    filename = secure_filename(file.filename)
    save_img = save_username + ".jpg"
    filepath = os.path.join("image", save_img)
    file.save(filepath)

    user = User.query.filter_by(user_id=save_username).first()
    user.user_picture = filepath
    db.session.commit()
    return jsonify({'message': 'Login successful', 'success':True}), 200

# 안드로이드에서 아기 얼굴 이미지 호출하는 함수
@app.route('/getImage', methods=['GET'])
def getImage():
    global save_username
    try:
        user = User.query.filter_by(user_id=save_username).first()
        image_path = user.user_picture
        image_data = encode_image(image_path)
        return jsonify({'success': True, 'imageData': image_data})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

# 안드로이드에서 아기 아기 나이 호출하는 함수
@app.route('/getUserInfo', methods=['GET'])
def getUserInfo():
    global save_username
    user = User.query.filter_by(user_id=save_username).first()
    user_birth = user.user_age
    age = calculate_age(user_birth)
    return jsonify({'success': True, 'age': age, 'name' : user.user_name})

# 안드로이드에서 아기가 학습한 날짜를 호출하는 함수
@app.route('/getStudyDates')
def getStudyDate():
    user_inform = User.query.filter_by(user_id=save_username).first()
    product_inform = Product.query.filter_by(id=user_inform.id).first()
    dates = str(product_inform.product_date)[:10]
    print(dates)
    date_list = [dates]  # 예시 데이터
    return jsonify(date_list)

@app.route('/study-data/<date>', methods=['GET'])
def get_study_data(date):
    try:
        user_inform = User.query.filter_by(user_id=save_username).first()
        if not user_inform:
            return jsonify({'error': 'User not found'}), 404

        product_inform = Product.query.filter_by(id=user_inform.id).all()
        if not product_inform:
            return jsonify({'error': 'No study data found for the user'}), 404

        study_data = []

        for product in product_inform:
            if str(product.product_date.date()) == date:
                user_image_data = encode_image(product.product_image)
                ai_image_data = encode_image(product.modify_image)
                audio_data = encode_image(product.product_audio)
                word = product.product_word
                acc = product.product_accuracy

                study_data.append({
                    'word': word,
                    'accuracy': acc,
                    'images': [
                        user_image_data,
                        ai_image_data
                    ],
                    'audioData': audio_data
                })

        if study_data:
            return jsonify(study_data)
        else:
            return jsonify({'error': 'No study data found for the given date'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# @app.route('/study-data/<date>', methods=['GET'])
# def get_study_data(date):
#     # user = User.query.filter_by(user_id='testuser').first()  # 예시로 하드코딩된 사용자 데이터 사용
#     # if not user:
#     #     return jsonify({'error': 'User not found'}), 404
#     image_data = encode_image("image/jimin.jpg")
#     audio_data = encode_image("audio/siu.mp3")
    
#     if date:  # 예시로 하드코딩된 날짜 데이터 사용
#         study_data = {
#             'word': 'example_word',
#             'accuracy': 85,
#             'images': [
#                 image_data,
#                 image_data
#             ],
#             'audioData': audio_data
#         }
#         return jsonify(study_data)
#     else:
#         return jsonify({'error': 'Study data not found for the given date'}), 404



@app.route('/upload_information', methods=['POST'])
def upload_information():
    data = request.json
    print(data)
    user = User.query.filter_by(user_id=data['user_id']).first()
    print(user)
    new_user = Product(id=user.id, product_audio=data['product_audio'], product_word=data['product_word'], product_accuracy=data['product_accuracy'], product_image=data['product_image'], modify_image=data['modify_image'])
    # new_user = User(user_id=data['user_id'], user_password=data['user_password'], user_name=data['user_name'], user_age=data['user_age'])
    db.session.add(new_user)
    db.session.commit()
    return {"success":True}






@app.route('/product', methods=['POST'])
def get_product_detail():
    data = request.get_json()
    new_product = Product(product_id=data['product_id'], product_date=data['product_date'])
    db.session.add(new_product)
    db.session.commit()
    return jsonify({'message': 'Success'})

@app.route('/user/<name>')
def user_detail(name):
    user = User.query.get_or_404(name)
    return render_template('user_detail.html', user=user)

@app.route('/user/<name>/picture')
def user_picture(name):
    user = User.query.get_or_404(name)
    return send_file(io.BytesIO(user.user_picture), mimetype='image/jpeg', as_attachment=False, download_name=f'{user.user_name}.jpg')

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)