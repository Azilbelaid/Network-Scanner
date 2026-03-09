# 🔍 Network Scanner - Outil d'Analyse Réseau et Sécurité

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)
![Status](https://img.shields.io/badge/Status-Active-success.svg)

## 📋 Description

**Network Scanner** est un outil d'analyse réseau développé en Python permettant de :
- 🔍 Découvrir les hôtes actifs sur un réseau
- 🔓 Scanner les ports ouverts sur des cibles spécifiques
- 🏷️ Identifier les services en écoute
- 📊 Générer des rapports détaillés (TXT et JSON)

Développé dans le cadre de ma formation en cybersécurité pour démontrer mes compétences en programmation système, réseaux et sécurité.

---

## 🎯 Objectifs du Projet

Ce projet a été créé pour :
- Comprendre les fondamentaux du scanning réseau
- Maîtriser la programmation réseau en Python (sockets, threading)
- Pratiquer l'analyse de sécurité réseau
- Développer un outil utilisable en pentest/audit

---

## ✨ Fonctionnalités

### 🔍 Scan de Ports
- Scan rapide multi-threadé
- Support de ports individuels ou plages (ex: `80,443` ou `1-1000`)
- Identification automatique des services (HTTP, SSH, FTP, etc.)
- Timeout configurable

### 🌐 Découverte d'Hôtes
- Support de la notation CIDR (ex: `192.168.1.0/24`)
- Détection automatique des hôtes actifs
- Résolution DNS inverse pour identifier les noms d'hôtes

### 📊 Génération de Rapports
- **Format TXT** : Rapport lisible pour l'humain
- **Format JSON** : Données structurées pour traitement automatisé
- Informations détaillées : IP, hostname, ports, services, timestamps

### ⚡ Performance
- Scan parallèle multi-threadé (jusqu'à 50 threads simultanés)
- Optimisation du timeout pour un scan rapide
- Gestion efficace des ressources

---

## 🛠️ Technologies Utilisées

- **Python 3.8+**
- **Bibliothèques standard** :
  - `socket` : Communication réseau bas niveau
  - `concurrent.futures` : Threading pour parallélisation
  - `ipaddress` : Manipulation d'adresses IP et réseaux
  - `json` : Sérialisation des rapports
  - `argparse` : Interface en ligne de commande

**Aucune dépendance externe requise !** ✅

---

## 📦 Installation

### Prérequis
- Python 3.8 ou supérieur
- Système Linux/macOS/Windows

### Téléchargement
```bash
# Cloner ou télécharger le projet
git clone https://github.com/votre-username/network-scanner.git
cd network-scanner

# Rendre le script exécutable (Linux/macOS)
chmod +x scanner.py
```

---

## 🚀 Utilisation

### Syntaxe de Base
```bash
python3 scanner.py -t <CIBLE> -p <PORTS> [OPTIONS]
```

### Exemples d'Utilisation

#### 1️⃣ Scanner une IP avec ports communs
```bash
python3 scanner.py -t 192.168.1.1 -p 80,443,22,21,25
```

#### 2️⃣ Scanner un réseau entier (CIDR)
```bash
python3 scanner.py -t 192.168.1.0/24 -p 80,443
```

#### 3️⃣ Scanner une plage de ports
```bash
python3 scanner.py -t scanme.nmap.org -p 1-1000
```

#### 4️⃣ Scanner avec timeout personnalisé
```bash
python3 scanner.py -t 192.168.1.100 -p 1-65535 --timeout 2 --threads 100
```

#### 5️⃣ Scanner avec nom de rapport personnalisé
```bash
python3 scanner.py -t 10.0.0.0/24 -p 80,443,22 -o mon_scan_reseau
```

### Options Disponibles

| Option | Description | Défaut |
|--------|-------------|--------|
| `-t, --target` | Cible(s) à scanner (IP, hostname, CIDR) | **Requis** |
| `-p, --ports` | Ports à scanner (ex: `80,443` ou `1-1000`) | `21,22,23,25,80,443,3306,3389,8080` |
| `--timeout` | Timeout pour les connexions (secondes) | `1` |
| `--threads` | Nombre de threads parallèles | `50` |
| `-o, --output` | Nom de base pour les fichiers de sortie | `scan_report` |

---

## 📊 Exemple de Sortie

### Console
```
============================================================
  NETWORK SCANNER - Analyse de Sécurité Réseau
  Auteur: Belaid AZIL
============================================================

[*] Scan de 192.168.1.1 en cours...
  [+] Port 22 ouvert - Service: ssh
  [+] Port 80 ouvert - Service: http
  [+] Port 443 ouvert - Service: https

============================================================
  Scan terminé en 3.45 secondes
  Hôtes avec ports ouverts: 1
  Total ports ouverts: 3
============================================================

[+] Rapport TXT généré: scan_report.txt
[+] Rapport JSON généré: scan_report.json
```

### Rapport TXT (`scan_report.txt`)
```
======================================================================
  RAPPORT D'ANALYSE RÉSEAU
======================================================================

INFORMATIONS DU SCAN:
----------------------------------------------------------------------
date: 2026-03-07 14:30:22
scanner: Network Scanner v1.0
author: Belaid AZIL
targets: ['192.168.1.1']
ports_scanned: 9

RÉSULTATS PAR HÔTE:
----------------------------------------------------------------------

Hôte: 192.168.1.1
  Nom d'hôte: router.local
  Heure du scan: 2026-03-07 14:30:25
  Ports ouverts (3):
    - Port 22/tcp (open) - Service: ssh
    - Port 80/tcp (open) - Service: http
    - Port 443/tcp (open) - Service: https

======================================================================
RÉSUMÉ:
----------------------------------------------------------------------
total_hosts_scanned: 1
total_open_ports: 3
scan_duration_seconds: 3.45
======================================================================
```

### Rapport JSON (`scan_report.json`)
```json
{
  "scan_info": {
    "date": "2026-03-07 14:30:22",
    "scanner": "Network Scanner v1.0",
    "author": "Belaid AZIL",
    "targets": ["192.168.1.1"],
    "ports_scanned": 9
  },
  "hosts": {
    "192.168.1.1": {
      "ip": "192.168.1.1",
      "hostname": "router.local",
      "scan_time": "2026-03-07 14:30:25",
      "open_ports": [
        {"port": 22, "state": "open", "service": "ssh"},
        {"port": 80, "state": "open", "service": "http"},
        {"port": 443, "state": "open", "service": "https"}
      ]
    }
  },
  "summary": {
    "total_hosts_scanned": 1,
    "total_open_ports": 3,
    "scan_duration_seconds": 3.45
  }
}
```

---

## 🔒 Considérations de Sécurité

### ⚠️ Usage Légal Uniquement
- **Ne scannez QUE vos propres réseaux ou ceux pour lesquels vous avez une autorisation explicite**
- Le scan de réseaux tiers sans permission est **illégal** dans la plupart des pays
- Cet outil est destiné à des fins éducatives et d'audit de sécurité autorisé

### 🛡️ Bonnes Pratiques
- Utiliser sur des environnements de test/lab
- Obtenir des autorisations écrites avant tout scan en production
- Respecter les politiques de sécurité de votre organisation
- Ne pas utiliser pour des activités malveillantes

---

## 🎓 Compétences Démontrées

Ce projet met en avant mes compétences en :
- ✅ **Programmation Python** : POO, gestion d'exceptions, threading
- ✅ **Réseaux** : Sockets TCP/IP, protocoles réseau, adressage IP
- ✅ **Sécurité** : Scanning de ports, énumération de services
- ✅ **Optimisation** : Programmation parallèle, gestion de performance
- ✅ **Documentation** : Code commenté, README professionnel

---

## 🚧 Améliorations Futures

- [ ] Support du protocole UDP
- [ ] Détection de version des services (banner grabbing)
- [ ] Export au format CSV et HTML
- [ ] Interface graphique (GUI)
- [ ] Détection d'OS (OS fingerprinting)
- [ ] Intégration de scripts NSE (Nmap Scripting Engine)

---

## 📚 Ressources & Apprentissage

### Concepts Abordés
- **TCP Three-Way Handshake** : Comprendre SYN/SYN-ACK/ACK
- **Port Scanning Techniques** : TCP Connect scan
- **Service Enumeration** : Identification des services courants
- **Python Threading** : Utilisation de `ThreadPoolExecutor`
- **Network Programming** : Module `socket` en Python

### Références
- [Python Socket Documentation](https://docs.python.org/3/library/socket.html)
- [OWASP Testing Guide - Port Scanning](https://owasp.org/)
- [Nmap Documentation](https://nmap.org/book/man.html)

---

## 👨‍💻 Auteur

**Belaid AZIL**
- 📧 Email: belaidazil48@gmail.com
- 🔗 LinkedIn: [linkedin.com/in/belaid-azil-42b30a2ba](https://linkedin.com/in/belaid-azil-42b30a2ba)
- 💻 GitHub: [github.com/Azilbelaid](https://github.com/Azilbelaid)
- 🎓 Étudiant en L3 Informatique - Université de Caen Normandie

---

## 📄 Licence

Ce projet est sous licence MIT. Voir le fichier `LICENSE` pour plus de détails.


**⭐ Si ce projet vous a été utile, n'hésitez pas à le partager ! ⭐**
