from supabase import create_client, Client
import os
from dotenv import load_dotenv

load_dotenv()

class SupabaseClient:
    """
    Patrón Singleton: Una sola instancia del cliente Supabase
    """
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.client = create_client(
                os.getenv("SUPABASE_URL"),
                os.getenv("SUPABASE_KEY")
            )
        return cls._instance
    
    def get_client(self) -> Client:
        return self.client

# Función de conveniencia
def get_db():
    return SupabaseClient().get_client()