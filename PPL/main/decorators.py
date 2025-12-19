from django.shortcuts import redirect
from functools import wraps

def butuh_login_siswa(func):
    """
    Decorator untuk memastikan pengguna sudah login.
    Jika belum login (tidak ada session 'id_pengguna'), akan diarahkan ke halaman login.
    """
    @wraps(func)
    def wrapper(request, *args, **kwargs):
        # Cek apakah session id_pengguna ada?
        if 'id_pengguna' not in request.session:
            return redirect('login_siswa') # Sesuaikan dengan nama URL login Anda (misal: 'login' atau 'login_siswa')
        return func(request, *args, **kwargs)
    return wrapper