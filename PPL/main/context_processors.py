from .models import Pengguna

def user_context(request):
    """
    Membuat objek Pengguna yang sedang login tersedia di semua template 
    dengan nama 'logged_in_user'.
    """
    user_id = request.session.get("user_id")
    user = None
    
    if user_id:
        try:
            # Ambil objek Pengguna
            user = Pengguna.objects.get(id_pengguna=user_id)
        except Pengguna.DoesNotExist:
            # Jika user terhapus tapi session masih ada
            pass 
            
    return {
        'logged_in_user': user # Variabel yang akan digunakan di header.html
    }