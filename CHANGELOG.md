# 📝 Historique des Modifications

## Version 1.1 - 09/03/2026

### ✨ Nouvelles fonctionnalités
- **Organisation des rapports** : Les rapports sont maintenant automatiquement sauvegardés dans un dossier `rapports/` créé à côté du script
- **Meilleure organisation** : Plus besoin de chercher les fichiers de rapport, ils sont tous centralisés

### 🔧 Améliorations
- Création automatique du dossier `rapports/` s'il n'existe pas
- Messages informatifs lors de la création du dossier
- Chemins complets affichés pour les fichiers générés

### 📁 Structure des fichiers
```
network_scanner/
├── scanner.py           # Script principal
├── README.md           # Documentation
├── EXAMPLES.md         # Exemples d'utilisation
├── LICENSE             # Licence MIT
├── .gitignore          # Fichiers à ignorer par Git
└── rapports/           # Dossier créé automatiquement
    ├── scan_report.txt
    └── scan_report.json
```

### 🎯 Exemple d'utilisation
```bash
python3 scanner.py -t 192.168.1.1 -p 80,443,22

# Résultat :
# [+] Dossier 'rapports/' créé
# [+] Rapport TXT généré: rapports/scan_report.txt
# [+] Rapport JSON généré: rapports/scan_report.json
```

---

## Version 1.0 - 07/03/2026

### 🚀 Version initiale
- Scan de ports TCP multi-threadé
- Découverte d'hôtes actifs (notation CIDR)
- Identification des services
- Génération de rapports TXT et JSON
- Interface CLI avec argparse
