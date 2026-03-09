# 📝 Exemples d'Utilisation - Network Scanner

## 🎯 Scénarios Pratiques

### 1. Scan Rapide d'un Serveur Web
**Objectif** : Vérifier les ports web standards (80, 443)

```bash
python3 scanner.py -t 192.168.1.100 -p 80,443
```

**Résultat attendu** : Détection des services HTTP et HTTPS

---

### 2. Audit Réseau Local
**Objectif** : Découvrir tous les appareils sur votre réseau local

```bash
python3 scanner.py -t 192.168.1.0/24 -p 22,80,443,3389
```

**Utilisation** : 
- Inventaire des machines sur le réseau
- Détection d'appareils inconnus
- Vérification de la segmentation réseau

---

### 3. Scan Complet d'un Serveur
**Objectif** : Scanner les 1000 premiers ports (les plus communs)

```bash
python3 scanner.py -t mon-serveur.com -p 1-1000 --timeout 2 --threads 100
```

**Note** : Plus rapide mais peut être détecté par les IDS/IPS

---

### 4. Scan de Services Critiques
**Objectif** : Vérifier uniquement les services sensibles

```bash
python3 scanner.py -t 10.0.0.50 -p 21,22,23,25,445,3306,3389,5432,8080
```

**Services vérifiés** :
- FTP (21)
- SSH (22)
- Telnet (23)
- SMTP (25)
- SMB (445)
- MySQL (3306)
- RDP (3389)
- PostgreSQL (5432)
- HTTP-alt (8080)

---

### 5. Scan d'un Réseau Distant avec Rapport Personnalisé
**Objectif** : Scanner et générer un rapport nommé

```bash
python3 scanner.py -t 203.0.113.0/28 -p 80,443,22 -o audit_externe_2026
```

**Fichiers générés** :
- `audit_externe_2026.txt`
- `audit_externe_2026.json`

---

## 🔍 Cas d'Usage Réels

### Pentest - Phase de Reconnaissance
```bash
# Découvrir les hôtes actifs
python3 scanner.py -t 192.168.10.0/24 -p 80,443

# Scan approfondi des hôtes découverts
python3 scanner.py -t 192.168.10.50,192.168.10.51,192.168.10.52 -p 1-65535 --timeout 3
```

### Audit de Conformité
```bash
# Vérifier que seuls les ports autorisés sont ouverts
python3 scanner.py -t serveur-prod.entreprise.local -p 22,80,443 -o conformite_janvier
```

### Troubleshooting Réseau
```bash
# Vérifier si un service est accessible
python3 scanner.py -t app-server.local -p 8080,8443,9000
```

---

## ⚠️ AVERTISSEMENT

**Ces exemples sont fournis à des fins éducatives uniquement.**

### ✅ Utilisation Autorisée
- Votre propre infrastructure
- Environnements de lab/test
- Avec permission écrite de l'administrateur réseau
- Plateformes d'entraînement (TryHackMe, HackTheBox, etc.)

### ❌ Utilisation Interdite
- Réseaux tiers sans autorisation
- Infrastructure d'entreprise sans permission
- Réseaux publics
- Toute activité malveillante

**Scanner un réseau sans autorisation est illégal et peut entraîner des poursuites judiciaires.**

---

## 📊 Interpréter les Résultats

### Ports Ouverts Communs

| Port | Service | Sécurité |
|------|---------|----------|
| 21 | FTP | ⚠️ Non chiffré |
| 22 | SSH | ✅ Sécurisé si configuré |
| 23 | Telnet | ❌ Non sécurisé |
| 25 | SMTP | ⚠️ Vérifier config |
| 80 | HTTP | ⚠️ Non chiffré |
| 443 | HTTPS | ✅ Chiffré |
| 3306 | MySQL | ⚠️ Ne devrait pas être exposé |
| 3389 | RDP | ⚠️ Cible fréquente d'attaques |
| 8080 | HTTP-alt | ⚠️ Vérifier |

### Red Flags 🚩
- Port 23 (Telnet) ouvert = Protocole non sécurisé
- Port 3306 (MySQL) exposé = Base de données accessible
- Nombreux ports ouverts = Surface d'attaque importante
- Services inconnus = Potentiellement vulnérables

---

## 🎓 Exercices Pratiques

### Débutant
1. Scanner votre propre machine (127.0.0.1)
2. Scanner votre routeur local (généralement 192.168.1.1)
3. Comparer les résultats entre différents timeouts

### Intermédiaire
1. Scanner un réseau /24 complet
2. Générer des rapports et analyser les données JSON
3. Identifier les services par leurs ports

### Avancé
1. Scanner avec différents niveaux de threading
2. Automatiser l'analyse des résultats JSON
3. Créer un script qui scanne régulièrement et alerte sur les changements

---

## 💡 Astuces

### Optimiser la Vitesse
```bash
# Scan très rapide (peut être moins précis)
python3 scanner.py -t 192.168.1.1 -p 1-1000 --timeout 0.5 --threads 200
```

### Scan Discret
```bash
# Scan lent et discret (moins détectable)
python3 scanner.py -t cible.com -p 80,443 --timeout 5 --threads 5
```

### Scanner Plusieurs Cibles
```bash
# Virgule pour séparer
python3 scanner.py -t 192.168.1.1,192.168.1.2,192.168.1.3 -p 80,443
```

---

**Bon scanning ! 🚀**

*Utilisez cet outil de manière responsable et éthique.*
