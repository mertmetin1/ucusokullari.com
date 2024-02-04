from werkzeug.utils import secure_filename
from datetime import date
from email.message import EmailMessage
import random
from flask import Flask, render_template, redirect, request, send_file, session, url_for
import pymysql
import smtplib
import os

from flask import send_from_directory
from email.mime.text import MIMEText
from flask_session import Session

app = Flask(__name__)
app.config['SESSION_TYPE'] = ''
app.config['SECRET_KEY'] = ''  # Gizli anahtarınızı buraya ekleyin
Session(app)

smtp_server = "smtpout.secureserver.net"
smtp_port = 465
smtp_username = "@ucusokullari.com"
smtp_password = ""
ip_log_file = "ip_log.txt"



try:
    # Veritabanı bağlantı bilgilerini ayarlayın
    db_host = ''
    db_user = ''
    db_password = ''
    db_name = ''
    connect=pymysql.connect(cursorclass=pymysql.cursors.DictCursor ,charset='utf8mb4' ,host=db_host,user=db_user,password=db_password,db=db_name)  
    print("------------------VERİTABANI BAĞLANTISI BAŞARILI--------------------------")  
except pymysql.MySQLError as e :
    print("veri tabanı bağlantsııs başarısız",e)

# IP logunu kaydetmek için basit bir fonksiyon
def log_ip(ip_address):
    with open(ip_log_file, "a") as f:
        f.write(ip_address + "\n")



@app.route('/')
def index():
    # İstemcinin (kullanıcının) IP adresini yakala
    client_ip = request.remote_addr

    # IP adresini log'a kaydet
    log_ip(client_ip)

    return render_template("index.html")



@app.route('/kurslar')
def kurslar():
    try:
        connect=pymysql.connect(cursorclass=pymysql.cursors.DictCursor ,charset='utf8mb4' ,host=db_host,user=db_user,password=db_password,db=db_name)  
        print("------------------VERİTABANI BAĞLANTISI BAŞARILI--------------------------")  
    except pymysql.MySQLError as e :
        print("veri tabanı bağlantsııs başarısız",e)
    cursor = connect.cursor()
    cursor.execute("SELECT * FROM kurslar_ilan")
    kurslar_ilan = cursor.fetchall()
    cursor.close()
    
    #if 'ogrenci_id' in session:
        
    #    ogrenci_id = session['ogrenci_id']
        # Öğrenci oturumu var, işlemleri gerçekleştir
    return render_template("kurslar.html", kurslar_ilan=kurslar_ilan)
    #else:
     #   return "<script>alert('eğitimleri görüntülemek için giriş yap'); window.location.href='/' </script>"
    


# Kurs ilanı ekleme

@app.route('/kurs_ekle', methods=['GET', 'POST'])
def kurs_ekle():
    # Veritabanı bağlantı bilgilerini ayarlayın
    try:
        connect=pymysql.connect(cursorclass=pymysql.cursors.DictCursor ,charset='utf8mb4' ,host=db_host,user=db_user,password=db_password,db=db_name)  
        print("------------------VERİTABANI BAĞLANTISI BAŞARILI--------------------------")  
    except pymysql.MySQLError as e :
        print("veri tabanı bağlantsııs başarısız",e)   
    if request.method == 'POST':
        # Retrieve form data
        kurs_adi = request.form.get('kurs_adi').strip()
        kurs_veren_okul = request.form.get('kurs_veren_okul').strip()
        kurs_admin_username = request.form.get('kurs_admin_username').strip()
        kurs_aciklama = request.form.get('kurs_aciklama').strip()
        kurs_tarih = request.form.get('kurs_tarih').strip()
        kurs_kontenjan = request.form.get('kurs_kontenjan').strip()
        kurs_fiyat = request.form.get('kurs_fiyat').strip()

        try:
            cursor = connect.cursor()
            cursor.execute("""
                INSERT INTO kurslar_ilan (kurs_adi, kurs_veren_okul, kurs_admin_username, kurs_aciklama, kurs_tarih, kurs_kontenjan, kurs_fiyat)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (kurs_adi, kurs_veren_okul, kurs_admin_username, kurs_aciklama, kurs_tarih, kurs_kontenjan, kurs_fiyat))

            connect.commit()
            cursor.close()

            return redirect('/admin_panel')
        except Exception as e:
            print("Hata:", str(e))
            return "<script>alert('Kurs eklenirken bir hata oluştu.');</script>"
    else:
        try:
            cursor = connect.cursor()
            cursor.execute("SELECT kurs_adi FROM kurs")
            kurslar = cursor.fetchall()

            cursor.execute("SELECT kurs_admin_username FROM kurs_admin")
            kurs_admin_usernames = cursor.fetchall()

            cursor.close()

            return render_template("kurs_ekle.html", kurslar=kurslar, kurs_admin_usernames=kurs_admin_usernames)
        except Exception as e:
            print("Hata:", str(e))
            return "<script>alert('Veritabanından veriler alınırken bir hata oluştu.');</script>"



@app.route('/kullanici_kurs_ekle/<string:username>', methods=['GET', 'POST'])
def kullanici_kurs_ekle(username):
        # Veritabanı bağlantı bilgilerini ayarlayın
    try:
        connect=pymysql.connect(cursorclass=pymysql.cursors.DictCursor ,charset='utf8mb4' ,host=db_host,user=db_user,password=db_password,db=db_name)  
        print("------------------VERİTABANI BAĞLANTISI BAŞARILI--------------------------")  
    except pymysql.MySQLError as e :
        print("veri tabanı bağlantsııs başarısız",e)
    if request.method == 'POST':
        # Retrieve form data
        kurs_adi = request.form.get('kurs_adi').strip()
        kurs_veren_okul = request.form.get('kurs_veren_okul').strip()
        kurs_admin_username = username
        kurs_aciklama = request.form.get('kurs_aciklama').strip()
        kurs_tarih = request.form.get('kurs_tarih').strip()
        kurs_kontenjan = request.form.get('kurs_kontenjan').strip()
        kurs_fiyat = request.form.get('kurs_fiyat').strip()

        try:
            cursor = connect.cursor()
            cursor.execute("""
                INSERT INTO kurslar_ilan (kurs_adi, kurs_veren_okul, kurs_admin_username, kurs_aciklama, kurs_tarih, kurs_kontenjan, kurs_fiyat)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (kurs_adi, kurs_veren_okul, kurs_admin_username, kurs_aciklama, kurs_tarih, kurs_kontenjan, kurs_fiyat))

            connect.commit()
            cursor.close()

            return redirect('/kullanici_giris')
        except Exception as e:
            print("Hata:", str(e))
            return "<script>alert('Kurs eklenirken bir hata oluştu.');</script>"
    else:
        cursor = connect.cursor()
        cursor.execute("SELECT kurs_adi FROM kurs")
        kurslar = cursor.fetchall()
        cursor.close()
        return render_template("kullanici_kurs_ekle.html", kurslar=kurslar,username=username)

@app.route('/ilanlar')
def ilanlar():
    if 'admin_logged_in' not in session or not session['admin_logged_in']:
        return redirect('/admin_login')

        # Veritabanı bağlantı bilgilerini ayarlayın
    try:
        connect=pymysql.connect(cursorclass=pymysql.cursors.DictCursor ,charset='utf8mb4' ,host=db_host,user=db_user,password=db_password,db=db_name)  
        print("------------------VERİTABANI BAĞLANTISI BAŞARILI--------------------------")  
    except pymysql.MySQLError as e :
        print("veri tabanı bağlantsııs başarısız",e)
    cursor = connect.cursor()
    cursor.execute("SELECT * FROM kurslar_ilan")
    ilanlar = cursor.fetchall()
    cursor.close()
    return render_template("ilanlar.html", ilanlar=ilanlar)

@app.route('/hakkimizda')
def hakkimizda():
    return render_template('hakkimizda.html')

# Kurs ilanı düzenleme
@app.route('/kurs_duzenle/<int:kurs_ilan_id>', methods=['GET', 'POST'])
def kurs_duzenle(kurs_ilan_id):
        # Veritabanı bağlantı bilgilerini ayarlayın
    try:
        connect=pymysql.connect(cursorclass=pymysql.cursors.DictCursor ,charset='utf8mb4' ,host=db_host,user=db_user,password=db_password,db=db_name)  
        print("------------------VERİTABANI BAĞLANTISI BAŞARILI--------------------------")  
    except pymysql.MySQLError as e :
        print("veri tabanı bağlantsııs başarısız",e)
    if request.method == 'POST':
        # Retrieve form data
        kurs_adi = request.form.get('kurs_adi').strip()
        kurs_veren_okul = request.form.get('kurs_veren_okul').strip()
        kurs_admin_username = request.form.get('kurs_admin_username').strip()
        kurs_aciklama = request.form.get('kurs_aciklama').strip()
        kurs_tarih = request.form.get('kurs_tarih').strip()
        kurs_kontenjan = request.form.get('kurs_kontenjan').strip()
        kurs_fiyat = request.form.get('kurs_fiyat').strip()

        try:
            cursor = connect.cursor()
            cursor.execute("""
            UPDATE kurslar_ilan
            SET kurs_adi=%s, kurs_veren_okul=%s, kurs_admin_username=%s, kurs_aciklama=%s, kurs_tarih=%s, kurs_kontenjan=%s, kurs_fiyat=%s
            WHERE kurs_ilan_id=%s
            """, (kurs_adi, kurs_veren_okul, kurs_admin_username, kurs_aciklama, kurs_tarih, kurs_kontenjan, kurs_fiyat, kurs_ilan_id))

            connect.commit()
            cursor.close()

            return redirect('/kurslar')
        except Exception as e:
            print("Hata:", str(e))
            return "<script>alert('Kurs ilanı düzenlenirken bir hata oluştu.');</script>"
    else:
        cursor = connect.cursor()
        cursor.execute("SELECT * FROM kurslar_ilan WHERE kurs_ilan_id=%s", (kurs_ilan_id,))
        kurs = cursor.fetchone()
        cursor.close()
        return render_template("kurs_duzenle.html", kurs=kurs)




@app.route('/admin_login', methods=['GET', 'POST'])
def admin_login():
        # Veritabanı bağlantı bilgilerini ayarlayın
    try:
        connect=pymysql.connect(cursorclass=pymysql.cursors.DictCursor ,charset='utf8mb4' ,host=db_host,user=db_user,password=db_password,db=db_name)  
        print("------------------VERİTABANI BAĞLANTISI BAŞARILI--------------------------")  
    except pymysql.MySQLError as e :
        print("veri tabanı bağlantsııs başarısız",e)
    if request.method == 'POST':
        admin_username = request.form.get('admin_username').strip()
        admin_password = request.form.get('admin_password').strip()

        cursor = connect.cursor()
        cursor.execute("""
            SELECT *
            FROM master_admin
            WHERE admin_username = %s AND admin_password = %s
        """, (admin_username, admin_password))
        admin = cursor.fetchone()
        cursor.close()

        if admin:
            # Oturumu başlat ve admin kullanıcısını oturum verilerine kaydet
            session['admin_logged_in'] = True
            session['admin_username'] = admin_username

            return redirect('/admin_panel')
        else:
            return "<script>alert('Geçersiz kullanıcı adı veya şifre.'); window.location.href='/' </script>"
    else:
        return render_template('admin_login.html')




@app.route('/admin_panel')
def admin_panel():
        # Veritabanı bağlantı bilgilerini ayarlayın
    try:
        connect=pymysql.connect(cursorclass=pymysql.cursors.DictCursor ,charset='utf8mb4' ,host=db_host,user=db_user,password=db_password,db=db_name)  
        print("------------------VERİTABANI BAĞLANTISI BAŞARILI--------------------------")  
    except pymysql.MySQLError as e :
        print("veri tabanı bağlantsııs başarısız",e)
    # Oturum verilerini kontrol et
    if 'admin_logged_in' not in session or not session['admin_logged_in']:
        return redirect('/admin_login')

    cursor = connect.cursor()
    cursor.execute("SELECT * FROM kurs")
    dersler = cursor.fetchall()

    cursor.execute("SELECT * FROM ogrenci")
    ogrenciler = cursor.fetchall()

    cursor.execute("SELECT * FROM kurslar_ilan")
    ilanlar = cursor.fetchall()

    cursor.execute("""
        SELECT r.rezervasyon_id, r.rezervasyon_tarih, o.ogrenci_isim, o.ogrenci_soyisim, r.kurs_ilan_id
        FROM rezervasyonlar r
        INNER JOIN ogrenci o ON r.ogrenci_id = o.ogrenci_id
    """)
    rezervasyonlar = cursor.fetchall()

    cursor.execute("SELECT * FROM kurs_admin")
    kullanici_listesi = cursor.fetchall()

    cursor.close()
    dekont_listesi = os.listdir(app.config['UPLOAD_FOLDER'])
    return render_template("admin_panel.html",dekontlar=dekont_listesi, ogrenciler=ogrenciler, dersler=dersler, ilanlar=ilanlar, rezervasyonlar=rezervasyonlar, kullanici_listesi=kullanici_listesi)


@app.route('/admin_logout')
def admin_logout():
    # Oturumu sonlandır
    session.pop('admin_logged_in', None)
    session.pop('admin_username', None)
    return redirect('/admin_login')




# Kullanıcı Ekle
@app.route('/kullanici_ekle', methods=['GET', 'POST'])
def kullanici_ekle():
        # Veritabanı bağlantı bilgilerini ayarlayın
    try:
        connect=pymysql.connect(cursorclass=pymysql.cursors.DictCursor ,charset='utf8mb4' ,host=db_host,user=db_user,password=db_password,db=db_name)  
        print("------------------VERİTABANI BAĞLANTISI BAŞARILI--------------------------")  
    except pymysql.MySQLError as e :
        print("veri tabanı bağlantsııs başarısız",e)
    if request.method == 'POST':
        username = request.form.get('kurs_admin_username').strip()
        password = request.form.get('kurs_admin_password').strip()

        try:
            cursor = connect.cursor()
            cursor.execute("""
            INSERT INTO kurs_admin (kurs_admin_username, kurs_admin_password)
            VALUES (%s, %s)
            """, (username, password))
            connect.commit()
            cursor.close()

            return redirect('/admin_panel')
        except Exception as e:
            print("Hata:", str(e))
            return "<script>alert('Kullanıcı eklerken bir hata oluştu.');</script>"
    else:
        return render_template("kullanici_ekle.html")

# Kullanıcı Sil
@app.route('/kullanici_sil/<string:username>')
def kullanici_sil(username):
        # Veritabanı bağlantı bilgilerini ayarlayın
    try:
        connect=pymysql.connect(cursorclass=pymysql.cursors.DictCursor ,charset='utf8mb4' ,host=db_host,user=db_user,password=db_password,db=db_name)  
        print("------------------VERİTABANI BAĞLANTISI BAŞARILI--------------------------")  
    except pymysql.MySQLError as e :
        print("veri tabanı bağlantsııs başarısız",e)
    try:
        cursor = connect.cursor()
        cursor.execute("DELETE FROM kurs_admin WHERE kurs_admin_username=%s", (username,))
        connect.commit()
        cursor.close()

        return redirect('/admin_panel')
    except Exception as e:
        print("Hata:", str(e))
        return "<script>alert('Kullanıcı silerken bir hata oluştu.');</script>"
# Eski kodlarınızın devamı...
@app.route('/ogrenciler')
def ogrenciler():
    if 'admin_logged_in' not in session or not session['admin_logged_in']:
        return redirect('/admin_login')
        # Veritabanı bağlantı bilgilerini ayarlayın
    try:
        connect=pymysql.connect(cursorclass=pymysql.cursors.DictCursor ,charset='utf8mb4' ,host=db_host,user=db_user,password=db_password,db=db_name)  
        print("------------------VERİTABANI BAĞLANTISI BAŞARILI--------------------------")  
    except pymysql.MySQLError as e :
        print("veri tabanı bağlantsııs başarısız",e)
    cursor = connect.cursor()
    cursor.execute("SELECT * FROM ogrenci")
    ogrenciler = cursor.fetchall()
    cursor.close()
    return render_template("ogrenciler.html", ogrenciler=ogrenciler)
# Eski kodlarınızın devamı...
@app.route('/ogrenci_ekle', methods=['GET', 'POST'])
def ogrenci_ekle():
        # Veritabanı bağlantı bilgilerini ayarlayın
    try:
        connect=pymysql.connect(cursorclass=pymysql.cursors.DictCursor ,charset='utf8mb4' ,host=db_host,user=db_user,password=db_password,db=db_name)  
        print("------------------VERİTABANI BAĞLANTISI BAŞARILI--------------------------")  
    except pymysql.MySQLError as e :
        print("veri tabanı bağlantsııs başarısız",e)
    if request.method == 'POST':
        ogrenci_isim = request.form.get('ogrenci_isim').strip()
        ogrenci_soyisim = request.form.get('ogrenci_soyisim').strip()
        ogrenci_telefon = request.form.get('ogrenci_telefon').strip()
        ogrenci_email = request.form.get('ogrenci_email').strip()

        try:
            cursor = connect.cursor()
            cursor.execute("""
            INSERT INTO ogrenci (ogrenci_isim, ogrenci_soyisim, ogrenci_telefon_no, ogrenci_email)
            VALUES (%s, %s, %s, %s)
            """, (ogrenci_isim, ogrenci_soyisim, ogrenci_telefon, ogrenci_email))

            connect.commit()
            cursor.close()

            return redirect('/ogrenciler')
        except Exception as e:
            print("Hata:", str(e))
            return "<script>alert('Öğrenci eklenirken bir hata oluştu.');</script>"
    else:
        return render_template("ogrenci_ekle.html")
    

@app.route('/profil')
def profil():
            # Veritabanı bağlantı bilgilerini ayarlayın
    try:
        connect=pymysql.connect(cursorclass=pymysql.cursors.DictCursor ,charset='utf8mb4' ,host=db_host,user=db_user,password=db_password,db=db_name)  
        print("------------------VERİTABANI BAĞLANTISI BAŞARILI--------------------------")  
    except pymysql.MySQLError as e :
        print("veri tabanı bağlantsııs başarısız",e)
    if 'ogrenci_id' in session:
        ogrenci_id = session['ogrenci_id']
        try:
            cursor = connect.cursor()
            cursor.execute("""
                SELECT r.rezervasyon_id, r.rezervasyon_tarih, k.kurs_adi, k.kurs_veren_okul, o.ogrenci_isim
                FROM rezervasyonlar r
                INNER JOIN kurslar_ilan k ON r.kurs_ilan_id = k.kurs_ilan_id
                INNER JOIN ogrenci o ON r.ogrenci_id = o.ogrenci_id
                WHERE r.ogrenci_id = %s
            """, (ogrenci_id,))
            rezervasyonlar = cursor.fetchall()
            cursor.close()
            
            return render_template("profil.html", rezervasyonlar=rezervasyonlar)
        except Exception as e:
            print("Hata:", str(e))
            return "<script>alert('Bir hata oluştu.');</script>"
    else:
        return "<script>alert('Lütfen Giriş Yapın' ); window.location.href='/'</script>"



@app.route('/ogrenci_giris', methods=['GET', 'POST'])
def ogrenci_giris():
    # Veritabanı bağlantı bilgilerini ayarlayın
    try:
        connect = pymysql.connect(cursorclass=pymysql.cursors.DictCursor, charset='utf8mb4', host=db_host,
                                  user=db_user, password=db_password, db=db_name)
        print("------------------VERİTABANI BAĞLANTISI BAŞARILI--------------------------")
    except pymysql.MySQLError as e:
        print("veri tabanı bağlantsııs başarısız", e)
    
    if request.method == 'POST':
        ogrenci_soyisim = request.form.get('ogrenci_soyisim').strip()  # Boşlukları temizle
        ogrenci_telefon = request.form.get('ogrenci_telefon').strip()  # Boşlukları temizle

        try:
            cursor = connect.cursor()
            cursor.execute("""
            SELECT * FROM ogrenci WHERE ogrenci_soyisim = %s AND ogrenci_telefon_no = %s
            """, (ogrenci_soyisim, ogrenci_telefon))

            ogrenci = cursor.fetchone()  # İlk kaydı al
            cursor.close()

            if ogrenci:
                print(ogrenci['ogrenci_id'])
                session['ogrenci_id'] = ogrenci['ogrenci_id']
                # Giriş başarılı, öğrenci bilgilerini kullanarak işlemler yapabilirsiniz.
                # Kurslar sayfasına yönlendir
                return redirect('/profil')
            else:
                return "<script>alert('Girş Bilgileriniz yanlış lütfen tekrar kontrol edin'); window.location.href='/' ;</script>"
        except Exception as e:
            print("Hata:", str(e))
            return "<script>alert('Giriş yapılırken bir hata oluştu.'); window.location.href='/' </script>"
    else:
        return render_template("ogrenci_giris.html")


def generate_verification_code():
    return random.randint(1000, 9999)  # 4 haneli rastgele kod oluştur

@app.route('/oturumu_kapat')
def oturumu_kapat():
    session.clear()
    return redirect(url_for('index'))

@app.route('/ogrenci_kayit', methods=['GET', 'POST'])
def ogrenci_kayit():
    if request.method == 'POST':
        randomsayi = generate_verification_code()
    
        ogrenci_isim = request.form.get('ogrenci_isim').strip()
        ogrenci_soyisim = request.form.get('ogrenci_soyisim').strip()
        ogrenci_telefon = request.form.get('ogrenci_telefon').strip()
        ogrenci_email = request.form.get('ogrenci_email').strip()

        try:
            # E-posta alıcısı ve içeriği
            to_email = ogrenci_email
            subject = "doğrulama kodu : " + str(randomsayi)
            message_content = f"Merhaba {ogrenci_isim},\n\n"
            message_content += f"Doğrulama kodunuz : {randomsayi}"

            # E-posta oluşturma
            msg = EmailMessage()
            msg.set_content(message_content)
            msg["Subject"] = subject
            msg["From"] = smtp_username
            msg["To"] = to_email

            # SMTP sunucusuna bağlanma ve e-postayı gönderme
            with smtplib.SMTP_SSL(smtp_server, smtp_port) as server:
                server.login(smtp_username, smtp_password)
                server.send_message(msg)
            print("E-posta başarıyla gönderildi.")

            return render_template("dogrulama.html", ogrenci_email=ogrenci_email, randomsayi=randomsayi, ogrenci_isim=ogrenci_isim, ogrenci_soyisim=ogrenci_soyisim, ogrenci_telefon=ogrenci_telefon)
        except Exception as e:
            print("Hata:", str(e))
            return "<script>alert('Öğrenci eklenirken bir hata oluştu.');</script>"
    else:
        return render_template("ogrenci_kayit.html")

@app.route('/dogrulama', methods=['GET', 'POST'])
def dogrulama():
    try:
        connect = pymysql.connect(cursorclass=pymysql.cursors.DictCursor, charset='utf8mb4', host=db_host, user=db_user, password=db_password, db=db_name)
        print("------------------VERİTABANI BAĞLANTISI BAŞARILI--------------------------")
    except pymysql.MySQLError as e:
        print("veri tabanı bağlantsııs başarısız", e)

    if request.method == 'POST':
        randomsayi = request.form.get('randomsayi')
        girilensayi = request.form.get('verification_code')

        if randomsayi == girilensayi:
            ogrenci_isim = request.form.get('ogrenci_isim').strip()
            ogrenci_soyisim = request.form.get('ogrenci_soyisim').strip()
            ogrenci_telefon = request.form.get('ogrenci_telefon').strip()
            ogrenci_email = request.form.get('ogrenci_email').strip()

            cursor = connect.cursor()

            # Öğrenciyi eklemeden önce mevcut kayıt kontrolü yapalım
            cursor.execute("SELECT * FROM ogrenci WHERE ogrenci_isim = %s AND ogrenci_soyisim = %s AND ogrenci_telefon_no = %s AND ogrenci_email = %s",
                           (ogrenci_isim, ogrenci_soyisim, ogrenci_telefon, ogrenci_email))
            existing_student = cursor.fetchone()

            if existing_student:
                cursor.close()
                return "<script>alert('Bu öğrenci zaten kayıtlı.');window.location.href='/'</script>"

            # Öğrenciyi ekleyelim
            cursor.execute("""
                INSERT INTO ogrenci (ogrenci_isim, ogrenci_soyisim, ogrenci_telefon_no, ogrenci_email)
                VALUES (%s, %s, %s, %s)
            """, (ogrenci_isim, ogrenci_soyisim, ogrenci_telefon, ogrenci_email))

            connect.commit()
            cursor.close()
            return "<script>alert('Kayıt başarılı'); window.location.href='/' </script>"
        else:
            return "<script>alert('Kod hatalı.'); window.location.href='/' </script>"
    else:
        return render_template("dogrulama.html")



@app.route('/ogrenci_duzenle/<int:ogrenci_id>', methods=['GET', 'POST'])
def ogrenci_duzenle(ogrenci_id):
        # Veritabanı bağlantı bilgilerini ayarlayın
    try:
        connect=pymysql.connect(cursorclass=pymysql.cursors.DictCursor ,charset='utf8mb4' ,host=db_host,user=db_user,password=db_password,db=db_name)  
        print("------------------VERİTABANI BAĞLANTISI BAŞARILI--------------------------")  
    except pymysql.MySQLError as e :
        print("veri tabanı bağlantsııs başarısız",e)
    if request.method == 'POST':
        ogrenci_isim = request.form.get('ogrenci_isim').strip()
        ogrenci_soyisim = request.form.get('ogrenci_soyisim').strip()
        ogrenci_telefon = request.form.get('ogrenci_telefon').strip()
        ogrenci_email = request.form.get('ogrenci_email').strip()

        try:
            cursor = connect.cursor()
            cursor.execute("""
            UPDATE ogrenci
            SET ogrenci_isim=%s, ogrenci_soyisim=%s, ogrenci_telefon_no=%s, ogrenci_email=%s
            WHERE ogrenci_id=%s
            """, (ogrenci_isim, ogrenci_soyisim, ogrenci_telefon, ogrenci_email, ogrenci_id))

            connect.commit()
            cursor.close()

            return redirect('/ogrenciler')
        except Exception as e:
            print("Hata:", str(e))
            return "<script>alert('Öğrenci düzenlenirken bir hata oluştu.');</script>"
    else:
        cursor = connect.cursor()
        cursor.execute("SELECT * FROM ogrenci WHERE ogrenci_id=%s", (ogrenci_id,))
        ogrenci = cursor.fetchone()
        cursor.close()
        return render_template("ogrenci_duzenle.html", ogrenci=ogrenci)

@app.route('/ogrenci_sil/<int:ogrenci_id>')
def ogrenci_sil(ogrenci_id):
        # Veritabanı bağlantı bilgilerini ayarlayın
    try:
        connect=pymysql.connect(cursorclass=pymysql.cursors.DictCursor ,charset='utf8mb4' ,host=db_host,user=db_user,password=db_password,db=db_name)  
        print("------------------VERİTABANI BAĞLANTISI BAŞARILI--------------------------")  
    except pymysql.MySQLError as e :
        print("veri tabanı bağlantsııs başarısız",e)
    try:
        cursor = connect.cursor()
        cursor.execute("DELETE FROM ogrenci WHERE ogrenci_id=%s", (ogrenci_id,))

        connect.commit()
        cursor.close()

        return redirect('/ogrenciler')
    except Exception as e:
        print("Hata:", str(e))
        return "<script>alert('Öğrenci silme sırasında bir hata oluştu.');</script>"

# Kullanıcı Düzenle
@app.route('/kullanici_duzenle/<string:username>', methods=['GET', 'POST'])
def kullanici_duzenle(username):
        # Veritabanı bağlantı bilgilerini ayarlayın
    try:
        connect=pymysql.connect(cursorclass=pymysql.cursors.DictCursor ,charset='utf8mb4' ,host=db_host,user=db_user,password=db_password,db=db_name)  
        print("------------------VERİTABANI BAĞLANTISI BAŞARILI--------------------------")  
    except pymysql.MySQLError as e :
        print("veri tabanı bağlantsııs başarısız",e)
    if request.method == 'POST':
        new_username = request.form.get('kurs_admin_username').strip()
        new_password = request.form.get('kurs_admin_password').strip()

        try:
            cursor = connect.cursor()
            cursor.execute("""
            UPDATE kurs_admin
            SET kurs_admin_username=%s, kurs_admin_password=%s
            WHERE kurs_admin_username=%s
            """, (new_username, new_password, username))
            connect.commit()
            cursor.close()

            return redirect('/admin_panel')
        except Exception as e:
            print("Hata:", str(e))
            return "<script>alert('Kullanıcı düzenlerken bir hata oluştu.Öğrencinin  \n Rezervasyonu var ise önce rezervasyonunu silin lütfen            ');</script>"
    else:
        cursor = connect.cursor()
        cursor.execute("SELECT * FROM kurs_admin WHERE kurs_admin_username=%s", (username,))
        kullanici = cursor.fetchone()
        cursor.close()
        return render_template("kullanici_duzenle.html", kullanici=kullanici)

# Kurs ilanı silme
@app.route('/kurs_sil/<int:kurs_ilan_id>')
def kurs_sil(kurs_ilan_id):
        # Veritabanı bağlantı bilgilerini ayarlayın
    try:
        connect=pymysql.connect(cursorclass=pymysql.cursors.DictCursor ,charset='utf8mb4' ,host=db_host,user=db_user,password=db_password,db=db_name)  
        print("------------------VERİTABANI BAĞLANTISI BAŞARILI--------------------------")  
    except pymysql.MySQLError as e :
        print("veri tabanı bağlantsııs başarısız",e)
    try:
        cursor = connect.cursor()

        # İlgili kurs ilanını kontrol et
        cursor.execute("SELECT * FROM kurslar_ilan WHERE kurs_ilan_id=%s", (kurs_ilan_id,))
        ilan = cursor.fetchone()

        if ilan:
            # İlgili rezervasyonları sil
            cursor.execute("DELETE FROM rezervasyonlar WHERE kurs_ilan_id=%s", (kurs_ilan_id,))
            connect.commit()

            # Kurs ilanını sil
            cursor.execute("DELETE FROM kurslar_ilan WHERE kurs_ilan_id=%s", (kurs_ilan_id,))
            connect.commit()

            cursor.close()

            return redirect('/kurslar')
        else:
            return "<script>alert('İlgili kurs ilanı bulunamadı.');</script>"
    except Exception as e:
        print("Hata:", str(e))
        return "<script>alert('Kurs ilanı silme sırasında bir hata oluştu.');</script>"


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

UPLOAD_FOLDER = 'dekontlar'  # Yüklenen dosyanın kaydedileceği klasör
ALLOWED_EXTENSIONS = {'pdf', 'jpg', 'jpeg', 'png'}  # İzin verilen dosya uzantıları
app.config['UPLOAD_FOLDER'] =UPLOAD_FOLDER

@app.route('/odeme/<int:kurs_ilan_id>', methods=['GET', 'POST'])
def odeme(kurs_ilan_id):
    try:
        connect = pymysql.connect(cursorclass=pymysql.cursors.DictCursor, charset='utf8mb4', host=db_host, user=db_user, password=db_password, db=db_name)  
        print("------------------VERİTABANI BAĞLANTISI BAŞARILI--------------------------")  
    except pymysql.MySQLError as e:
        print("veri tabanı bağlantsııs başarısız", e)
    
    if request.method == 'POST':
        ogrenci_bilgileri = request.form['ogrenci_bilgileri']
        dekont = request.files['dekont']
        
        if dekont and allowed_file(dekont.filename):
            # Dosya adını güvenli bir şekilde al
            filename = secure_filename(dekont.filename)
            
            # Dosyanın tam yolunu oluştur
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], f"{ogrenci_bilgileri}_{kurs_ilan_id}_{filename}")
            
            # Dosyayı kaydet
            dekont.save(file_path)
            
            # Veritabanında dosya yolunu kaydetme işlemini burada yapabilirsiniz
            
            return redirect('/kurs_detay/' + str(kurs_ilan_id))
    else:
        return render_template('odeme.html', kurs_ilan_id=kurs_ilan_id)
    
@app.route('/dekontlar')
def dekontlar():
    if 'admin_logged_in' not in session or not session['admin_logged_in']:
        return redirect('/admin_login')

    dekont_listesi = os.listdir(app.config['UPLOAD_FOLDER'])
    return render_template('dekontlar.html', dekontlar=dekont_listesi)

@app.route('/dekont_goster/<filename>')
def dekont_goster(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


# Dekontu indirme
@app.route('/dekont_indir/<filename>')
def dekont_indir(filename):
    return send_file(os.path.join(app.config['UPLOAD_FOLDER'], filename), as_attachment=True)

# Dekontu silme
@app.route('/dekont_sil/<filename>')
def dekont_sil(filename):
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    os.remove(file_path)
    return redirect('/dekontlar')

@app.route('/kurs_detay/<int:kurs_ilan_id>')
def kurs_detay(kurs_ilan_id):
        # Veritabanı bağlantı bilgilerini ayarlayın
    try:
        connect=pymysql.connect(cursorclass=pymysql.cursors.DictCursor ,charset='utf8mb4' ,host=db_host,user=db_user,password=db_password,db=db_name)  
        print("------------------VERİTABANI BAĞLANTISI BAŞARILI--------------------------")  
    except pymysql.MySQLError as e :
        print("veri tabanı bağlantsııs başarısız",e)
    
    cursor = connect.cursor()
    cursor.execute("SELECT * FROM kurslar_ilan WHERE kurs_ilan_id=%s", (kurs_ilan_id,))
    kurs = cursor.fetchone()
    cursor.close()

    return render_template("kurs_detay.html", kurs=kurs)



@app.route('/rezervasyon/<int:kurs_ilan_id>', methods=["GET", "POST"])
def rezervasyon(kurs_ilan_id):
        # Veritabanı bağlantı bilgilerini ayarlayın
    try:
        connect=pymysql.connect(cursorclass=pymysql.cursors.DictCursor ,charset='utf8mb4' ,host=db_host,user=db_user,password=db_password,db=db_name)  
        print("------------------VERİTABANI BAĞLANTISI BAŞARILI--------------------------")  
    except pymysql.MySQLError as e :
        print("veri tabanı bağlantsııs başarısız",e)
    if request.method == 'POST':
        try:
            # Form verilerini al
            ogrenci_isim = request.form.get('ogrenci_isim').strip()
            ogrenci_soyisim = request.form.get('ogrenci_soyisim').strip()
            ogrenci_telefon = request.form.get('ogrenci_telefon').strip()
            ogrenci_email = request.form.get('ogrenci_email').strip()

            cursor = connect.cursor()

            # Öğrencinin ogrenci tablosunda zaten var olup olmadığını kontrol et
            cursor.execute("""
                SELECT ogrenci_id FROM ogrenci
                WHERE ogrenci_isim = %s AND ogrenci_soyisim = %s 
                AND ogrenci_telefon_no = %s AND ogrenci_email = %s
            """, (ogrenci_isim, ogrenci_soyisim, ogrenci_telefon, ogrenci_email))

            existing_student = cursor.fetchone()

            if existing_student:
               ogrenci_id = existing_student['ogrenci_id']
            else:
                # Yeni öğrenciyi ogrenci tablosuna ekle
                cursor.execute("""
                    INSERT INTO ogrenci (ogrenci_isim, ogrenci_soyisim, ogrenci_telefon_no, ogrenci_email)
                    VALUES (%s, %s, %s, %s)
                """, (ogrenci_isim, ogrenci_soyisim, ogrenci_telefon, ogrenci_email))
                ogrenci_id = cursor.lastrowid  # Son eklenen öğrencinin idsini al
                connect.commit()

            # Rezervasyon için gerekli bilgileri al ve rezervasyon yap
            cursor.execute("SELECT * FROM kurslar_ilan WHERE kurs_ilan_id=%s", (kurs_ilan_id,))
            ilan = cursor.fetchone()

            today = date.today()
            rezervasyon_tarih = today.strftime("%Y-%m-%d")

            cursor.execute("""
                INSERT INTO rezervasyonlar (kurs_ilan_id, ogrenci_id, rezervasyon_tarih)
                VALUES (%s, %s, %s)
                """, (kurs_ilan_id, ogrenci_id, rezervasyon_tarih))
            connect.commit()

            # Kurs kontenjanını azalt
            cursor.execute("""
                UPDATE kurslar_ilan
                SET kurs_kontenjan = kurs_kontenjan - 1
                WHERE kurs_ilan_id = %s
                AND kurs_kontenjan > 0
            """, (kurs_ilan_id,))
            connect.commit()

            cursor.close()

                    # E-posta alıcısı ve içeriği
            to_email = ogrenci_email
            subject = "Rezervasyon Onayı"
            message_content = f"Merhaba {ogrenci_isim},\n\n"
            message_content += f"Rezervasyonunuz başarıyla alınmıştır. İşte detaylar:\n\n"
            message_content += f"Kurs Adı: {ilan['kurs_adi']}\n"
            message_content += f"Açıklama: {ilan['kurs_aciklama']}\n"
            message_content += f"Tarih: {rezervasyon_tarih}\n"
            message_content += f"Öğrenci Adı: {ogrenci_isim} {ogrenci_soyisim}\n"
            message_content += f"Telefon: {ogrenci_telefon}\n"
            message_content += f"E-posta: {ogrenci_email}\n\n"
            message_content += "Rezervasyonunuz hakkında herhangi bir sorunuz olduğunda bize ulaşmaktan çekinmeyin.\n"
            message_content += "İyi günler dileriz!"

            # SMTP sunucusuna bağlanma ve e-postayı gönderme
            try:
                with smtplib.SMTP_SSL(smtp_server, smtp_port) as server:
                    server.login(smtp_username, smtp_password)

                    # E-posta oluşturma
                    msg = EmailMessage()
                    msg.set_content(message_content)
                    msg["Subject"] = subject
                    msg["From"] = smtp_username
                    msg["To"] = to_email

                    # E-postayı gönderme
                    server.send_message(msg)

                print("E-posta başarıyla gönderildi.")
            except smtplib.SMTPAuthenticationError:
                print("SMTP kimlik doğrulaması başarısız. Kullanıcı adı veya parola hatalı.")
            except smtplib.SMTPException as e:
                print("SMTP hatası:", str(e))
            except Exception as e:
                print("E-posta gönderilirken bir hata oluştu:", str(e))
            # Başarılı rezervasyon için şablonu döndür
            return render_template("rezervasyon_basarili.html", ogrenci_isim=ogrenci_isim, ogrenci_soyisim=ogrenci_soyisim,
                                   ogrenci_telefon=ogrenci_telefon, ogrenci_email=ogrenci_email,
                                   kurs_adi=ilan['kurs_adi'], aciklama=ilan['kurs_aciklama'])
        except Exception as e:
            print("Hata:", str(e))
            return "<script>alert('Rezervasyon sırasında bir hata oluştu.');</script>"
    else:
        # Sayfayı göster
        return render_template("rezervasyon.html")


# Rezervasyonları listeleme
@app.route('/rezervasyonlar')
def rezervasyonlar():
    if 'admin_logged_in' not in session or not session['admin_logged_in']:
        return redirect('/admin_login')
        # Veritabanı bağlantı bilgilerini ayarlayın
    try:
        connect=pymysql.connect(cursorclass=pymysql.cursors.DictCursor ,charset='utf8mb4' ,host=db_host,user=db_user,password=db_password,db=db_name)  
        print("------------------VERİTABANI BAĞLANTISI BAŞARILI--------------------------")  
    except pymysql.MySQLError as e :
        print("veri tabanı bağlantsııs başarısız",e)
    cursor = connect.cursor()
    cursor.execute("""
        SELECT r.rezervasyon_id, r.rezervasyon_tarih, o.ogrenci_isim, o.ogrenci_soyisim, k.kurs_adi, k.kurs_veren_okul, k.kurs_admin_username, k.kurs_kontenjan
        FROM rezervasyonlar r
        INNER JOIN ogrenci o ON r.ogrenci_id = o.ogrenci_id
        INNER JOIN kurslar_ilan k ON r.kurs_ilan_id = k.kurs_ilan_id
    """)
    rezervasyonlar = cursor.fetchall()
    cursor.close()

    fully_booked_kurslar = [rezervasyon for rezervasyon in rezervasyonlar if rezervasyon.get('kurs_kontenjan',0) <= 0]
    available_kurslar = [rezervasyon for rezervasyon in rezervasyonlar if rezervasyon.get('kurs_kontenjan',0) > 0]

    return render_template("rezervasyonlar.html", fully_booked_kurslar=fully_booked_kurslar, available_kurslar=available_kurslar)


@app.route('/rezervasyon_sil/<int:rezervasyon_id>')
def rezervasyon_sil(rezervasyon_id):
        # Veritabanı bağlantı bilgilerini ayarlayın
    try:
        connect=pymysql.connect(cursorclass=pymysql.cursors.DictCursor ,charset='utf8mb4' ,host=db_host,user=db_user,password=db_password,db=db_name)  
        print("------------------VERİTABANI BAĞLANTISI BAŞARILI--------------------------")  
    except pymysql.MySQLError as e :
        print("veri tabanı bağlantsııs başarısız",e)
    try:
        cursor = connect.cursor()
        
        # Rezervasyon bilgilerini al
        cursor.execute("SELECT kurs_ilan_id FROM rezervasyonlar WHERE rezervasyon_id=%s", (rezervasyon_id,))
        rezervasyon = cursor.fetchone()
        kurs_ilan_id = rezervasyon['kurs_ilan_id']
        
        # Rezervasyonu sil
        cursor.execute("DELETE FROM rezervasyonlar WHERE rezervasyon_id=%s", (rezervasyon_id,))
        
        # Kurs kontenjanını güncelle
        cursor.execute("""
            UPDATE kurslar_ilan
            SET kurs_kontenjan = kurs_kontenjan + 1
            WHERE kurs_ilan_id = %s
        """, (kurs_ilan_id,))
        
        connect.commit()
        cursor.close()

        return redirect('/rezervasyonlar')
    except Exception as e:
        print("Hata:", str(e))
        return "<script>alert('Rezervasyon silme sırasında bir hata oluştu.');</script>"
    


@app.route('/ogrenci_rezervasyon_sil/<int:rezervasyon_id>', methods=['GET', 'POST'])
def ogrenci_rezervasyon_sil(rezervasyon_id):
    try:
        connect = pymysql.connect(cursorclass=pymysql.cursors.DictCursor, charset='utf8mb4', host=db_host, user=db_user, password=db_password, db=db_name)
        print("------------------VERİTABANI BAĞLANTISI BAŞARILI--------------------------")
    except pymysql.MySQLError as e:
        print("veri tabanı bağlantsııs başarısız", e)
    try:
        cursor = connect.cursor()

        # Rezervasyon bilgilerini al
        cursor.execute("SELECT rezervasyonlar.ogrenci_id, ogrenci.ogrenci_isim, ogrenci.ogrenci_soyisim, ogrenci.ogrenci_telefon_no, kurslar_ilan.kurs_adi, kurslar_ilan.kurs_veren_okul, kurslar_ilan.kurs_admin_username FROM rezervasyonlar INNER JOIN ogrenci ON rezervasyonlar.ogrenci_id = ogrenci.ogrenci_id INNER JOIN kurslar_ilan ON rezervasyonlar.kurs_ilan_id = kurslar_ilan.kurs_ilan_id WHERE rezervasyonlar.rezervasyon_id=%s", (rezervasyon_id,))
        rezervasyon = cursor.fetchone()

        if rezervasyon:
            ogrenci_isim = rezervasyon['ogrenci_isim']
            ogrenci_soyisim = rezervasyon['ogrenci_soyisim']
            ogrenci_telefon = rezervasyon['ogrenci_telefon_no']
            kurs_admin_username = rezervasyon['kurs_admin_username']
            kurs_adi = rezervasyon['kurs_adi']
            kurs_veren_okul = rezervasyon['kurs_veren_okul']

            # Rezervasyonu sil
            cursor.execute("DELETE FROM rezervasyonlar WHERE rezervasyon_id=%s", (rezervasyon_id,))

            # Kurs kontenjanını güncelle
            cursor.execute("""
                UPDATE kurslar_ilan
                SET kurs_kontenjan = kurs_kontenjan + 1
                WHERE kurs_adi = %s
            """, (kurs_adi,))

            connect.commit()
            cursor.close()
            try:
                with smtplib.SMTP_SSL(smtp_server, smtp_port) as server:
                    server.login(smtp_username, smtp_password)
                    to_email = kurs_admin_username
                    subject = "Rezervasyon Silindi"
                    
                    # E-posta içeriği oluşturma
                    message_content = f"""
                        Rezervasyon silindi:
                        
                        Öğrenci Adı: {ogrenci_isim}
                        Öğrenci Soyadı: {ogrenci_soyisim}
                        Öğrenci Telefon: {ogrenci_telefon}
                        Kurs Adı: {kurs_adi}
                        Kurs Veren Okul: {kurs_veren_okul}
                        Rezervasyon ID: {rezervasyon_id}
                        
                        """
                    
                    # E-postayı oluşturma
                    msg = EmailMessage()
                    msg.set_content(message_content)
                    msg["Subject"] = subject
                    msg["From"] = smtp_username
                    msg["To"] = to_email

                    # E-postayı gönderme
                    server.send_message(msg)

                print("E-posta başarıyla gönderildi.")
            except smtplib.SMTPAuthenticationError:
                print("SMTP kimlik doğrulaması başarısız. Kullanıcı adı veya parola hatalı.")
            except smtplib.SMTPException as e:
                print("SMTP hatası:", str(e))
            except Exception as e:
                print("E-posta gönderilirken bir hata oluştu:", str(e))
            return redirect('/profil')
        else:
            return "<script>alert('Belirtilen rezervasyon bulunamadı.');</script>"

    except Exception as e:
        print("Hata:", str(e))
        return "<script>alert('Rezervasyon silme sırasında bir hata oluştu.');</script>"



@app.route('/rezervasyon_duzenle/<int:rezervasyon_id>', methods=['GET', 'POST'])
def rezervasyon_duzenle(rezervasyon_id):
        # Veritabanı bağlantı bilgilerini ayarlayın
    try:
        connect=pymysql.connect(cursorclass=pymysql.cursors.DictCursor ,charset='utf8mb4' ,host=db_host,user=db_user,password=db_password,db=db_name)  
        print("------------------VERİTABANI BAĞLANTISI BAŞARILI--------------------------")  
    except pymysql.MySQLError as e :
        print("veri tabanı bağlantsııs başarısız",e)
    if request.method == 'POST':
        # Retrieve form data
        ogrenci_isim = request.form.get('ogrenci_isim').strip()
        ogrenci_soyisim = request.form.get('ogrenci_soyisim').strip()
        kurs_adi = request.form.get('kurs_adi').strip()
        rezervasyon_tarih = request.form.get('rezervasyon_tarih').strip()

        # Perform database updates
        cursor = connect.cursor()

        # Update 'ogrenci' table
        cursor.execute("""
            UPDATE ogrenci
            SET ogrenci_isim=%s, ogrenci_soyisim=%s
            WHERE ogrenci_id IN (
                SELECT ogrenci_id
                FROM rezervasyonlar
                WHERE rezervasyon_id=%s
            )
        """, (ogrenci_isim, ogrenci_soyisim, rezervasyon_id))

        # Update 'kurslar_ilan' table
        cursor.execute("""
            UPDATE kurslar_ilan
            SET kurs_adi=%s
            WHERE kurs_ilan_id IN (
                SELECT kurs_ilan_id
                FROM rezervasyonlar
                WHERE rezervasyon_id=%s
            )
        """, (kurs_adi, rezervasyon_id))

        connect.commit()
        cursor.close()

        return redirect('/rezervasyonlar')


    else:
        cursor = connect.cursor()
        cursor.execute("""
            SELECT r.rezervasyon_id, r.rezervasyon_tarih, o.ogrenci_isim, o.ogrenci_soyisim, k.kurs_adi
            FROM rezervasyonlar r
            INNER JOIN ogrenci o ON r.ogrenci_id = o.ogrenci_id
            INNER JOIN kurslar_ilan k ON r.kurs_ilan_id = k.kurs_ilan_id
            WHERE r.rezervasyon_id=%s
        """, (rezervasyon_id,))
        rezervasyon = cursor.fetchone()
        cursor.close()
        return render_template("rezervasyon_duzenle.html", rezervasyon=rezervasyon)
@app.route('/kullanicilar')
def kullanicilar():

    if 'admin_logged_in' not in session or not session['admin_logged_in']:
        return redirect('/admin_login')
        # Veritabanı bağlantı bilgilerini ayarlayın
    try:
        connect=pymysql.connect(cursorclass=pymysql.cursors.DictCursor ,charset='utf8mb4' ,host=db_host,user=db_user,password=db_password,db=db_name)  
        print("------------------VERİTABANI BAĞLANTISI BAŞARILI--------------------------")  
    except pymysql.MySQLError as e :
        print("veri tabanı bağlantsııs başarısız",e)
    cursor = connect.cursor()
    cursor.execute("SELECT * FROM kurs_admin")
    kullanici_listesi = cursor.fetchall()
    cursor.close()
    return render_template("kullanicilar.html", kullanici_listesi=kullanici_listesi)


@app.route('/kullanici_giris', methods=['GET', 'POST'])
def kullanici_giris():
        # Veritabanı bağlantı bilgilerini ayarlayın
    try:
        connect=pymysql.connect(cursorclass=pymysql.cursors.DictCursor ,charset='utf8mb4' ,host=db_host,user=db_user,password=db_password,db=db_name)  
        print("------------------VERİTABANI BAĞLANTISI BAŞARILI--------------------------")  
    except pymysql.MySQLError as e :
        print("veri tabanı bağlantsııs başarısız",e)
    if request.method == 'POST':
        username = request.form.get('username').strip()
        password = request.form.get('password').strip()

        # Kullanıcı adı ve şifreyi kontrol et
        cursor = connect.cursor()
        cursor.execute("SELECT * FROM kurs_admin WHERE kurs_admin_username = %s AND kurs_admin_password = %s", (username, password))
        kullanici = cursor.fetchone()

        if kullanici:
            # Oturumu başlat
            session['kullanici_logged_in'] = True
            session['kullanici_username'] = username
            
            # Kullanıcının ilanlarını getir
            cursor = connect.cursor()
            cursor.execute("SELECT * FROM kurslar_ilan WHERE kurs_admin_username = %s", (username,))
            ilanlar = cursor.fetchall()

            # Kullanıcının rezervasyonlarını getir
            cursor.execute("""
                SELECT o.ogrenci_isim, o.ogrenci_soyisim, k.kurs_adi, k.kurs_aciklama, r.rezervasyon_tarih
                FROM rezervasyonlar r
                INNER JOIN ogrenci o ON r.ogrenci_id = o.ogrenci_id
                INNER JOIN kurslar_ilan k ON r.kurs_ilan_id = k.kurs_ilan_id
                WHERE k.kurs_admin_username = %s
            """, (username))

            rezervasyonlar = cursor.fetchall()
            cursor.close()

            return render_template('/kullanici_panel.html', username=username, ilanlar=ilanlar, rezervasyonlar=rezervasyonlar)
        else:
            return "<script>alert('Geçersiz kullanıcı adı veya şifre.'); window.location.href='/' </script>"
    else:
        return render_template('kullanici_giris.html')


@app.route('/kullanici_panel')
def kullanici_panel():
        # Veritabanı bağlantı bilgilerini ayarlayın
    try:
        connect=pymysql.connect(cursorclass=pymysql.cursors.DictCursor ,charset='utf8mb4' ,host=db_host,user=db_user,password=db_password,db=db_name)  
        print("------------------VERİTABANI BAĞLANTISI BAŞARILI--------------------------")  
    except pymysql.MySQLError as e :
        print("veri tabanı bağlantsııs başarısız",e)
    # Oturum verilerini kontrol et
    if 'kullanici_logged_in' not in session or not session['kullanici_logged_in']:
        return redirect('/kullanici_giris')

    return render_template('kullanici_panel.html', username=session['kullanici_username'])



@app.route('/kullanici_cikis')
def kullanici_cikis():
        # Veritabanı bağlantı bilgilerini ayarlayın
    try:
        connect=pymysql.connect(cursorclass=pymysql.cursors.DictCursor ,charset='utf8mb4' ,host=db_host,user=db_user,password=db_password,db=db_name)  
        print("------------------VERİTABANI BAĞLANTISI BAŞARILI--------------------------")  
    except pymysql.MySQLError as e :
        print("veri tabanı bağlantsııs başarısız",e)
    # Oturumu sonlandır
    session.pop('kullanici_logged_in', None)
    session.pop('kullanici_username', None)
    
    return redirect(url_for('kullanici_giris'))


@app.route('/ders_ekle', methods=['GET', 'POST'])
def ders_ekle():
        # Veritabanı bağlantı bilgilerini ayarlayın
    try:
        connect=pymysql.connect(cursorclass=pymysql.cursors.DictCursor ,charset='utf8mb4' ,host=db_host,user=db_user,password=db_password,db=db_name)  
        print("------------------VERİTABANI BAĞLANTISI BAŞARILI--------------------------")  
    except pymysql.MySQLError as e :
        print("veri tabanı bağlantsııs başarısız",e)
    if request.method == 'POST':
        # Form verilerini al
        kurs_adi = request.form.get('kurs_adi').strip()
        kurs_aciklama = request.form.get('kurs_aciklama').strip()

        try:
            cursor = connect.cursor()
            cursor.execute("""
            INSERT INTO kurs (kurs_adi, kurs_aciklama)
            VALUES (%s, %s)
            """, (kurs_adi, kurs_aciklama))

            connect.commit()
            cursor.close()

            return redirect('/admin_panel')
        except Exception as e:
            print("Hata:", str(e))
            return "<script>alert('Ders eklenirken bir hata oluştu.');</script>"
    else:
        return render_template("ders_ekle.html")
# Ders düzenleme
@app.route('/ders_duzenle/<int:kurs_id>', methods=['GET', 'POST'])
def ders_duzenle(kurs_id):
        # Veritabanı bağlantı bilgilerini ayarlayın
    try:
        connect=pymysql.connect(cursorclass=pymysql.cursors.DictCursor ,charset='utf8mb4' ,host=db_host,user=db_user,password=db_password,db=db_name)  
        print("------------------VERİTABANI BAĞLANTISI BAŞARILI--------------------------")  
    except pymysql.MySQLError as e :
        print("veri tabanı bağlantsııs başarısız",e)
    if request.method == 'POST':
        kurs_adi = request.form.get('kurs_adi').strip()
        kurs_aciklama = request.form.get('kurs_aciklama').strip()

        try:
            cursor = connect.cursor()
            cursor.execute("""
            UPDATE kurs
            SET kurs_adi=%s, kurs_aciklama=%s
            WHERE kurs_id=%s
            """, (kurs_adi, kurs_aciklama, kurs_id))

            connect.commit()
            cursor.close()

            return redirect('/dersler')
        except Exception as e:
            print("Hata:", str(e))
            return "<script>alert('Ders düzenlenirken bir hata oluştu.');</script>"
    else:
        cursor = connect.cursor()
        cursor.execute("SELECT * FROM kurs WHERE kurs_id=%s", (kurs_id,))
        ders = cursor.fetchone()
        cursor.close()
        return render_template("ders_duzenle.html", ders=ders)

# Ders silme
@app.route('/ders_sil/<int:kurs_id>')
def ders_sil(kurs_id):
        # Veritabanı bağlantı bilgilerini ayarlayın
    try:
        connect=pymysql.connect(cursorclass=pymysql.cursors.DictCursor ,charset='utf8mb4' ,host=db_host,user=db_user,password=db_password,db=db_name)  
        print("------------------VERİTABANI BAĞLANTISI BAŞARILI--------------------------")  
    except pymysql.MySQLError as e :
        print("veri tabanı bağlantsııs başarısız",e)
    try:
        cursor = connect.cursor()
        cursor.execute("DELETE FROM kurs WHERE kurs_id=%s", (kurs_id,))

        connect.commit()
        cursor.close()

        return redirect('/dersler')
    except Exception as e:
        print("Hata:", str(e))
        return "<script>alert('Ders silme sırasında bir hata oluştu.');</script>"
# Dersleri listeleme
@app.route('/dersler')
def dersler():
    if 'admin_logged_in' not in session or not session['admin_logged_in']:
        return redirect('/admin_login')
        # Veritabanı bağlantı bilgilerini ayarlayın
    try:
        connect=pymysql.connect(cursorclass=pymysql.cursors.DictCursor ,charset='utf8mb4' ,host=db_host,user=db_user,password=db_password,db=db_name)  
        print("------------------VERİTABANI BAĞLANTISI BAŞARILI--------------------------")  
    except pymysql.MySQLError as e :
        print("veri tabanı bağlantsııs başarısız",e)
    cursor = connect.cursor()
    cursor.execute("SELECT * FROM kurs")
    dersler = cursor.fetchall()
    cursor.close()
    return render_template("dersler.html", dersler=dersler)

if __name__ == '__main__':
    app.run(debug=True, port=80, host='0.0.0.0')
