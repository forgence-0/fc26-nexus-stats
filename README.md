# FC26 Custom EA Trax's — Nexus Skorbordu

`FC26 Custom EA Trax's` modunun Nexus Mods sayfasındaki **Unique DLs /
Total DLs / Total views** rakamlarını otomatik çekip GitHub Pages
üzerinde gösteren küçük bir panel.

Önemli: bu rakamlar gerçekte saniyede bir değişmiyor. Sayfa kendini
her 10 saniyede bir yeniler ama arkadaki veri, GitHub Actions'ın
çalıştığı sıklıkta (varsayılan 15 dakika) güncellenir. "Son
güncelleme" yazısı bunu gösterir.

## Nasıl çalışıyor

1. `.github/workflows/update-stats.yml` — GitHub Actions ile periyodik
   olarak `scraper.py`'yi çalıştırır.
2. `scraper.py` — Playwright (gerçek bir tarayıcı motoru) ile Nexus
   sayfasını açar, JS ile dolan rakamları okur, `stats.json`'a yazar
   ve commit'ler.
3. `index.html` — GitHub Pages üzerinde yayınlanan statik sayfa.
   `stats.json`'ı okuyup skorbord şeklinde gösterir.

## Kurulum

1. GitHub'da yeni bir repo oluştur (örn. `fc26-nexus-stats`).
2. Bu klasördeki tüm dosyaları (gizli `.github` klasörü dahil) repoya
   push'la:
   ```
   git init
   git add .
   git commit -m "ilk kurulum"
   git branch -M main
   git remote add origin https://github.com/KULLANICI_ADIN/fc26-nexus-stats.git
   git push -u origin main
   ```
3. Repo sayfasında **Settings → Pages** açıp:
   - Source: "Deploy from a branch"
   - Branch: `main` / `(root)`
   seç ve kaydet.
4. **Settings → Actions → General → Workflow permissions** altından
   "Read and write permissions" seçili olduğundan emin ol (workflow'un
   `stats.json`'ı commit'leyebilmesi için gerekli).
5. **Actions** sekmesine git, "Nexus stats güncelle" workflow'unu seç
   ve **Run workflow** ile bir kez elle tetikle — böylece `stats.json`
   hemen ilk gerçek verilerle dolar.
6. Birkaç dakika içinde sayfan şurada yayında olur:
   `https://KULLANICI_ADIN.github.io/fc26-nexus-stats/`

## Ayarlar

- Yenileme sıklığı: `.github/workflows/update-stats.yml` içindeki
  `cron: "*/15 * * * *"` satırını değiştir (GitHub'ın pratik minimumu
  ~5 dakikadır, daha sık ayarlarsan gecikmeler/atlamalar olabilir).
- Başka bir modu izlemek istersen `scraper.py` içindeki `MOD_URL`
  değerini değiştir.
