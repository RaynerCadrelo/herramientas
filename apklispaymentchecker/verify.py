# coding=UTF-8
from jnius import autoclass


#Retorna 	[None, False] si no se pudo sestionar la petición
#			["Nombre_del_usuario", False] si el usuario autentificado no ha comprado la apk
#			["Nombre_del_usuario", True] si el usuario autentificado lo ha comprado.

class Verify():
	def isPurchased(self, packageId):
		APKLIS_PROVIDER = "content://cu.uci.android.apklis.payment.provider/app/"
		APKLIS_USER_NAME = "user_name"
		APKLIS_PAID = "paid"		
		paid = False
		userName = None
		try:
			Context = autoclass("android.content.Context") 
			BuildAndroid = autoclass("android.os.Build")
			androidVersion = autoclass('android.os.Build$VERSION')
			Uri = autoclass("android.net.Uri")
			
			providerURI = Uri.parse(APKLIS_PROVIDER + packageId)
			contentResolver = Context.getContentResolver().acquireContentProviderClient(providerURI)
			cursor = contentResolver.query(providerURI,None,None,None,None)
			if cursor.moveToFirst():			
				paid = cursor.getInt(cursor.getColumnIndex(APKLIS_PAID)) > 0
				userName = cursor.getString(cursor.getColumnIndex(APKLIS_USER_NAME))
				
			if androidVersion.SDK_INT >= 26:
				contentResolver.close()
			else:
				contentResolver.release()
			cursor.close()		
		except:
			pass #self.root.ids["label"].text = str(sys.exc_info()[0]) + "\n " + str(sys.exc_info()[1])
			
		return [userName, paid]
