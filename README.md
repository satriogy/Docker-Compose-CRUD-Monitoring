# Docker-Compose-CRUD-Monitoring

ini berisikan 
1. Frontend: Menggunakan Nginx untuk melayani halaman statis.
2. Backend: flask  
3. Database: PostgreSQL untuk menyimpan data aplikasi.
4. Networking: Backend dan database harus saling terhubung dengan jaringan privat.
5. Volume: Database PostgreSQL memerlukan penyimpanan data yang persisten.
6. Monitoring : Grafana

langkah running:
docker-compose up --build -d

langkah matikan:
docker-compose down
