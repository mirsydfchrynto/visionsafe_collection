import os
import json
import hashlib
import feedparser
import requests
from bs4 import BeautifulSoup
import firebase_admin
from firebase_admin import credentials, firestore
from datetime import datetime
import time

# ==============================================================================
# VISIONSAFE ABSOLUTE KNOWLEDGE ENGINE (SDA ELITE V7.0 - GITHUB EDITION)
# ==============================================================================

class VisionSafeEliteIngestor:
    def __init__(self):
        self.db = self._init_firebase()
        self.collection_name = "visionsafe_knowledge"
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
        # Smart Filter Keywords
        self.eye_keywords = [
            'eye', 'vision', 'blindness', 'myopia', 'glaucoma', 'retina', 'sight', 'screen time', 
            'mata', 'penglihatan', 'rabun', 'miopia', 'katarak', 'gadget', 'kacamata', 'ophthalmology'
        ]

    def _init_firebase(self):
        """Initializes Firebase from environment variable."""
        firebase_config_raw = os.environ.get("FIREBASE_CONFIG")
        if not firebase_config_raw:
            raise ValueError("Environment variable FIREBASE_CONFIG is missing.")
        
        try:
            config_dict = json.loads(firebase_config_raw)
            if not firebase_admin._apps:
                cred = credentials.Certificate(config_dict)
                firebase_admin.initialize_app(cred)
            return firestore.client()
        except Exception as e:
            print(f"Error initializing Firebase: {e}")
            raise

    def generate_id(self, url):
        """Generates a SHA-256 hash for global deduplication."""
        return hashlib.sha256(url.encode('utf-8')).hexdigest()

    def is_eye_related(self, text):
        """Smart filter to ensure relevance to eye health."""
        if not text: return False
        text_lower = text.lower()
        return any(keyword in text_lower for keyword in self.eye_keywords)

    def extract_full_content(self, url):
        """Surgical Extraction of main article text with noise removal."""
        try:
            response = requests.get(url, headers=self.headers, timeout=15)
            soup = BeautifulSoup(response.text, 'lxml')
            
            # Remove noise
            for element in soup(["script", "style", "nav", "header", "footer", "aside", "form", "iframe"]):
                element.decompose()

            paragraphs = soup.find_all('p')
            content = " ".join([p.get_text() for p in paragraphs])
            content = " ".join(content.split()) # Normalize whitespace
            
            # Minimum threshold for quality content
            return content if len(content) > 300 else None
        except Exception as e:
            print(f"Extraction failed for {url}: {e}")
            return None

    def get_data_sources(self):
        """Centralized Authority Source Management."""
        return {
            "NIH National Eye Institute": {"url": "https://www.nei.nih.gov/about/news-and-events/news/feed", "type": "rss", "filter": False},
            "WHO Global News": {"url": "https://www.who.int/rss-feeds/news-english.xml", "type": "rss", "filter": True},
            "Medical News Today (Eye)": {"url": "https://www.medicalnewstoday.com/rss/eye-health", "type": "rss", "filter": False},
            "Science Daily (Eye Care)": {"url": "https://www.sciencedaily.com/rss/health_medicine/eye_care.xml", "type": "rss", "filter": False},
            "News Medical (Eye Health)": {"url": "https://www.news-medical.net/tag/feed/Eye-Health.aspx", "type": "rss", "filter": False},
            "Kemenkes RI (Sehat Negeriku)": {"url": "https://sehatnegeriku.kemkes.go.id/feed/", "type": "rss", "filter": True},
            "Google News (Eye Health ID)": {"url": "https://news.google.com/rss/search?q=kesehatan+mata+miopia+katarak&hl=id&gl=ID&ceid=ID:id", "type": "rss", "filter": False}
        }

    def run(self):
        """Main execution flow for GitHub Actions with enhanced logging."""
        print(f"--- VisionSafe Data Ingestion Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} ---")
        sources = self.get_data_sources()
        
        stats = {
            "total_scanned": 0,
            "total_new": 0,
            "total_skipped": 0,
            "errors": 0
        }
        
        for name, config in sources.items():
            print(f"\n[Source] {name}")
            try:
                if config["type"] == "rss":
                    feed = feedparser.parse(config["url"])
                    entries = feed.entries[:30] # Limit per source
                    
                    for entry in entries:
                        stats["total_scanned"] += 1
                        url = entry.link
                        title = entry.title
                        
                        if config["filter"]:
                            combined_text = title + " " + (entry.summary if hasattr(entry, 'summary') else "")
                            if not self.is_eye_related(combined_text):
                                stats["total_skipped"] += 1
                                continue
                        
                        doc_id = self.generate_id(url)
                        doc_ref = self.db.collection(self.collection_name).document(doc_id)
                        
                        if not doc_ref.get().exists:
                            content = self.extract_full_content(url)
                            if content:
                                payload = {
                                    "title": title,
                                    "url": url,
                                    "full_content": content,
                                    "source": name,
                                    "category": "Authoritative Intelligence",
                                    "published_raw": entry.get("published", datetime.now().strftime("%Y-%m-%d")),
                                    "collected_at": firestore.SERVER_TIMESTAMP,
                                    "content_length": len(content),
                                    "fingerprint": doc_id
                                }
                                doc_ref.set(payload)
                                stats["total_new"] += 1
                                print(f"  [NEW] {title}")
                                time.sleep(1) # Polite delay
                        else:
                            stats["total_skipped"] += 1
                            
            except Exception as e:
                print(f"  [ERROR] {name}: {e}")
                stats["errors"] += 1
                continue

        print("\n--- Ingestion Summary ---")
        print(f"Total Scanned : {stats['total_scanned']}")
        print(f"Total New     : {stats['total_new']}")
        print(f"Total Skipped : {stats['total_skipped']}")
        print(f"Errors Found  : {stats['errors']}")
        print(f"Finished at   : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

if __name__ == "__main__":
    ingestor = VisionSafeEliteIngestor()
    ingestor.run()
